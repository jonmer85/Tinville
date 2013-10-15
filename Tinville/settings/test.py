# Django settings for Tinville project.

from .base import *  # Start with base settings

TEST_RUNNER = 'discover_jenkins.runner.DiscoverCIRunner'
TEST_DISCOVER_PATTERN = "test_*"


DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}





########## TEST SETTINGS
#TEST_RUNNER = "discover_runner.DiscoverRunner"
#TEST_DISCOVER_TOP_LEVEL = PROJECT_DIR
#TEST_DISCOVER_ROOT = PROJECT_DIR
#TEST_DISCOVER_PATTERN = "test_*"
########## IN-MEMORY TEST DATABASE
