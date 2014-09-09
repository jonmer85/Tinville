import json
import collections

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
from designer_shop.models import Shop
from catalogue.models import Product
from oscar.apps.basket.models import Basket
from oscar.apps.basket.models import Line

from oscar.apps.partner import strategy
from common.utils import get_list_or_empty, get_or_none
from django.utils.html import strip_tags

# Create your views here.
def load_cart(request):
    if request.method == 'POST':
        cartItems = []
        if not request.user.id is None:
            index = 0
            ret = request.POST
            if int(ret['cartLoaded']) == 0:
                basket = get_object_or_404(Basket, owner_id=request.user.id)
                basketlines = get_list_or_empty(Line, basket_id=basket)
                if len(basketlines) > 0:
                    for basketline in basketlines:
                        if checkLineId(ret['Id'],basketline.id):
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
                                        'msg': '',
                                        'cartLoaded': 1}
                            cartItems.append(cartInfo)
            if not str(ret['product_id'])=='':
                product_ids = ret['product_id'].split(',')
                Ids = ret['Id'].split(',')
                qtys = ret['qty'].split(',')
                for product_id in product_ids:
                    if int(Ids[index]) < 0:
                        cartItems.append(addBasket(request,product_id, int(qtys[index])))
                    index = index + 1
            else:
                cartInfo = {'Id': 0, 'msg': ''}
                cartItems.append(cartInfo)
        else:
            cartInfo = {'Id': 0, 'msg': ''}
            cartItems.append(cartInfo)
        return HttpResponse(json.dumps(cartItems), mimetype='application/json')


def checkLineId(Ids, basketlineId):
    if not str(Ids) == '':
        ids = Ids.split(',')
        for id in ids:
            if id < 0:
                return True
            if id == basketlineId:
                return False
    else:
        return True


def addBasket(request, product_id, qty):
        msg = ''
        # ToDo figure out this tax stuff
        tax = 1
        stockrecord = get_object_or_404(StockRecords, product_id=product_id)
        currentproduct = get_object_or_404(Product, id=product_id)
        parentproduct = get_object_or_404(Product, id=currentproduct.parent_id)
        price_excl_tax = stockrecord.price_excl_tax * qty
        price_incl_tax = (stockrecord.price_excl_tax * qty) * tax
        image = get_list_or_empty(ProductImages, product_id=parentproduct.id)
        if not request.user.id is None:
            basket = get_object_or_404(Basket, owner_id=request.user.id)
            if not basket.has_strategy:
                basket._set_strategy(strategy)
            line_quantity = basket.line_quantity(product=currentproduct, stockrecord=stockrecord)
            line_ref=basket._create_line_reference(product=currentproduct, stockrecord=stockrecord, options=None)
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
                    'product_id': currentproduct.id,
                    'title': currentproduct.title,
                    'description': strip_tags(parentproduct.description),
                    'price': float(price_excl_tax),
                    'image': str(image[0].original),
                    'qty': qty,
                    'msg': msg,
                    'cartLoaded': 0}
        return cartInfo


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
        cartInfo = addBasket(request,currentproduct.id,qty)
        return HttpResponse(json.dumps(cartInfo), mimetype='application/json')
    else:
        return redirect('designer_shop.views.itemdetail', shop_slug, item_slug)


def get_filtered_variant(itemId, post):
    sizeFilter = post['sizeFilter']
    colorFilter = post['colorFilter']
    attributeColor = get_object_or_404(AttributeOption, option=colorFilter.lower())
    attributeSize = get_object_or_404(AttributeOption, option=sizeFilter.lower())
    variant = get_object_or_404(Product, parent=itemId, attribute_values__value_option_id=attributeColor.id & attributeSize.id)
    return variant


def delete_item_to_cart(request):
    cartId = request.POST['Id']
    basketline = Line.objects.get(pk=cartId).delete()
    return HttpResponse(json.dumps({'deleted': True}, {'errors': 'error'}), mimetype='application/json')
