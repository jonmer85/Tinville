import json
import collections
from decimal import Decimal
import simplejson as json
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.db import models
from oscar.apps.catalogue.models import ProductAttributeValue as Attributes
from oscar.apps.catalogue.models import AttributeOption
from oscar.apps.partner.models import StockRecord as StockRecords
from oscar.apps.catalogue.models import ProductImage as ProductImages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages


from oscar.core.loading import get_model
from oscar.core.loading import get_class
from designer_shop.models import Shop

from oscar.apps.partner import strategy
from common.utils import get_list_or_empty, get_or_none
from django.utils.html import strip_tags
from oscar.apps.basket import signals

Basket = get_model('basket', 'basket')
Product = get_model('catalogue', 'product')
Line = get_model('basket', 'line')
Selector = get_class('partner.strategy', 'Selector')

selector = Selector()
add_signal = signals.basket_addition

# Create your views here.
def load_cart(request):
    if request.method == 'GET':
        cartItems = []
        basket = request.basket
        index = 0
        ret = request.POST
        basketlines = get_list_or_empty(Line, basket_id=basket)
        if len(basketlines) > 0:
            for basketline in basketlines:
                currentproduct = get_object_or_404(Product, id=basketline.product_id)
                parentproduct = get_object_or_404(Product, id=currentproduct.parent_id)
                image = get_list_or_empty(ProductImages, product_id=parentproduct.id)
                stockrecord = get_object_or_404(StockRecords, product_id=basketline.product_id)
                price_excl_tax = basketline.price_excl_tax
                cartInfo = {'Id': basketline.id,
                            'product_id': currentproduct.id,
                            'title': currentproduct.title,
                            'description': strip_tags(parentproduct.description),
                            'price': float(basketline.price_excl_tax),
                            'image': str(image[0].original),
                            'qty': basketline.quantity,
                            'msg': ''}
                cartItems.append(cartInfo)

        return HttpResponse(json.dumps(cartItems), mimetype='application/json')



def addBasket(request, product_id, qty):
    msg = ''
    # ToDo figure out this tax stuff
    tax = 1
    stockrecord = get_object_or_404(StockRecords, product_id=product_id)
    if(qty > stockrecord.num_in_stock):
        errorMsg = "Quantity is greater than {0}.".format(stockrecord.num_in_stock)
        return HttpResponseBadRequest(json.dumps({'errors': errorMsg}), mimetype='application/json')
    if(qty < 1):
        return HttpResponseBadRequest(json.dumps({'errors': "Quantity cannot be less than 1."}), mimetype='application/json')

    currentproduct = get_object_or_404(Product, id=product_id)
    parentproduct = get_object_or_404(Product, id=currentproduct.parent_id)
    price_excl_tax = stockrecord.price_excl_tax * qty
    price_incl_tax = (stockrecord.price_excl_tax * qty) * tax
    image = get_list_or_empty(ProductImages, product_id=parentproduct.id)


    basket = request.basket
    line_quantity = basket.line_quantity(product=currentproduct, stockrecord=stockrecord)
    line_ref=basket._create_line_reference(product=currentproduct, stockrecord=stockrecord, options=None)
    if line_quantity == 0:
        # item not in the basket line
        basket.add_product(currentproduct,qty)
        # Send signal for basket addition
        add_signal.send(sender=None,product=currentproduct, user=request.user, request=request)
        basketline = get_list_or_empty(Line, line_reference=line_ref, basket_id=basket.id)[0]

    else:
        # item already in the basket_line but add to the qty
        basketline = Line.objects.get(basket=basket, product=currentproduct, line_reference=line_ref)
        basketline.quantity = qty
        basketline.save(update_fields=["quantity"])
    basketlineId = basketline.id

    cartInfo = {'Id': basketlineId,
                'product_id': currentproduct.id,
                'title': currentproduct.title,
                'description': strip_tags(parentproduct.description),
                'price': float(price_excl_tax),
                'image': str(image[0].original),
                'qty': qty,
                'msg': msg}
    return HttpResponse(json.dumps(cartInfo), mimetype='application/json')


def add_item_to_cart(request, shop_slug, item_slug):

    if request.method == 'POST':
        shop = get_object_or_404(Shop, slug__iexact=shop_slug)
        item = get_object_or_404(Product, slug__iexact=item_slug, shop_id=shop.id, parent__isnull=True)
        #this is getting all the variants and need to get the that info from the page
        variants = get_list_or_empty(Product, parent=item.id)
        qty = int(request.POST['qtyFilter'])
        msg = ''
        if request.POST['colorFilter'] == '':
            return HttpResponseBadRequest(json.dumps({'errors': 'Please select a color!'}), mimetype='application/json')
        if request.POST['sizeFilter'] == '':
            return HttpResponseBadRequest(json.dumps({'errors': 'Please select a size!'}), mimetype='application/json')
        # varItem = Product.objects.filter(attribute_values__value_option_id=2)
        currentproduct = get_filtered_variant(item.id, request.POST)
        image = get_list_or_empty(ProductImages, product_id=item.id)
        return addBasket(request,currentproduct.id,qty)
    else:
        return redirect('designer_shop.views.itemdetail', shop_slug, item_slug)

# Purpose: Update a pre-existing cart item
# Params:
#        product_id  -- The id of the product
#        quantity    -- The number of the product which cannot be less than 1 or greater than current stock
def update_cart_item(request):
    if(request.POST.__contains__('product_id') is not True):
        return HttpResponseBadRequest("Product Id is required.")

    if(request.POST.__contains__('quantity') is not True):
        return HttpResponseBadRequest("Quantity is required.")

    quantity = int(request.POST['quantity'])

    return addBasket(request, int(request.POST['product_id']), quantity)

def cart_total(request):
    basket = request.basket
    return HttpResponse(json.dumps({'total': Decimal(basket.total_excl_tax)}, use_decimal=True), mimetype='application/json')

def get_filtered_variant(itemId, post):
    sizeFilter = post['sizeFilter']
    colorFilter = post['colorFilter']

    attributeColor = get_object_or_404(AttributeOption, option=colorFilter.lower())
    if " x " in sizeFilter:
        sizeDim = sizeFilter.split(' x ')
        variant = Product.objects.filter(parent=itemId, attribute_values__value_option_id=attributeColor.id).filter(parent=itemId,
                                                                                                          attribute_values__attribute_id=2,
                                                                                                          attribute_values__value_float=sizeDim[0]).filter(
            parent=itemId, attribute_values__attribute_id=3, attribute_values__value_float=sizeDim[1])[0]
    else:
        try:
            attributeSize = get_object_or_404(AttributeOption, option=sizeFilter.lower())
            variant = Product.objects.filter(parent=itemId, attribute_values__value_option_id=attributeColor.id).filter(parent=itemId, attribute_values__value_option_id=attributeSize.id)[0]
        except Exception as e:
            variant = Product.objects.filter(parent=itemId, attribute_values__value_option_id=attributeColor.id).filter(parent=itemId,
                                                                                                          attribute_values__attribute_id=4,                                                                                                          attribute_values__value_float=float(sizeFilter))[0]
    return variant


def delete_item_to_cart(request):
    cartId = request.POST['Id']
    basketline = Line.objects.get(pk=cartId).delete()
    return HttpResponse(json.dumps({'deleted': True}, {'errors': 'error'}), mimetype='application/json')
