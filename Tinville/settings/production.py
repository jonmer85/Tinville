# Django settings for Tinville project.

from .base import *  # Start with base settings

import dj_database_url
DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}

# HEROKU Change!!!
import dj_database_url
DATABASES['default'] = dj_database_url.config()

DEFAULT_FILE_STORAGE = 'common.s3utils.MediaS3BotoStorage'
STATICFILES_STORAGE = 'common.s3utils.StaticS3BotoStorage'

AWS_ACCESS_KEY_ID = 'AKIAJJLBU23GKJZH6SQA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'tinville'
AWS_S3_SECURE_URLS = False

PAYPAL_API_USERNAME = 'dis.abreu_api1.tinville.com'
PAYPAL_API_PASSWORD = 'QJ2FDWUTCS698EVK'
PAYPAL_API_SIGNATURE = 'A.du0CNmdwFvvDeE1iilY11MlA-wAJ1j18ehYUGBKhRNaxN8bnPWvInR'

S3_URL = 'http://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = S3_URL + STATIC_DIRECTORY
MEDIA_URL = S3_URL + MEDIA_DIRECTORY

BROKER_URL=os.environ['REDISTOGO_URL'],
CELERY_RESULT_BACKEND=os.environ['REDISTOGO_URL']