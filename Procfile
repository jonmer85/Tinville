web: gunicorn tinville.wsgi --log-file -
worker: python manage.py celery worker -B -l info