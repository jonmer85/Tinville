web: newrelic-admin run-program gunicorn Tinville.wsgi --worker-class gevent --log-file -
worker: python manage.py celery worker -B -l info