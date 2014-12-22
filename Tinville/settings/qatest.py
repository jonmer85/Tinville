# Django settings for Tinville project.

from .base import *  # Start with base settings

# HEROKU Change!!!
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['tinville-testing.herokuapp.com']

import dj_database_url
DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}

DEFAULT_FILE_STORAGE = 'common.s3utils.MediaS3BotoStorage'
STATICFILES_STORAGE = 'common.s3utils.StaticS3BotoStorage'

AWS_ACCESS_KEY_ID = 'AKIAJJLBU23GKJZH6SQA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'tinville-testing'
AWS_S3_SECURE_URLS = False

S3_URL = 'http://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = S3_URL + STATIC_DIRECTORY
MEDIA_URL = S3_URL + MEDIA_DIRECTORY

BROKER_URL=os.environ.get('REDISTOGO_URL', None)
CELERY_RESULT_BACKEND=os.environ.get('REDISTOGO_URL', None)