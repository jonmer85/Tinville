# Django settings for Tinville project.

from .base import *  # Start with base settings

# HEROKU Change!!!
import dj_database_url
DATABASES['default'] = dj_database_url.config()

STATIC_URL = S3_URL + STATIC_DIRECTORY
MEDIA_URL = S3_URL + MEDIA_DIRECTORY