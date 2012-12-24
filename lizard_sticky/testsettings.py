import os

DEBUG = True
TEMPLATE_DEBUG = True
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'test.db'
SITE_ID = 1
INSTALLED_APPS = [
    'lizard_sticky',
    'lizard_map',
    'lizard_ui',
    'compressor',
    'staticfiles',
    'django_nose',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.sites',
    ]
ROOT_URLCONF = 'lizard_sticky.urls'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Used for django-staticfiles
STATIC_URL = '/static_media/'
SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))
BUILDOUT_DIR = os.path.abspath(os.path.join(SETTINGS_DIR, '..'))
STATIC_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'static')

TEMPLATE_CONTEXT_PROCESSORS = (
    # Default items.
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    # Needs to be added for django-staticfiles to allow you to use
    # {{ STATIC_URL }}myapp/my.css in your templates.
    'staticfiles.context_processors.static_url',
    )

LIZARD_STICKY_STANDALONE = True

try:
    # Import local settings that aren't stored in svn.
    from lizard_sticky.local_testsettings import *
except ImportError:
    pass
