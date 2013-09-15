# Django settings for Tinville project.

from .base import *  # Start with base settings

# HEROKU Change!!!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'd59iq3hg83vsoq',
    'HOST': 'ec2-107-21-120-102.compute-1.amazonaws.com',
    'PORT': 5432,
    'USER': 'xvhimzngcdsccg',
    'PASSWORD': 'kNzd6vhVm7ZeHke961oiIkeZno'
  }
}