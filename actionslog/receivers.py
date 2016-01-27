from __future__ import unicode_literals

import json

from actionslog.diff import model_instance_diff
from actionslog.models import LogAction


def action_log_create(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a log entry when a model instance is first saved to the database.

    Direct use is discouraged, connect your model through :py:func:`actionslog.registry.register` instead.
    """
    if created:
        changes = model_instance_diff(None, instance)

        log_entry = LogAction.objects.create_log_action(
            instance=instance,
            action=LogAction.CREATE,
            changes=json.dumps(changes),
        )


def action_log_update(sender, instance, **kwargs):
    """
    Signal receiver that creates a log entry when a model instance is changed and saved to the database.

    Direct use is discouraged, connect your model through :py:func:`actionslog.registry.register` instead.
    """
    if instance.pk is not None:
        try:
            old = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            pass
        else:
            new = instance

            changes = model_instance_diff(old, new)

            # Log an entry only if there are changes
            if changes:
                log_entry = LogAction.objects.create_log_action(
                    instance=instance,
                    action=LogAction.UPDATE,
                    changes=json.dumps(changes),
                )


def action_log_delete(sender, instance, **kwargs):
    """
    Signal receiver that creates a log entry when a model instance is deleted from the database.

    Direct use is discouraged, connect your model through :py:func:`actionslog.registry.register` instead.
    """
    if instance.pk is not None:
        changes = model_instance_diff(instance, None)

        log_entry = LogAction.objects.create_log_action(
            instance=instance,
            action=LogAction.DELETE,
            changes=json.dumps(changes),
        )
