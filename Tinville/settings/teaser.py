# Django settings for Tinville project.

from .base import *  # Start with base settings

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'd8r1jlreha6qkl',
    'HOST': 'ec2-107-20-191-205.compute-1.amazonaws.com',
    'PORT': 5432,
    'USER': 'jugdlwmcsppefe',
    'PASSWORD': 'dzRZWVVHkXPEjWllfKkg428ao3'
  }
}

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jon Meran', 'jon.meran@tinville.com'),
)