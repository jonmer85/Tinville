# Django settings for Tinville project.

from .base import *  # Start with base settings
from tempfile import NamedTemporaryFile

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PROJECT_DIR, 'lettucedb.sqlite3'),
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

LETTUCE_APPS = (
    'designer_shop',
    'user',
)

INSTALLED_APPS = INSTALLED_APPS + ['lettuce.django',  'django_nose',] + ['extensions',]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

########## TEST SETTINGS
#TEST_RUNNER = "discover_runner.DiscoverRunner"
#TEST_DISCOVER_TOP_LEVEL = PROJECT_DIR
#TEST_DISCOVER_ROOT = PROJECT_DIR
#TEST_DISCOVER_PATTERN = "test_*"
########## IN-MEMORY TEST DATABASE
