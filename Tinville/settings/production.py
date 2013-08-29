# Django settings for Tinville project.

from .base import *  # Start with base settings

# HEROKU Change!!!
import dj_database_url
DATABASES['default'] = dj_database_url.config()

STATIC_URL = S3_URL + STATIC_DIRECTORY
MEDIA_URL = S3_URL + MEDIA_DIRECTORY



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'd22ga7lmru7i9i',                      # Or path to database file if using sqlite3.
        'USER': 'yqtncenlctafzu',                      # Not used with sqlite3.
        'PASSWORD': 'zN8Vs8qqtmR3KXOJI6Mk6kKINY',                  # Not used with sqlite3.
        'HOST': 'ec2-54-221-199-33.compute-1.amazonaws.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}