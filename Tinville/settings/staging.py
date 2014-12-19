from .base import *  # Start with base settings

BROKER_URL=os.environ['REDISTOGO_URL'],
CELERY_RESULT_BACKEND=os.environ['REDISTOGO_URL']
