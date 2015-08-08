# Django settings for Tinville project.

from .lettuce_tests import *  # Start with base settings

DATABASES = {
    "default": {
        "ENGINE": 'django_postgrespool',
        "NAME": 'd82sme94fdr4c4',
        "USER": "metppdydnqiilm",
        "PASSWORD": "Q8jDKxyF-IkE9TfSqBsw8FF4yf",
        "HOST": "ec2-54-204-0-120.compute-1.amazonaws.com",
        "PORT": "5432",
    },
}