# Django settings for Tinville project.

from .base import *  # Start with base settings

# HEROKU Change!!!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'Tinville',                      # Or path to database file if using sqlite3.
        'USER': 'django_login',                      # Not used with sqlite3.
        'PASSWORD': 'django_login',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}