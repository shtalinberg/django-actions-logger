from __future__ import unicode_literals

default_app_config = 'actionslog.apps.ActionslogConfig'


VERSION = (0, 3, 1)


def get_version():
    """Return the version as a string."""
    return '.'.join(map(str, VERSION))
