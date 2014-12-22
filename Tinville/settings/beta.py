# Django settings for Tinville project.

from .base import *  # Start with base settings

import dj_database_url
DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}

GOOGLE_ANALYTICS_TRACKING_ID = get_env_variable('GOOGLE_ANALYTICS_TRACKING_ID')

ALLOWED_HOSTS = ['tinville-beta.herokuapp.com', 'www.beta.tinville.com']

DEFAULT_FILE_STORAGE = 'common.s3utils.MediaS3BotoStorage'
STATICFILES_STORAGE = 'common.s3utils.StaticS3BotoStorage'

AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SECURE_URLS = False

S3_URL = 'http://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = S3_URL + STATIC_DIRECTORY
MEDIA_URL = S3_URL + MEDIA_DIRECTORY