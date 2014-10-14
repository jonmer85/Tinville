# Django settings for Tinville project.

import os.path
import os
from unipath import Path

from oscar import get_core_apps
from oscar.defaults import *

# HEROKU Change!!!
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

AUTH_USER_MODEL = 'user.TinvilleUser'

PROJECT_DIR = Path(__file__).ancestor(2)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_DIR.child("media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ""

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_DIR.child("static"),

)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=5sic^#9yx+r9o5khng_8#!41y=5f8z8218bvpb)mu%p0q0xs3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django_mobile.loader.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Tinville.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'Tinville.wsgi.application'

from oscar import OSCAR_MAIN_TEMPLATE_DIR
location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', x)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_DIR.child("templates"),
    PROJECT_DIR.parent.child("dashboard"),
    OSCAR_MAIN_TEMPLATE_DIR
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django_mobile.context_processors.flavour',
    'user.context_processors.include_login_form',
    'oscar.apps.search.context_processors.search_form',
    'oscar.apps.promotions.context_processors.promotions',
    'oscar.apps.checkout.context_processors.checkout',
    'oscar.apps.customer.notifications.context_processors.notifications',
    'oscar.core.context_processors.metadata',
    'Tinville.context_processors.google_analytics_id',
    'Tinville.context_processors.include_shops'
    )

# Actual Tinville business logic
# django-jenkins needs it defined in this variable
PROJECT_APPS = [
    'Tinville',
    'user',
    'designer_shop',
    'common',
    'basket',
    'dashboard',
    'dashboard.orders'
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'crispy_forms',
    'braces',
    'parsley',
    'django.contrib.flatpages',
    'django_mobile',
    'django_jenkins',
    'fixture_media',
    'django_extensions',
    'compressor',
    'tinymce',
    'sorl.thumbnail',
    'django_basic_feedback',
    # 'debug_toolbar',
    'oscar_stripe'
] + PROJECT_APPS + get_core_apps(['catalogue', 'checkout', 'dashboard', 'dashboard.orders', 'order'])

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# For django-oscar search
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# DJANGO OSCAR SETTINGS
OSCAR_DEFAULT_CURRENCY = '$'
OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Processed', 'Cancelled',),
    'Cancelled': (),
}
OSCAR_ALLOW_ANON_CHECKOUT = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.heroku.com', 'herokuapp.com', 'www.tinville.com']

STATIC_DIRECTORY = '/static/'
MEDIA_DIRECTORY = '/media/'

EMAIL_HOST_USER = 'registration@tinville.com'
EMAIL_HOST_PASSWORD = 'Vill3Cr3w!2014'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

LOGIN_REDIRECT_URL = '/'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'menubar': True,
    'statusbar': False,
    'width': "75%",
    'height': "250px",
    'font-size': '22',
    'plugins': "spellchecker, paste, searchreplace, advimage",  
    'theme_advanced_buttons1': "fontsizeselect, separator, bold, italic, underline, separator, bullist, separator, outdent, indent, separator, undo, redo, separator, link",
    'cleaup_on_startup': True,
    'theme_advanced_path': False
    
}
TINYMCE_SPELLCHECKER = True
TINYMCE_PASTE = True

# to be overridden in other settings files
GOOGLE_ANALYTICS_TRACKING_ID = ''

STRIPE_PUBLISHABLE_KEY = 'pk_test_lxcDBw1osRxoju89EG9T5uS5'
STRIPE_SECRET_KEY = 'sk_test_uN49VakfMajXYBdTS4FM64VM'
STRIPE_CURRENCY = 'USD'
