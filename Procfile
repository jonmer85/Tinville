web: newrelic-admin run-program gunicorn Tinville.wsgi --log-file -
worker: python manage.py celery worker -B -l info