=====================
django-actions-logger
=====================
.. image:: https://img.shields.io/pypi/dm/django-actions-logger.svg
    :target:  https://pypi.python.org/pypi/django-actions-logger/

.. image:: https://img.shields.io/pypi/v/django-actions-logger.svg
    :target:  https://pypi.python.org/pypi/django-actions-logger/

A Django app that keeps a log of user actions or changes in objects
You can log arbitrary action with user and optional info that goes with your action.

this code forked from django-auditlog and add my new ideas

Quick start
-----------

1. Add "actionslog" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'actionslog',
    ]


2. Run `python manage.py migrate` to create models.

