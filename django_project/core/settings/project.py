# coding=utf-8

"""Project level settings.

Adjust these values as needed but don't commit passwords etc. to any public
repository!
"""

import os  # noqa

from django.utils.translation import gettext_lazy as _

from .contrib import *  # noqa

ALLOWED_HOSTS = ['*']
ADMINS = (
    ('Dimas Ciputra', 'dimas@kartoza.com'),
)
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USERNAME'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': 5432,
        'TEST_NAME': 'unittests',
    }
}

# Due to profile page does not available,
# this will redirect to home page after login
LOGIN_REDIRECT_URL = '/'

# How many versions to list in each project box
PROJECT_VERSION_LIST_SIZE = 10

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

SOUTH_TESTS_MIGRATE = False

# Set languages which want to be translated
LANGUAGES = (
    ('en', _('English')),
)

# Set storage path for the translation files
LOCALE_PATHS = (absolute_path('locale'),)

# Extra installed apps
INSTALLED_APPS = INSTALLED_APPS + (
    'core',
    'georepo',
    'dashboard'
)

EXPORT_FOLDER_OUTPUT = os.path.join(
    MEDIA_ROOT,
    'export_data'
)

if not os.path.exists(EXPORT_FOLDER_OUTPUT):
    os.mkdir(EXPORT_FOLDER_OUTPUT)

GEOJSON_FOLDER_OUTPUT = os.path.join(
    EXPORT_FOLDER_OUTPUT,
    'geojson'
)

if not os.path.exists(GEOJSON_FOLDER_OUTPUT):
    os.mkdir(GEOJSON_FOLDER_OUTPUT)
