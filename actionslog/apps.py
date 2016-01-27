from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ActionslogConfig(AppConfig):
    name = 'actionslog'
    verbose_name = _("Actions logger")
