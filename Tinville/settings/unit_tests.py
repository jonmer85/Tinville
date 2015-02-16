# Django settings for Tinville project.

from .base import *  # Start with base settings
from tempfile import NamedTemporaryFile

DEBUG = False
TEMPLATE_DEBUG = DEBUG


DISABLE_BETA_ACCESS_CHECK = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PROJECT_DIR, 'unitdb.sqlite3'),
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

INSTALLED_APPS = INSTALLED_APPS + ['django_nose',] + ['extensions',]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SSLIFY_DISABLE = True

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
BROKER_BACKEND = 'memory'

LOCAL_STATIC_SERVE = env("LOCAL_STATIC_SERVE", True)
