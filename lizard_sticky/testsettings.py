import os
from lizard_ui.settingshelper import setup_logging
from lizard_ui.settingshelper import STATICFILES_FINDERS

SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))
BUILDOUT_DIR = os.path.abspath(os.path.join(SETTINGS_DIR, '..'))
LOGGING = setup_logging(BUILDOUT_DIR)
STATICFILES_FINDERS = STATICFILES_FINDERS

DEBUG = True
TEMPLATE_DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BUILDOUT_DIR, 'test.db')
    },
}
SITE_ID = 1
INSTALLED_APPS = [
    'lizard_sticky',
    'lizard_map',
    'lizard_ui',
    'lizard_security',
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
STATIC_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'media')
ADMIN_MEDIA_PREFIX = '/static_media/admin/'
LANGUAGES = (
    ('nl', 'Nederlands'),
    ('en', 'English'),
    )
USE_TZ = True

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
