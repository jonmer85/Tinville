# Django settings for Tinville project.

from .base import *  # Start with base settings

DEBUG = True

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'd16di73hdn2fpc',
    'HOST': 'ec2-54-235-250-41.compute-1.amazonaws.com',
    'PORT': 5432,
    'USER': 'htoivplvisbcjh',
    'PASSWORD': '6yphOtV57xayRDtMCPMd79Fth4'
  }
}

ALLOWED_HOSTS = ['tinville-alpha.herokuapp.com', 'www.alpha.tinville.com']

DEFAULT_FILE_STORAGE = 'common.s3utils.MediaS3BotoStorage'
STATICFILES_STORAGE = 'common.s3utils.StaticS3BotoStorage'

AWS_ACCESS_KEY_ID = 'AKIAJJLBU23GKJZH6SQA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'tinville-alpha'
AWS_S3_SECURE_URLS = False

S3_URL = 'http://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = S3_URL + STATIC_DIRECTORY
MEDIA_URL = S3_URL + MEDIA_DIRECTORY