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

DEFAULT_FILE_STORAGE = 'Tinville.Site.s3utils.MediaS3BotoStorage'
STATICFILES_STORAGE = 'Tinville.Site.s3utils.StaticS3BotoStorage'

AWS_STORAGE_BUCKET_NAME = 'tinville'
S3_URL = 'http://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = S3_URL + STATIC_DIRECTORY
MEDIA_URL = S3_URL + MEDIA_DIRECTORY

AWS_ACCESS_KEY_ID = 'AKIAJJLBU23GKJZH6SQA'
AWS_SECRET_ACCESS_KEY = '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'