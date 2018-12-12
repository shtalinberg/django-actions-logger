# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""Settings file for the Django project used for tests."""

import os

DEBUG = True
ALLOWED_HOSTS = ['*']

# Disable 1.9 arguments '--parallel' and try exclude  “Address already in use” at “setUpClass”
os.environ['DJANGO_TEST_PROCESSES'] = "1"
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = "localhost:8000-8010,8080,9200-9300"

PROJECT_NAME = 'project'

# Base paths.
ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT = os.path.join(ROOT, PROJECT_NAME)

# Django configuration.
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
DEBUG = TEMPLATE_DEBUG = True
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'actionslog',
    'nose',
    'django_nose',
    PROJECT_NAME,
)
LANGUAGE_CODE = os.getenv('ACTIONSLOG_LANGUAGE_CODE', 'en')
ROOT_URLCONF = PROJECT_NAME + '.urls'
SECRET_KEY = os.getenv('ACTIONSLOG_SECRET_KEY', 'secret')
SITE_ID = 1
STATIC_ROOT = os.path.join(PROJECT, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                # PROJECT_NAME + '.context_processors.navbar',
                # PROJECT_NAME + '.context_processors.versions',
            ],
        },

    },
]

# Testing.
NOSE_ARGS = (
    '--verbosity=2',
    '--stop',
    '-s',  # Don't capture stdout (any stdout output will be printed immediately) [NOSE_NOCAPTURE]
    # '--nomigrations',
    # '--with-coverage',
    # '--cover-package=actionslog',
)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG