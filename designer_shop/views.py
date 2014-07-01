import json
import collections
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.db import models
from oscar.apps.catalogue.models import ProductAttributeValue as Attributes
from oscar.apps.partner.models import StockRecord as StockRecords


from oscar.core.loading import get_model
from designer_shop.models import Shop, SIZE_SET, SIZE_NUM, SIZE_DIM
from designer_shop.forms import ProductCreationForm, AboutBoxForm, DesignerShopColorPicker, BannerUploadForm, \
    LogoUploadForm
from catalogue.models import Product

from common.utils import get_list_or_empty, get_or_none
from functools import wraps

AttributeOption = get_model('catalogue', 'AttributeOption')

class IsShopOwnerDecorator(object):
    def __init__(self, view_func):
        self.view_func = view_func
        wraps(view_func)(self)


    def authenticate(self, request, shop_slug, item_slug):
        if request.user.is_authenticated():
            shop = get_object_or_404(Shop, slug__iexact=shop_slug)
            if request.user.id == shop.user_id:
                response = self.view_func(request, shop_slug) \
                    if not item_slug else self.view_func(request, shop_slug, item_slug)
                return response
            else:
                return redirect('home')
        else:
            return redirect('home')

    def __call__(self, request, shop_slug):
        return self.authenticate(request, shop_slug, None)



class IsShopOwnerDecoratorUsingItem(IsShopOwnerDecorator):

    def __call__(self, request, shop_slug, item_slug):
        return self.authenticate(request, shop_slug, item_slug)




def shopper(request, slug):
    shop = get_object_or_404(Shop, slug__iexact=slug)
    return render(request, 'designer_shop/shopper.html', {
        'shop': shop,
        'categories': get_model('catalogue', 'Category').objects.all(),
        'products': get_list_or_empty(Product, shop=shop.id)
        # 'categories': get_object_or_404(get_model('catalogue', 'AbstrastCategory')).objects.all()
    })

def itemdetail(request, shop_slug, item_slug=None):
    shop = get_object_or_404(Shop, slug__iexact=shop_slug)
    item = get_object_or_404(Product, slug__iexact=item_slug, shop_id=shop.id, parent__isnull=True)
    variants = get_list_or_empty(Product, parent=item.id)
    colorlist = []
    for variant in variants:
        colorattribute = get_or_none(Attributes, product_id=variant.id, attribute_id=5)
        colorlist.append(colorattribute.value_as_text)
    colorset = set(colorlist)

    colorsizequantity = get_variants(item)

    return render(request, 'designer_shop/itemdetail.html', {
        'shop': shop,
        'item': item,
        'variants': variants,
        'validcolors': colorset,
        'colorsizequantity': colorsizequantity,
        # What what in the butt (Tom Bowman) 6-22-14
    })

@IsShopOwnerDecorator
def shopeditor(request, shop_slug):
    return processShopEditorForms(request, shop_slug)

@IsShopOwnerDecoratorUsingItem
def shopeditor_with_item(request, shop_slug, item_slug):
    return processShopEditorForms(request, shop_slug, item_slug)

@IsShopOwnerDecorator
def ajax_about(request, slug):
        if request.method == 'POST':
            form = AboutBoxForm(request.POST)
            currentshop = Shop.objects.get(slug__iexact=slug)
            if request.is_ajax() and form.is_valid():
                currentshop.aboutContent = form.cleaned_data["aboutContent"]
                currentshop.save(update_fields=["aboutContent"])
                return HttpResponse(json.dumps({'errors': form.errors}), mimetype='application/json')
        return HttpResponseBadRequest(json.dumps(form.errors), mimetype="application/json")

@IsShopOwnerDecorator
def ajax_color(request, slug):
        if request.method == 'POST':
            currentShop = Shop.objects.get(slug__iexact=slug)
            form = DesignerShopColorPicker(request.POST)

            if request.is_ajax() and form.is_valid():
                currentShop.color = form.cleaned_data["color"]
                currentShop.save(update_fields=["color"])
                return HttpResponse(json.dumps({'errors': form.errors}), mimetype='application/json')

        return HttpResponseBadRequest(json.dumps(form.errors), mimetype="application/json")

def get_variants(item):
    variants = get_list_or_empty(Product, parent=item.id)
    colorsizequantitydict = collections.defaultdict(list)
    addsizetype = collections.defaultdict(dict)
    for variant in variants:
        color = ""
        sizeSet = ""
        sizeX = ""
        sizeY = ""
        sizeNum = ""
        divider = ""
        quantity = get_or_none(StockRecords, product_id=variant.id).net_stock_level
        price = str(get_or_none(StockRecords, product_id=variant.id).price_excl_tax)
        currency = get_or_none(StockRecords, product_id=variant.id).price_currency

        if get_or_none(Attributes, product_id=variant.id, attribute_id=5) != None:
            color = get_or_none(Attributes, product_id=variant.id, attribute_id=5).value_as_text

        if get_or_none(Attributes, product_id=variant.id, attribute_id=1) != None:
            sizeSet = get_or_none(Attributes, product_id=variant.id, attribute_id=1).value_as_text

        if get_or_none(Attributes, product_id=variant.id, attribute_id=2) != None:
            sizeX = get_or_none(Attributes, product_id=variant.id, attribute_id=2).value_as_text

        if get_or_none(Attributes, product_id=variant.id, attribute_id=3) != None:
            sizeY = get_or_none(Attributes, product_id=variant.id, attribute_id=3).value_as_text

        if get_or_none(Attributes, product_id=variant.id, attribute_id=4) != None:
            sizeNum = get_or_none(Attributes, product_id=variant.id, attribute_id=4).value_as_text

        if sizeX != "" and sizeY != "":
            divider = " x "
        variantsize = str(sizeSet) + str(sizeX) + divider + str(sizeY) + str(sizeNum)
        quantitysize = {'size': variantsize.capitalize(), 'quantity': quantity, 'price': price, 'currency': currency}
        colorsizequantitydict[str(color).capitalize()].append(quantitysize)
    addsizetype= {get_sizetype(variants): colorsizequantitydict }
    return json.dumps(addsizetype)

def get_sizetype(variants):
    for variant in variants:
       if hasattr(variant.attr, 'size_set'):
           return SIZE_SET
       elif hasattr(variant.attr, 'size_dimension_x') or hasattr(variant.attr, 'size_dimension_y'):
           return SIZE_DIM
       elif hasattr(variant.attr, 'size_number'):
           return SIZE_NUM
       return "0"


def get_variants_httpresponse(request, shop_slug, item_slug):
    shop = get_object_or_404(Shop, slug__iexact=shop_slug)
    item = get_object_or_404(Product, slug__iexact=item_slug, shop_id=shop.id, parent__isnull=True)
    return HttpResponse(get_variants(item), mimetype='application/json')

def get_sizes_colors_and_quantities(sizeType, post):
    if sizeType == SIZE_SET:
        sizes = {}
        i = 0
        while (True):
            sizeSetTemplate = "sizeSetSelectionTemplate" + str(i)
            sizeSetSelection = sizeSetTemplate + "_sizeSetSelection"
            if sizeSetSelection in post and post[sizeSetSelection]:
                sizes[i] = {
                    "sizeSet": post[sizeSetSelection],
                    "colorsAndQuantities": []
                }

                j = 0
                while (True):
                    color = sizeSetTemplate + "_colorSelection" + str(j)
                    quantity = sizeSetTemplate + "_quantityField" + str(j)
                    if color in post and quantity in post:
                        if post[color] and post[quantity]:
                            sizes[i]["colorsAndQuantities"].append({"color": post[color], "quantity": post[quantity]})
                    else:
                        break
                    j += 1
                i += 1
            else:
                break
        return sizes

    if sizeType == SIZE_DIM:
        sizes = {}
        i=0
        while (True):
            sizeDimensionTemplate = "sizeDimensionSelectionTemplate" + str(i)
            sizeDimensionSelection = {"x": sizeDimensionTemplate + "_sizeDimWidth", "y": sizeDimensionTemplate + "_sizeDimLength"}
            if sizeDimensionSelection["x"] in post and sizeDimensionSelection["y"] in post:
                sizes[i] = {
                    "sizeX": post[sizeDimensionSelection["x"]],
                    "sizeY": post[sizeDimensionSelection["y"]],
                    "colorsAndQuantities": []
                }

                j = 0
                while (True):
                    color = sizeDimensionTemplate + "_colorSelection" + str(j)
                    quantity = sizeDimensionTemplate + "_quantityField" + str(j)
                    if color in post and quantity in post:
                        if post[color] and post[quantity]:
                            sizes[i]["colorsAndQuantities"].append({"color": post[color], "quantity": post[quantity]})
                    else:
                        break
                    j += 1
                i += 1
            else:
                break
        return sizes

    if sizeType == SIZE_NUM:
        sizes = {}
        i = 0
        while (True):
            sizeNumberTemplate = "sizeNumberSelectionTemplate" + str(i)
            sizeNumberSelection = sizeNumberTemplate + "_sizeNumberSelection"
            if sizeNumberSelection in post:
                sizes[i] = {
                    "sizeNum": post[sizeNumberSelection],
                    "colorsAndQuantities": []
                }

                j = 0
                while (True):
                    color = sizeNumberTemplate + "_colorSelection" + str(j)
                    quantity = sizeNumberTemplate + "_quantityField" + str(j)
                    if color in post and quantity in post:
                        if post[color] and post[quantity]:
                            sizes[i]["colorsAndQuantities"].append({"color": post[color], "quantity": post[quantity]})
                    else:
                        break
                    j += 1
                i += 1
            else:
                break
        return sizes

#private method no Auth
def renderShopEditor(request, shop, productCreationForm=None, aboutForm=None, colorPickerForm=None, logoUploadForm=None,
                     bannerUploadForm=None, item=None):
        editItem = item is not None
        return render(request, 'designer_shop/shopeditor.html', {
        'shop': shop,
        'productCreationForm': productCreationForm or ProductCreationForm(instance=item if editItem else None),
        'editItemMode': editItem,
        'bannerUploadForm': bannerUploadForm or BannerUploadForm(initial=
                                                                 {
                                                                     "banner": shop.banner
                                                                 }),
        'logoUploadForm': logoUploadForm or LogoUploadForm(initial=
                                                           {
                                                               "logo": shop.logo
                                                           }),
        'designerShopColorPicker': colorPickerForm or DesignerShopColorPicker(initial=
                                                                              {
                                                                                  "color": shop.color
                                                                              }),
        'aboutBoxForm': aboutForm or AboutBoxForm(initial=
                                                  {
                                                      "aboutContent": shop.aboutContent
                                                  }),
        'colors': AttributeOption.objects.filter(group=2),
        'sizeSetOptions': AttributeOption.objects.filter(group=1),
        'categories': get_model('catalogue', 'Category').objects.all(),
        'products': get_list_or_empty(Product, shop=shop.id)
    })

#private method no Auth
def processShopEditorForms(request, shop_slug, item_slug=None):
    shop = get_object_or_404(Shop, slug__iexact=shop_slug)

    form = None
    if request.method == 'POST':
        if request.POST.__contains__('bannerUploadForm'):
            form = BannerUploadForm(request.POST, request.FILES)
            if form.is_valid():
                shop.banner = form.cleaned_data["banner"]
                shop.save(update_fields=["banner"])
            return renderShopEditor(request, shop, bannerUploadForm=form)
        elif request.POST.__contains__('logoUploadForm'):
            form = LogoUploadForm(request.POST, request.FILES)
            if form.is_valid():
                shop.logo = form.cleaned_data["logo"]
                shop.save(update_fields=["logo"])
            return renderShopEditor(request, shop, logoUploadForm=form)
        else:
            if request.method == 'POST':
                sizeVariationType = request.POST["sizeVariation"]
                sizes = get_sizes_colors_and_quantities(sizeVariationType, request.POST)
                form = ProductCreationForm(request.POST, request.FILES, sizes=sizes)
                if form.is_valid():
                    canonicalProduct = form.save(shop)
                    form = ProductCreationForm()
            return renderShopEditor(request, shop, productCreationForm=form)
    else:
        return renderShopEditor(request, shop, item=get_object_or_404(Product, slug__iexact=item_slug, parent__isnull=True) if item_slug else None)

