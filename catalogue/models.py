from django.db import models

from oscar.apps.catalogue.abstract_models import AbstractProduct

from designer_shop.models import Shop

class Product(AbstractProduct):
    shop = models.ForeignKey(Shop)

from oscar.apps.catalogue.models import *