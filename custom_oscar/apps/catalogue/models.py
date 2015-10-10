from django.db import models
from easy_thumbnails.files import get_thumbnailer

from common.utils import get_list_or_empty, get_or_none
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractProductImage, AbstractAttributeOption

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

    def get_size(self):
        from oscar.apps.catalogue.models import ProductAttributeValue as Attributes
        sizeSet = ""
        sizeX = ""
        sizeY = ""
        sizeNum = ""
        divider = ""
        oneSize = ""
        if get_or_none(Attributes, product_id=self.id, attribute_id=5) != None:
            if get_or_none(Attributes, product_id=self.id, attribute_id=1) != None:
                sizeSet = get_or_none(Attributes, product_id=self.id, attribute_id=1).value_as_text

            if get_or_none(Attributes, product_id=self.id, attribute_id=2) != None:
                sizeX = get_or_none(Attributes, product_id=self.id, attribute_id=2).value_as_text

            if get_or_none(Attributes, product_id=self.id, attribute_id=3) != None:
                sizeY = get_or_none(Attributes, product_id=self.id, attribute_id=3).value_as_text

            if get_or_none(Attributes, product_id=self.id, attribute_id=4) != None:
                sizeNum = get_or_none(Attributes, product_id=self.id, attribute_id=4).value_as_text

            if get_or_none(Attributes, product_id=self.id, attribute_id=6) != None:
                oneSize = "One Size"

            if sizeX != "" and sizeY != "":
                divider = " x "

            return str(sizeSet) + str(sizeX) + divider + str(sizeY) + str(sizeNum) + str(oneSize)

    def get_color(self):
        from oscar.apps.catalogue.models import ProductAttributeValue as Attributes
        if get_or_none(Attributes, product_id=self.id, attribute_id=5) != None:
            primary_color = get_or_none(Attributes, product_id=self.id, attribute_id=5).value_as_text
            secondary_color = get_or_none(Attributes, product_id=self.id, attribute_id=7)
            if secondary_color:
                return str(primary_color).capitalize() + "/" + str(secondary_color.value_as_text).capitalize()
            else:
                return str(primary_color).capitalize()




class ProductImage(AbstractProductImage):
    cropping = ImageRatioField('original', '400x400', box_max_width=200)

    def delete(self, *args, **kwargs):
        thumbnailer = get_thumbnailer(self.original)
        thumbnailer.delete_thumbnails()
        super(ProductImage, self).delete(*args, **kwargs)

class AttributeOption(AbstractAttributeOption):
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='child_colors',
        verbose_name=("Parent attribute"))

from oscar.apps.catalogue.models import *