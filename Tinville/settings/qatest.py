# Django settings for Tinville project.

from .base import *  # Start with base settings
import urlparse

# HEROKU Change!!!
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['tinville-testing.herokuapp.com']

import dj_database_url
DATABASES = {'default': dj_database_url.config(default=env('DATABASE_URL'))}

DEFAULT_FILE_STORAGE = 'common.s3utils.MediaS3BotoStorage'
STATICFILES_STORAGE = 'common.s3utils.StaticS3BotoStorage'
THUMBNAIL_DEFAULT_STORAGE = 'common.s3utils.MediaS3BotoStorage'

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SECURE_URLS = True
AWS_IS_GZIPPED = env('AWS_IS_GZIPPED', True)
AWS_QUERYSTRING_EXPIRE = env('AWS_QUERYSTRING_EXPIRE', 63115200)
AWS_HEADERS = {
    'Cache-Control': env('AWS_CACHE_CONTROL', 'public, max-age=2592000'),
}

S3_URL = '//%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = S3_URL + STATIC_DIRECTORY
MEDIA_URL = S3_URL + MEDIA_DIRECTORY

COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

BROKER_URL=os.environ.get('REDISTOGO_URL', None)
CELERY_RESULT_BACKEND=os.environ.get('REDISTOGO_URL', None)

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6959'))

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': redis_url.password,
        }
    }
}