from django.db import models

from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractProductImage

from image_cropping import ImageRatioField

from designer_shop.models import Shop

class Product(AbstractProduct):
    shop = models.ForeignKey(Shop, default=None)

    @models.permalink
    def get_absolute_url(self):
        u"""Return a product's absolute url"""
        return ('designer_shop.views.itemdetail', (), {
            'shop_slug': self.slug,
            'item_slug': self.shop.slug})

    def primary_image(self):
        """
        Returns the primary image for a product. Usually used when one can
        only display one product image, e.g. in a list of products.
        Jon M - Overriding this to get images from the parent product
        """
        images = self.images.all() if self.is_parent else self.parent.images.all()
        ordering = self.images.model.Meta.ordering if self.is_parent else self.parent.images.model.Meta.ordering
        if not ordering or ordering[0] != 'display_order':
            # Only apply order_by() if a custom model doesn't use default
            # ordering. Applying order_by() busts the prefetch cache of
            # the ProductManager
            images = images.order_by('display_order')
        try:
            return images[0]
        except IndexError:
            # We return a dict with fields that mirror the key properties of
            # the ProductImage class so this missing image can be used
            # interchangeably in templates.  Strategy pattern ftw!
            return {
                'original': self.get_missing_image(),
                'caption': '',
                'is_missing': True}

class ProductImage(AbstractProductImage):
    cropping = ImageRatioField('original', '400x500', box_max_width=400, box_max_height=500)

from oscar.apps.catalogue.models import *