from .base import *  # Start with base settings

BROKER_URL=os.environ.get('REDISTOGO_URL', None)
CELERY_RESULT_BACKEND=os.environ.get('REDISTOGO_URL', None)
