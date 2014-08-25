import json
import collections
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.db import models
from oscar.apps.catalogue.models import ProductAttributeValue as Attributes
from oscar.apps.partner.models import StockRecord as StockRecords
from oscar.apps.catalogue.models import ProductImage as ProductImages
from django.core.urlresolvers import reverse


from oscar.core.loading import get_model
from designer_shop.models import Shop
from catalogue.models import Product
from oscar.apps.basket.models import Basket
from oscar.apps.partner import strategy
from common.utils import get_list_or_empty, get_or_none


# Create your views here.
def add_item_to_cart(request, shop_slug, item_slug):

    if request.method == 'GET':
        shop = get_object_or_404(Shop, slug__iexact=shop_slug)
        item = get_object_or_404(Product, slug__iexact=item_slug, shop_id=shop.id, parent__isnull=True)
        if not request.user.id is None:
            basket = get_object_or_404(Basket, owner_id=request.user.id)
            #this is getting all the variants and need to get the that info from the page
            variants = get_list_or_empty(Product, parent=item.id)
            qty = 1 #request.GET['qtyFilter']
            currentproduct = get_filtered_variant(variants,request.GET)
            #get product_id from variants
            stockrecord = get_object_or_404(StockRecords, product_id=currentproduct.id)
            if basket.line_quantity(product=currentproduct, stockrecord=stockrecord) == 0:
                # this item isnt in the basket
                line_ref=basket._create_line_reference(product=variants[0],stockrecord=stockrecord, options=None)
                basketline = get_model('basket', 'Line')(basket=basket, product=variants[0], line_reference=line_ref,
                                                         stockrecord=stockrecord,
                                                         quantity=qty,
                                                         price_currency=stockrecord.price_currency,
                                                         price_excl_tax=stockrecord.price_excl_tax,
                                                         price_incl_tax=stockrecord.price_excl_tax)
                basketline.save()
            else:
            #     ask Ray if this does nothing or increase qty
                return redirect('designer_shop.views.itemdetail', shop_slug, item_slug)

            # success_url = reverse('#')
            # return HttpResponseRedirect(success_url)
            return redirect('designer_shop.views.itemdetail', shop_slug, item_slug)
        else:
            return redirect('home')
        return redirect('designer_shop.views.itemdetail', shop_slug, item_slug)
    else:
        return redirect('designer_shop.views.itemdetail', shop_slug, item_slug)


def get_filtered_variant(variants, post):
    # sizeFilter = post['sizeFilter']
    # colorFilter = post['colorFilter']
    # filteredVariant = Product.objects.filter(Q(shop_id=shop.id, parent__isnull=True) & get_valid_categories_for_filter(genderfilter, itemtypefilter))
    filteredVariant = variants[0]
    return filteredVariant
