from .base import *  # Start with base settings

BROKER_URL=env('REDISTOGO_URL', None)
CELERY_RESULT_BACKEND=env('REDISTOGO_URL', None)
