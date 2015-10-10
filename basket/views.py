import json
import collections
from decimal import Decimal
from easy_thumbnails.files import get_thumbnailer
import simplejson as json
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.db import models
from oscar.apps.catalogue.models import ProductAttributeValue as Attributes
from custom_oscar.apps.catalogue.models import AttributeOption
# from oscar.apps.catalogue.models import AttributeOption
from oscar.apps.partner.models import StockRecord as StockRecords
from common.utils import get_list_or_empty, get_or_none
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages
from operator import itemgetter, attrgetter


from oscar.core.loading import get_model
from oscar.core.loading import get_class
from designer_shop.models import Shop

from oscar.apps.partner import strategy
from common.utils import get_list_or_empty, convert_to_currency
from django.utils.html import strip_tags
from oscar.apps.basket import signals
from designer_shop.views import get_single_variant

Basket = get_model('basket', 'basket')
Product = get_model('catalogue', 'product')
Line = get_model('basket', 'line')
Selector = get_class('partner.strategy', 'Selector')
ProductImages = get_model("catalogue", "ProductImage")

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
                price_excl_tax = convert_to_currency(basketline.price_excl_tax)
                cartInfo = cartInfoJson(basket, basketline, currentproduct, parentproduct, stockrecord, basketline.quantity, image)
                cartItems.append(cartInfo)

        return HttpResponse(json.dumps(sorted(cartItems, key=lambda k: k['shop'])), content_type='application/json')

def cartInfoJson(basket, basketline, currentproduct, parentproduct, stockrecord, qty, image):
    color, size = get_single_variant(currentproduct)
    return {'Id': basketline.id,
                'product_id': currentproduct.id,
                'title': currentproduct.title,
                'description': strip_tags(parentproduct.description),
                'price': convert_to_currency(stockrecord.price_excl_tax),
                'subtotal': convert_to_currency(stockrecord.price_excl_tax * qty),
                'image': str(get_thumbnailer(image[0].original).get_thumbnail({
                            'size': (400, 400),
                            'box': image[0].cropping,
                            'crop': True,
                            'detail': True,
                            })),
                'qty': qty,
                'color': color,
                'size': size,
                'currentStock' : stockrecord.num_in_stock,
                'total' : convert_to_currency(basket.total_excl_tax),
                'shop' : currentproduct.shop.name,
                'shopSlug' : currentproduct.shop.slug,
                'msg': ''}

def addBasket(request, product_id, qty):
    # ToDo figure out this tax stuff
    tax = 1
    stockrecord = get_object_or_404(StockRecords, product_id=product_id)
    if(qty > stockrecord.num_in_stock):
        errorMsg = "Quantity is greater than {0}.".format(stockrecord.num_in_stock)
        return HttpResponseBadRequest(json.dumps({'errors': errorMsg}), content_type='application/json')
    if(qty < 1):
        return HttpResponseBadRequest(json.dumps({'errors': "Quantity cannot be less than 1."}), content_type='application/json')

    currentproduct = get_object_or_404(Product, id=product_id)
    parentproduct = get_object_or_404(Product, id=currentproduct.parent_id)
    price_excl_tax = convert_to_currency(stockrecord.price_excl_tax * qty)
    price_incl_tax = convert_to_currency((stockrecord.price_excl_tax * qty) * tax)
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

    cartInfo = cartInfoJson(basket, basketline, currentproduct, parentproduct, stockrecord, qty, image)

    return HttpResponse(json.dumps(cartInfo, use_decimal=True), content_type='application/json')


def add_item_to_cart(request, shop_slug, item_slug):

    if request.method == 'POST':
        shop = get_object_or_404(Shop, slug__iexact=shop_slug)
        item = get_object_or_404(Product, slug__iexact=item_slug, shop_id=shop.id, parent__isnull=True)
        #this is getting all the variants and need to get the that info from the page
        variants = get_list_or_empty(Product, parent=item.id)
        qty = int(request.POST['qtyFilter'])
        msg = ''
        if request.POST['colorFilter'] == '':
            return HttpResponseBadRequest(json.dumps({'errors': 'Please select a color!'}), content_type='application/json')
        if request.POST['sizeFilter'] == '':
            return HttpResponseBadRequest(json.dumps({'errors': 'Please select a size!'}), content_type='application/json')
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
    if(not 'product_id' in request.POST):
        return HttpResponseBadRequest(json.dumps({'errors':'Product Id is required.'}), content_type='application/json')

    if(not 'quantity' in request.POST):
        return HttpResponseBadRequest(json.dumps({'errors':'Quantity is required.'}), content_type='application/json')

    quantity = int(request.POST['quantity'])

    return addBasket(request, int(request.POST['product_id']), quantity)

# Purpose: Get cart total
def cart_total(request):
    basket = request.basket
    return HttpResponse(json.dumps({'total': convert_to_currency(basket.total_excl_tax)}, use_decimal=True), content_type='application/json')

def total_cart_items(request):
    basket = request.basket
    return HttpResponse(json.dumps({'count': basket.num_lines}), content_type='application/json')

def get_filtered_variant(itemId, post):
    sizeFilter = post['sizeFilter']
    colorFilter = post['colorFilter']

    if "/" in colorFilter:
        colors = colorFilter.split('/')
        primary_color = get_or_none(AttributeOption, option=colors[0].lower())
        secondary_color = get_or_none(AttributeOption, option=colors[1].lower())
        color_variants = Product.objects.filter(parent=itemId, attribute_values__attribute_id=5, attribute_values__value_option=primary_color.id)\
            .filter(parent=itemId, attribute_values__attribute_id=7, attribute_values__value_option=secondary_color.id)
    else:
        primary_color = get_or_none(AttributeOption, option=colorFilter.lower())
        color_variants = Product.objects.filter(parent=itemId, attribute_values__attribute_id=5, attribute_values__value_option=primary_color)

    if " x " in sizeFilter:
        sizeDim = sizeFilter.split(' x ')
        variant = color_variants.filter(parent=itemId,attribute_values__attribute_id=2,attribute_values__value_float=sizeDim[0]).filter(
            parent=itemId, attribute_values__attribute_id=3, attribute_values__value_float=sizeDim[1])[0]
    elif sizeFilter == "One size":
        variant = color_variants[0]
    else:
        try:
            attributeSize = get_object_or_404(AttributeOption, option=sizeFilter.lower())
            variant = color_variants.filter(parent=itemId, attribute_values__value_option_id=attributeSize.id)[0]
        except Exception as e:
            variant = color_variants.filter(parent=itemId, attribute_values__attribute_id=4,                                                                                                          attribute_values__value_float=float(sizeFilter))[0]
    return variant


def delete_item_to_cart(request):
    cartId = request.POST['Id']
    basketline = Line.objects.get(pk=cartId).delete()
    return HttpResponse(json.dumps({'deleted': True}, {'errors': 'error'}), content_type='application/json')
