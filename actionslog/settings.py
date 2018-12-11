# """Django Actions Log settings file."""
#
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


CREATE = 100
SUCCESS = 110
ACTIVATE = 130
AUTH = 150
VIEW = 180
UPDATE = 200
SUSPEND = 250
UNSUSPEND = 260
DELETE = 300
TERMINATE = 500
FAILED = 999
ERROR = 1000

LOG_ACTION_CHOICES_DEFAULT = [
    (CREATE, _("create")),
    (SUCCESS, _("success")),
    (ACTIVATE, _("activate")),
    (AUTH, _("authorize")),
    (VIEW, _("view")),
    (UPDATE, _("update")),
    (SUSPEND, _("suspend")),
    (UNSUSPEND, _("unsuspend")),
    (DELETE, _("delete")),
    (TERMINATE, _("terminate")),
    (FAILED, _("failed")),
    (ERROR, _("error")),
]


AL_LOG_ACTION_SETTINGS = getattr(
    settings, 'AL_LOG_ACTION_CHOICES',
    LOG_ACTION_CHOICES_DEFAULT
)

LOG_ACTION_CHOICES = [
    (value[0], value[1])
    for value in AL_LOG_ACTION_SETTINGS
]


