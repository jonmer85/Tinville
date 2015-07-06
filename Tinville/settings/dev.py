# Django settings for Tinville project.

from .base import *  # Start with base settings
import urlparse

import dj_database_url
DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}

# HEROKU Change!!!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['tinville-dev.herokuapp.com']

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
    'Cache-Control': str(env('AWS_CACHE_CONTROL', 'public, max-age=2592000')),
}
AWS_S3_FILE_OVERWRITE = env('AWS_S3_FILE_OVERWRITE', False)

S3_URL = '//%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = S3_URL + STATIC_DIRECTORY
MEDIA_URL = S3_URL + MEDIA_DIRECTORY

COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'



BROKER_URL=env('REDISTOGO_URL')
CELERY_RESULT_BACKEND=env('REDISTOGO_URL')

SSLIFY_DISABLE = False

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
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': env('REDIS_POOL_MAX_CONNECTIONS', 50),
                'timeout': env('REDIS_POOL_TIMEOUT', 30),
            }
        }
    }
}
