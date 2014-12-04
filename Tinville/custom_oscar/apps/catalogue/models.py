from django.db import models

from oscar.apps.catalogue.abstract_models import AbstractProduct

from designer_shop.models import Shop

class Product(AbstractProduct):
    shop = models.ForeignKey(Shop, default=None)

    @models.permalink
    def get_absolute_url(self):
        u"""Return a product's absolute url"""
        return ('designer_shop.views.itemdetail', (), {
            'shop_slug': self.slug,
            'item_slug': self.shop.slug})

from oscar.apps.catalogue.models import *