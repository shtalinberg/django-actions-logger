
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.admin.utils import quote
from django.contrib.contenttypes.models import ContentType
try:
    from django.urls import NoReverseMatch, reverse
except ImportError:
    from django.core.urlresolvers import NoReverseMatch, reverse
from django.db import models
from django.db.models import QuerySet, Q
from django.utils.encoding import python_2_unicode_compatible, smart_text
from django.utils.six import iteritems, integer_types
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import lazy

from jsonfield import JSONField

from .signals import action_logged
from . import settings as app_conf

import json


class LogActionManager(models.Manager):

    def create_log_action(self, **kwargs):
        """
        Helper method to create a new log entry.
        This method automatically populates some fields when no explicit value is given.
        :param instance: The model instance to log a change for.
        :type instance: Model
        :param kwargs: Field overrides for the :py:class:`LogAction` object.
        :return: The new log entry or `None` if there were no changes.
        :rtype: LogAction
        """
        instance = kwargs.get('instance', None)
        if instance is not None:
            del kwargs['instance']

        request = kwargs.get('request', None)
        if request is not None:
            del kwargs['request']
            # Let's grab the current IP of the user.
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                remote_ip = x_forwarded_for.split(',')[0]
            else:
                remote_ip = request.META.get('REMOTE_ADDR')
            kwargs.setdefault('remote_ip', remote_ip)

        if instance is not None:
            pk = self._get_pk_value(instance)

            kwargs.setdefault(
                'content_type',
                ContentType.objects.get_for_model(instance)
            )
            kwargs.setdefault('object_pk', pk)
            kwargs.setdefault('object_repr', smart_text(instance))

            if isinstance(pk, integer_types):
                kwargs.setdefault('object_id', pk)

            get_object_extra_info = getattr(
                instance,
                'get_object_extra_info',
                None
            )

            if callable(get_object_extra_info):
                kwargs.setdefault('object_extra_info', get_object_extra_info())

            # Delete log entries with the same pk as a newly created model.
            # This should only be necessary when an pk is used twice.
            if kwargs.get('action', None) is app_conf.CREATE:
                is_obj_exists = self.filter(
                    content_type=kwargs.get('content_type'),
                    object_id=kwargs.get('object_id')
                ).exists()

                if kwargs.get('object_id', None) is not None and is_obj_exists:
                    self.filter(
                        content_type=kwargs.get('content_type'),
                        object_id=kwargs.get('object_id')
                    ).delete()
                else:
                    self.filter(
                        content_type=kwargs.get('content_type'),
                        object_pk=kwargs.get('object_pk', '')
                    ).delete()

        action_log = self.create(**kwargs)
        action_logged.send(sender=LogAction, action=action_log)
        return action_log

    def get_for_model(self, model):
        """
        Get log entries for all objects of a specified type.
        :param model: The model to get log entries for.
        :type model: class
        :return: QuerySet of log entries for the given model.
        :rtype: QuerySet
        """
        # Return empty queryset if the given object is not valid.
        if not issubclass(model, models.Model):
            return self.none()

        ct = ContentType.objects.get_for_model(model)

        return self.filter(content_type=ct)

    def get_for_objects(self, queryset):
        """
        Get log entries for the objects in the specified queryset.
        :param queryset: The queryset to get the log entries for.
        :type queryset: QuerySet
        :return: The LogAction objects for the objects in the given queryset.
        :rtype: QuerySet
        """
        if not isinstance(queryset, QuerySet) or queryset.count() == 0:
            return self.none()

        content_type = ContentType.objects.get_for_model(queryset.model)
        primary_keys = queryset.values_list(queryset.model._meta.pk.name, flat=True)

        if isinstance(primary_keys[0], integer_types):
            return self.filter(content_type=content_type).filter(Q(object_id__in=primary_keys)).distinct()
        else:
            return self.filter(content_type=content_type).filter(Q(object_pk__in=primary_keys)).distinct()

    def _get_pk_value(self, instance):
        """
        Get the primary key field value for a model instance.
        :param instance: The model instance to get the primary key for.
        :type instance: Model
        :return: The primary key value of the given model instance.
        """
        pk_field = instance._meta.pk.name
        pk = getattr(instance, pk_field, None)

        # Check to make sure that we got an pk not a model object.
        if isinstance(pk, models.Model):
            pk = self._get_pk_value(pk)
        return pk


def get_action_choices():
    return app_conf.LOG_ACTION_CHOICES


@python_2_unicode_compatible
class LogAction(models.Model):

    content_type = models.ForeignKey(
        'contenttypes.ContentType', related_name='+',
        verbose_name=_("content type"),
        blank=True, null=True, on_delete=models.SET_NULL
    )
    object_id = models.BigIntegerField(
        verbose_name=_("object id"),
        blank=True, null=True, db_index=True
    )
    object_pk = models.CharField(
        verbose_name=_("object pk"), max_length=255,
        blank=True, null=True, db_index=True
    )

    object_repr = models.TextField(
        verbose_name=_("object representation"),
        blank=True, null=True
    )
    object_extra_info = JSONField(
        verbose_name=_("object information"),
        blank=True, null=True
    )

    session_key = models.CharField(_('session key'), max_length=40, blank=True, null=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("user"),
        blank=True, null=True,
        on_delete=models.SET_NULL, related_name='actionlogs'
    )

    action = models.PositiveSmallIntegerField(verbose_name=_("action"), blank=True, null=True)

    action_info = JSONField(
        verbose_name=_("action information"),
        blank=True, null=True
    )
    changes = models.TextField(blank=True, verbose_name=_("change message"))

    remote_ip = models.GenericIPAddressField(
        verbose_name=_("remote IP"), blank=True, null=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"), auto_now_add=True, db_index=True
    )

    objects = LogActionManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("log action")
        verbose_name_plural = _("log actions")

    def __str__(self):
        if self.object_repr:
            return _("Logged {repr:s}").format(repr=self.object_repr)
        elif self.action:
            return _("Logged action, type: {action}, id: {id}").format(
                action=self.get_action_display(),
                id=self.id
            )
        else:
            return _("Logged action, id: {id}").format(id=self.id)

    def __init__(self, *args, **kwargs):
        super(LogAction, self).__init__(*args, **kwargs)
        try:
            self._meta.get_field('action').choices = \
                lazy(get_action_choices, list)()
        except:
            # for Django < 1.11
            self._meta.get_field_by_name('action')[0]._choices = \
                lazy(get_action_choices, list)()

    def get_action_display(self):
        for action in app_conf.LOG_ACTION_CHOICES:
            if action[0] == self.action:
                return action[1]
        return _('Not provided')

    def get_edited_object(self):
        """Returns the edited object represented by this log entry"""
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def get_admin_url(self):
        """
        Returns the admin URL to edit the object represented by this log entry.
        """
        if self.content_type and self.object_id:
            url_name = 'admin:%s_%s_change' % (
                self.content_type.app_label,
                self.content_type.model
            )
            try:
                return reverse(url_name, args=(quote(self.object_id),))
            except NoReverseMatch:
                pass
        return None

    @property
    def changes_dict(self):
        """
        :return: The changes recorded in this log entry as a dictionary object.
        """
        try:
            return json.loads(self.changes)
        except ValueError:
            return {}

    @property
    def changes_str(self, colon=': ', arrow=smart_text(' \u2192 '), separator='; '):
        """
        Return the changes recorded in this log entry as a string.
        The formatting of the string can be customized by
        setting alternate values for colon, arrow and separator.
        If the formatting is still not satisfying, please use
        :py:func:`LogAction.changes_dict` and format the string yourself.
        :param colon: The string to place between the field name and the values.
        :param arrow: The string to place between each old and new value.
        :param separator: The string to place between each field.
        :return: A readable string of the changes in this log entry.
        """
        substrings = []

        for field, values in iteritems(self.changes_dict):
            substring = smart_text('{field_name:s}{colon:s}{old:s}{arrow:s}{new:s}').format(
                field_name=field,
                colon=colon,
                old=values[0],
                arrow=arrow,
                new=values[1],
            )
            substrings.append(substring)

        return separator.join(substrings)
