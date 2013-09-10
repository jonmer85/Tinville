# Django settings for Tinville project.

from .base import *  # Start with base settings

# HEROKU Change!!!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'd2c638gaii8jv7',
    'HOST': 'ec2-23-23-211-161.compute-1.amazonaws.com',
    'PORT': 5432,
    'USER': 'xmrcaidzbiewqs',
    'PASSWORD': 'jqnzeIdyhXy9mmfYa6cwleCONg'
  }
}