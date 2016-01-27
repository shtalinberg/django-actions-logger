from __future__ import unicode_literals

import threading
import time

from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.functional import curry
from django.apps import apps
from actionslog.models import LogAction


threadlocal = threading.local()


class ActionslogMiddleware(object):
    """
    Middleware to couple the request's user to log items. This is accomplished by currying the signal receiver with the
    user from the request (or None if the user is not authenticated).
    """

    def process_request(self, request):
        """
        Gets the current user from the request and prepares and connects a signal receiver with the user already
        attached to it.
        """
        # Initialize thread local storage
        threadlocal.actionslog = {
            'signal_duid': (self.__class__, time.time()),
            'remote_ip': request.META.get('REMOTE_ADDR'),
        }

        # In case of proxy, set 'original' address
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            threadlocal.actionslog['remote_ip'] = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]

        # Connect signal for automatic logging
        if hasattr(request, 'user') and hasattr(request.user, 'is_authenticated') and request.user.is_authenticated():
            set_user = curry(self.set_user, request.user)
            pre_save.connect(set_user, sender=LogAction, dispatch_uid=threadlocal.actionslog['signal_duid'], weak=False)

    def process_response(self, request, response):
        """
        Disconnects the signal receiver to prevent it from staying active.
        """
        if hasattr(threadlocal, 'actionslog'):
            pre_save.disconnect(sender=LogAction, dispatch_uid=threadlocal.actionslog['signal_duid'])

        return response

    def process_exception(self, request, exception):
        """
        Disconnects the signal receiver to prevent it from staying active in case of an exception.
        """
        if hasattr(threadlocal, 'actionslog'):
            pre_save.disconnect(sender=LogAction, dispatch_uid=threadlocal.actionslog['signal_duid'])

        return None

    @staticmethod
    def set_user(user, sender, instance, **kwargs):
        """
        Signal receiver with an extra, required 'user' kwarg. This method becomes a real (valid) signal receiver when
        it is curried with the user.
        """
        try:
            app_label, model_name = settings.AUTH_USER_MODEL.split('.')
            auth_user_model = apps.get_model(app_label, model_name)
        except ValueError:
            auth_user_model = apps.get_model('auth', 'user')
        if sender == LogAction and isinstance(user, auth_user_model) and instance.user is None:
            instance.user = user
        if hasattr(threadlocal, 'actionslog'):
            instance.remote_ip = threadlocal.actionslog['remote_ip']
