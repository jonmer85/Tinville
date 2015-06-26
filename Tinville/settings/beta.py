# Django settings for Tinville project.

from .base import *  # Start with base settings
import urlparse

import dj_database_url

DATABASES = {'default': dj_database_url.config(default=env('DATABASE_URL'))}
DATABASES['default']['ENGINE'] = 'django_postgrespool'

SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2'
}

DATABASE_POOL_ARGS = {
    'max_overflow': 0,
    'pool_size': 120,  # Heroku's Standard 0 connection limit
    'recycle': 300
}

GOOGLE_ANALYTICS_TRACKING_ID = env('GOOGLE_ANALYTICS_TRACKING_ID')

ALLOWED_HOSTS = ['tinville-beta.herokuapp.com', 'www.beta.tinville.com', 'beta.tinville.com', 'www.tinville.com', 'tinville.com']

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
                'max_connections': 50,
                'timeout': 20,
            }
        }
    }
}

# List of callables that know how to import templates from various sources.
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)