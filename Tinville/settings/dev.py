# Django settings for Tinville project.

from .base import *  # Start with base settings

# HEROKU Change!!!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['tinville-dev.herokuapp.com']

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

DEFAULT_FILE_STORAGE = 'common.s3utils.MediaS3BotoStorage'
STATICFILES_STORAGE = 'common.s3utils.StaticS3BotoStorage'

AWS_ACCESS_KEY_ID = 'AKIAJJLBU23GKJZH6SQA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'tinville-dev'
AWS_S3_SECURE_URLS = False

S3_URL = 'http://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = S3_URL + STATIC_DIRECTORY
MEDIA_URL = S3_URL + MEDIA_DIRECTORY

BROKER_URL=os.environ.get('REDISTOGO_URL', None)
CELERY_RESULT_BACKEND=os.environ.get('REDISTOGO_URL', None)