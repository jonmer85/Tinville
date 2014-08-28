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
from django.db.models import Q
from django.contrib import messages


from oscar.core.loading import get_model
from designer_shop.models import Shop
from catalogue.models import Product
from oscar.apps.basket.models import Basket
from oscar.apps.basket.models import Line

from oscar.apps.partner import strategy
from common.utils import get_list_or_empty, get_or_none
from django.utils.html import strip_tags

# Create your views here.
def add_item_to_cart(request, shop_slug, item_slug):

    if request.method == 'POST':
        shop = get_object_or_404(Shop, slug__iexact=shop_slug)
        item = get_object_or_404(Product, slug__iexact=item_slug, shop_id=shop.id, parent__isnull=True)
        #this is getting all the variants and need to get the that info from the page
        variants = get_list_or_empty(Product, parent=item.id)
        qty = int(request.POST['qtyFilter'])
        msg = ''
        # ToDo figure out this tax stuff
        tax = 1
        currentproduct = get_filtered_variant(variants,request.POST)
        image = get_list_or_empty(ProductImages, product_id=item.id)
        #get product_id from variants
        stockrecord = get_object_or_404(StockRecords, product_id=currentproduct.id)
        price_excl_tax = stockrecord.price_excl_tax * qty
        price_incl_tax = (stockrecord.price_excl_tax * qty) * tax
        if not request.user.id is None:
            basket = get_object_or_404(Basket, owner_id=request.user.id)
            if not basket.has_strategy:
                basket._set_strategy(strategy)
            line_quantity = basket.line_quantity(product=currentproduct, stockrecord=stockrecord)
            line_ref=basket._create_line_reference(product=currentproduct,stockrecord=stockrecord, options=None)
            if line_quantity == 0:
                # item not in the basket line
                basketline = get_model('basket', 'Line')(basket=basket, product=currentproduct, line_reference=line_ref,
                                                         stockrecord=stockrecord,
                                                         quantity=qty,
                                                         price_currency=stockrecord.price_currency,
                                                         price_excl_tax=price_excl_tax,
                                                         price_incl_tax=price_incl_tax)
                basketline.save()
                basketlineId = basketline.id
            elif line_quantity == qty:
                msg = "You have tried to add the same item, please change the quantity"
                # messages.warning(request, msg)
                basketlineId = 0
            else:
                # item already in the basket_line but add to the qty
                basketline = Line.objects.get(basket=basket, product=currentproduct, line_reference=line_ref)
                basketline.quantity = qty
                basketline.save(update_fields=["quantity"])
                basketlineId = 0
        else:
            # not logged in or does not have an account
            basketlineId = -1
        cartInfo = {'Id': basketlineId,
                    'title': currentproduct.title,
                    'description': strip_tags(item.description),
                    'price': float(price_excl_tax),
                    'image': str(image[0].original),
                    'msg': msg}
        return HttpResponse(json.dumps(cartInfo, {'errors': 'error'}), mimetype='application/json')
    else:
        return redirect('designer_shop.views.itemdetail', shop_slug, item_slug)


def get_filtered_variant(variants, post):
    sizeFilter = post['sizeFilter']
    colorFilter = post['colorFilter']
    # foo = Product.object.filter(attribute_values__values_option_id=5)
    # for variant in variants:
    #     get_or_none(Product, productattributevalue__)
    # product = get_object_or_404(Product, productattributevalue__ )
    # filter = list()
    # filter.append(Q(attributes__value_option__contains=colorFilter))
    # # filter.append(Q(attributes__value__contains=sizeFilter))
    #
    # qs = filter
    # if filter != []:
    #     query = qs.pop()
    #     for q in qs:
    #         query &= q
    # else:
    #     query = Q(parent__isnull=True)
    #
    # return query
    # # filteredVariant = None
    # for variant in variants:
    #
    #     size_setattr = get_or_none(Attributes, product_id=variant.id, attribute_id=1)
    #     size_dim_xattr = get_or_none(Attributes, product_id=variant.id, attribute_id=2)
    #     size_dim_yattr = get_or_none(Attributes, product_id=variant.id, attribute_id=3)
    #     size_numattr = get_or_none(Attributes, product_id=variant.id, attribute_id=4)
    #     colorattribute = get_or_none(Attributes, product_id=variant.id, attribute_id=5)
    #     if colorattribute.value.option.lower() == colorFilter.lower():
    #         if size_setattr.value.option.lower() == sizeFilter.lower():
    #             return variant
    #         elif str(size_dim_xattr.valu) + " x " + str(size_dim_yattr.value) == str(sizeFilter):
    #             return variant
    #         elif str(size_numattr.value) == sizeFilter.lower():
    #             return variant
    return variants[0]


def delete_item_to_cart(request):
    cartId = request.POST['Id']
    basketline = Line.objects.get(pk=cartId).delete()
    return HttpResponse(json.dumps({'deleted': True}, {'errors': 'error'}), mimetype='application/json')
