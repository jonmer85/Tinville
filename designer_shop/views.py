import json
import collections
import re
import shutil
import datetime
from django.db import transaction, IntegrityError
from django.http import HttpResponseRedirect
from operator import itemgetter
from functools import wraps
from custom_oscar.apps.catalogue.models import Product
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.core.files.base import ContentFile
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.template.context import RequestContext
import os
from oscar.apps.catalogue.models import ProductAttributeValue as Attributes
from oscar.apps.partner.models import StockRecord as StockRecords
from oscar.apps.catalogue.models import ProductCategory as Categories
from oscar.apps.catalogue.models import Category as Category
from oscar.core.loading import get_model
from designer_shop.models import Shop, SIZE_SET, SIZE_NUM, SIZE_DIM, ONE_SIZE
from designer_shop.forms import ProductCreationForm, AboutBoxForm, DesignerShopColorPicker, BannerUploadForm, \
    LogoUploadForm, ProductImageFormSet, ReturnPolicyForm, SIZE_TYPES_AND_EMPTY
from common.utils import get_list_or_empty, get_or_none
from user.forms import BetaAccessForm
from user.models import TinvilleUser
from common.utils import get_list_or_empty, get_or_none, get_dict_value_or_suspicious_operation,convert_to_currency
from django.views.generic import ListView
from oscar.apps.analytics.scores import Calculator
import logging
from django import forms

AttributeOption = get_model('catalogue', 'AttributeOption')
ProductImage = get_model('catalogue', 'ProductImage')

logger = logging.getLogger(__name__)


class ShopListView(ListView):
    template_name = "shoplist.html"
    model = Shop
    context_object_name = "shop_list"

    def get_queryset(self):
        return Shop.objects.filter(user__is_approved = True)


class IsShopOwnerDecorator(object):
    def __init__(self, view_func):
        self.view_func = view_func
        wraps(view_func)(self)


    def authenticate(self, request, shop_slug, item_slug):
        if request.user.is_authenticated():
            shop = get_object_or_404(Shop, slug__iexact=shop_slug)
            if request.user.id == shop.user_id or request.user.is_staff:
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


class get_filter_lists:
    def __init__(self, shop=None):
        # if one does not pass a shop then is it will only filter through approved user
        if shop:
            self.shop = shop
            self.shop_products = Product.objects.filter(shop_id = shop.id).filter(structure="parent")
        else:
            self.shop_products = Product.objects.filter(structure="parent").filter(shop = Shop.objects.filter(user__is_approved = True))

    def shop_product_categories(self):
        shopProductCategories = set()
        for products in self.shop_products:
            shopProductCategories.add(get_or_none(Categories, product_id=products.id))
        return shopProductCategories

    def categorylist(self):
        shopCategories = set()
        shopCategoryNames = set()
        shopProductCategories = self.shop_product_categories()
        for productcategory in shopProductCategories:
            if productcategory != None:
                currentcategory = get_or_none(Category, id=productcategory.category.id)
                shopCategories.add(currentcategory)
                shopCategoryNames.add(currentcategory.name)
        return shopCategories, shopCategoryNames

    def genderlist(self):
        shopGenders = set()
        categorylist, names = self.categorylist()
        for category in categorylist:
            shopGenders.add(get_or_none(Category, path=category.path[:4]))
        return shopGenders


def shopper(request, slug):
    shop = get_object_or_404(Shop, slug__iexact=slug)

    if not (shop.user.is_approved):
        if(request.user.is_active):
            if(not request.user.slug==shop.user.slug and not request.user.is_staff):
                return HttpResponseRedirect(reverse('under_construction'))
        else:
            return HttpResponseRedirect(reverse('under_construction'))

    if not settings.DISABLE_BETA_ACCESS_CHECK and not check_access_code(request):
        if request.user.is_anonymous() or not request.user.is_seller:
            return HttpResponseRedirect('%s?shop=%s' % (reverse('beta_access'), slug))

    if request.method == 'GET':
        template = 'designer_shop/shopper.html'
        page_template = 'designer_shop/all_gallery.html'
        if request.GET.__contains__('genderfilter'):
            products = get_filtered_products(shop, request.GET, True)
            shopcategorynames = get_types(request=request,shop_slug=slug,group_by=request.GET['genderfilter'])
            return render(request, 'designer_shop/shop_items.html', {
                'shop': shop,
                'products': products,
                'shopProductCount': len(products),
                'shopcategories': shopcategorynames

            })

        products = get_filtered_products(shop)
        shopcategories, shopcategorynames = get_filter_lists(shop).categorylist()


        context = {
            'shop': shop,
            'shopgenders': get_filter_lists(shop).genderlist(),
            'shopcategories': shopcategorynames,
            'products': products,
            'shopProductCount': len(products),
        }
        if request.is_ajax():
            template = page_template
            context = {'products': products}
        return render_to_response(template, context, context_instance=RequestContext(request))


def check_access_code(request):
    if 'beta_access' in request.COOKIES:
        access_id = request.COOKIES['beta_access']
        try:
            TinvilleUser.objects.get(access_code = access_id)
            return True
        except ObjectDoesNotExist:
            return False
    return False

# What what in the butt (Tom Bowman) 6-22-14

def get_filtered_products(shop=None, post=None, filter=None):
    if shop is not None and filter is True:
        genderfilter = get_dict_value_or_suspicious_operation(post, 'genderfilter')
        itemtypefilter = get_dict_value_or_suspicious_operation(post, 'typefilter')
        sortfilter = get_dict_value_or_suspicious_operation(post, 'sortfilter')
        filteredProductList = get_sort_order(Product.objects.filter(
            Q(shop_id=shop.id, parent__isnull=True) & get_valid_categories_for_filter(genderfilter, itemtypefilter)),
                                             sortfilter)
        context = filteredProductList
    elif shop is None and filter is True:
        genderfilter = get_dict_value_or_suspicious_operation(post, 'genderfilter')
        itemtypefilter = get_dict_value_or_suspicious_operation(post, 'typefilter')
        sortfilter = get_dict_value_or_suspicious_operation(post, 'sortfilter')
        filteredProductList = get_sort_order(Product.objects.filter(
            Q(shop = Shop.objects.filter(user__is_approved = True), parent__isnull=True) & get_valid_categories_for_filter(genderfilter, itemtypefilter)),
                                             sortfilter)
        context = filteredProductList
    elif shop is not None:
        context = Product.objects.filter(shop_id = shop.id).filter(structure="parent")
    else:
        context = Product.objects.filter(structure="parent").filter(shop = Shop.objects.filter(user__is_approved = True))
    return context


def get_category_products(shop=None, genderfilter=None, itemtypefilter=None, sortfilter='date-asc'):
    if genderfilter is None:
        genderfilter = "View All"
    if itemtypefilter is None:
        itemtypefilter = "View All Types"
    if shop is None and filter is not None:
        filteredProductList = get_sort_order(Product.objects.filter(
            Q(shop = Shop.objects.filter(user__is_approved = True), parent__isnull=True) & get_valid_categories_for_filter(genderfilter, itemtypefilter)),
                                             sortfilter)
        context = filteredProductList
    else:
        context = Product.objects.filter(structure="parent").filter(shop = Shop.objects.filter(user__is_approved = True))
    return context


def get_valid_categories_for_filter(gender, type):
    filter = list()
    if gender != "View All":
        filter.append(Q(categories__full_name__startswith=gender + ' >'))
    if type != "View All Types":
        filter.append(Q(categories__full_name__contains='> ' + type))
    qs = filter
    if filter != []:
        query = qs.pop()
        for q in qs:
            query &= q
    else:
        query = Q(parent__isnull=True)

    return query


def get_sort_order(filteredobjects, sortfilter):
    if sortfilter == 'date-asc':
        return filteredobjects.order_by('-date_created')
    elif sortfilter == 'date-dsc':
        return filteredobjects.order_by('date_created')
    elif sortfilter == 'price-asc':
        return sorted(filteredobjects, key=lambda i: i.min_child_price_excl_tax)
    elif sortfilter == 'price-dsc':
        return sorted(filteredobjects, key=lambda i: i.min_child_price_excl_tax, reverse=True)
    elif sortfilter == 'pop-asc':
        return sorted(filteredobjects, key=lambda i: sum([j.stats.score if has_stats(j) else 0 for j in get_list_or_empty(Product, parent=i.id)]))
    elif sortfilter == 'pop-dsc':
        return sorted(filteredobjects, key=lambda i: sum([j.stats.score if has_stats(j) else 0 for j in get_list_or_empty(Product, parent=i.id)]), reverse=True)
    else:
        return filteredobjects.order_by('?')


def has_stats(product):
    try:
        product.stats
    except:
        return False
    return True


@IsShopOwnerDecorator
def shopeditor(request, shop_slug):
    return processShopEditorForms(request, shop_slug)


@IsShopOwnerDecoratorUsingItem
def shopeditor_with_item(request, shop_slug, item_slug):
    return processShopEditorForms(request, shop_slug, item_slug)


@IsShopOwnerDecorator
def ajax_color(request, slug):
    if request.method == 'POST':
        currentShop = Shop.objects.get(slug__iexact=slug)
        form = DesignerShopColorPicker(request.POST)

        if request.is_ajax() and form.is_valid():
            currentShop.color = form.cleaned_data["color"]
            currentShop.save(update_fields=["color"])
            return HttpResponse(json.dumps({'errors': form.errors}), content_type='application/json')
        return HttpResponseBadRequest(json.dumps(form.errors), content_type='application/json')
    return HttpResponseBadRequest()


def get_types(request, shop_slug=None, group_by=None):
    shopCategoryNames = get_categoryName(request=request, shop_slug=shop_slug, group_by=group_by)
    types = {'shopCategoryNames': shopCategoryNames}
    return HttpResponse(json.dumps(types), content_type='application/json')


def get_categoryName(request, shop_slug=None, group_by=None):
    shopCategoryNames = []
    if shop_slug is None:
        shopProductCategories = get_filter_lists().shop_product_categories()
    else:
        shop = get_object_or_404(Shop, slug__iexact=shop_slug)
        shopProductCategories = get_filter_lists(shop).shop_product_categories()
    for productcategory in shopProductCategories:
        if productcategory != None:
            currentcategory = get_or_none(Category, id=productcategory.category.id)
            if group_by != "All":
                if currentcategory.full_name.find(group_by) >= 0:
                    if not shopCategoryNames.__contains__(currentcategory.name):
                        shopCategoryNames.append(str(currentcategory.name))
            else:
                if not shopCategoryNames.__contains__(currentcategory.name):
                    shopCategoryNames.append(currentcategory.name)
    return shopCategoryNames


def get_variants(item, group=None):
    variants = get_list_or_empty(Product, parent=item.id)
    sizeType = get_sizetype(variants)

    if group is None:
        colorsizequantitydict = []
    else:
        colorsizequantitydict = collections.defaultdict(list)

    for variant in variants:
        color = ""
        sizeSet = ""
        sizeX = ""
        sizeY = ""
        sizeNum = ""
        divider = ""
        oneSize = ""
        quantity = get_or_none(StockRecords, product_id=variant.id).net_stock_level
        price = str(get_or_none(StockRecords, product_id=variant.id).price_excl_tax)
        currency = get_or_none(StockRecords, product_id=variant.id).price_currency

        if get_or_none(Attributes, product_id=variant.id, attribute_id=5) != None:
            primary_color = get_or_none(Attributes, product_id=variant.id, attribute_id=5).value_as_text
            secondary_color = get_or_none(Attributes, product_id=variant.id, attribute_id=7)
            if secondary_color:
                color = str(primary_color).capitalize() + "/" + str(secondary_color.value_as_text).capitalize()
            else:
                color = str(primary_color).capitalize()

        if get_or_none(Attributes, product_id=variant.id, attribute_id=1) != None:
            sizeSetNum = get_or_none(Attributes, product_id=variant.id, attribute_id=1).value_option_id
            sizeSet = get_or_none(Attributes, product_id=variant.id, attribute_id=1).value_as_text

        if get_or_none(Attributes, product_id=variant.id, attribute_id=2) != None:
            sizeX = get_or_none(Attributes, product_id=variant.id, attribute_id=2).value_as_text

        if get_or_none(Attributes, product_id=variant.id, attribute_id=3) != None:
            sizeY = get_or_none(Attributes, product_id=variant.id, attribute_id=3).value_as_text

        if get_or_none(Attributes, product_id=variant.id, attribute_id=4) != None:
            sizeNum = get_or_none(Attributes, product_id=variant.id, attribute_id=4).value_as_text

        if get_or_none(Attributes, product_id=variant.id, attribute_id=6) != None:
            oneSize = "One Size"

        if sizeX != "" and sizeY != "":
            divider = " x "
        variantsize = str(sizeSet) + str(sizeX) + divider + str(sizeY) + str(sizeNum) + str(oneSize)
        caseFunc = str.capitalize if sizeType != SIZE_SET else str.upper

        if group is None:
            if sizeType == SIZE_SET:
                quantitysize = {'color': color, 'size': caseFunc(variantsize), 'quantity': quantity,
                                'price': price, 'currency': currency, 'sizeorder': sizeSetNum}
            else:
                quantitysize = {'color': color, 'size': caseFunc(variantsize), 'quantity': quantity,
                                'price': price, 'currency': currency}
            colorsizequantitydict.append(quantitysize)
        else:
            if sizeType == SIZE_SET:
                groupdict = {'color': color, 'size': caseFunc(variantsize), 'quantity': quantity,
                             'price': price, 'currency': currency, 'sizeorder': sizeSetNum}
            else:
                groupdict = {'color': color, 'size': caseFunc(variantsize), 'quantity': quantity,
                             'price': price, 'currency': currency}
            mysort = groupdict[group]
            groupdict.pop(group)
            quantitysize = groupdict
            colorsizequantitydict[mysort].append(quantitysize)

            if str(group) == 'color':
                if sizeType == SIZE_SET:
                    colorsizequantitydict[mysort] = sorted(colorsizequantitydict[mysort], key=itemgetter('sizeorder'))
                elif sizeType == SIZE_NUM:
                    colorsizequantitydict[mysort] = sorted(colorsizequantitydict[mysort], key=lambda x: float(x.get('size')))
                elif sizeType == SIZE_DIM:
                    colorsizequantitydict[mysort] = sorted(colorsizequantitydict[mysort], key=lambda x: (float(x.get('size').split('x')[0]), float(x.get('size').split('x')[1])))
                else:
                    colorsizequantitydict[mysort] = sorted(colorsizequantitydict[mysort], key=itemgetter('size'))
            elif group == 'size':
                colorsizequantitydict[mysort] = sorted(colorsizequantitydict[mysort], key=itemgetter('color'))

    if sizeType == SIZE_NUM and group == 'size':
        colorsizequantitydict = collections.OrderedDict(sorted(colorsizequantitydict.items(), key=lambda x: float(x[0])))
    if sizeType == SIZE_DIM and group == 'size':
        colorsizequantitydict = collections.OrderedDict(sorted(colorsizequantitydict.items(), key=lambda x: (float(x[0].split('x')[0]), float(x[0].split('x')[1]))))

    addsizetype = {'sizetype': sizeType, 'variants': colorsizequantitydict,
                   'minprice': get_min_price(item)}
    return json.dumps(addsizetype)


def get_single_variant(variant, group=None):
    if group is None:
        colorsizequantitydict = []
    else:
        colorsizequantitydict = collections.defaultdict(list)

    color = ""
    sizeSet = ""
    isSizeSet = False
    sizeX = ""
    sizeY = ""
    sizeNum = ""
    divider = ""
    oneSize = ""
    quantity = get_or_none(StockRecords, product_id=variant.id).net_stock_level
    price = str(get_or_none(StockRecords, product_id=variant.id).price_excl_tax)
    currency = get_or_none(StockRecords, product_id=variant.id).price_currency

    if get_or_none(Attributes, product_id=variant.id, attribute_id=5) != None:
            primary_color = get_or_none(Attributes, product_id=variant.id, attribute_id=5).value_as_text
            secondary_color = get_or_none(Attributes, product_id=variant.id, attribute_id=7)
            if secondary_color:
                color = str(primary_color).capitalize() + "/" + str(secondary_color.value_as_text).capitalize()
            else:
                color = primary_color

    if get_or_none(Attributes, product_id=variant.id, attribute_id=1) != None:
        sizeSetNum = get_or_none(Attributes, product_id=variant.id, attribute_id=1).value_option_id
        sizeSet = get_or_none(Attributes, product_id=variant.id, attribute_id=1).value_as_text
        isSizeSet = True

    if get_or_none(Attributes, product_id=variant.id, attribute_id=2) != None:
        sizeX = get_or_none(Attributes, product_id=variant.id, attribute_id=2).value_as_text

    if get_or_none(Attributes, product_id=variant.id, attribute_id=3) != None:
        sizeY = get_or_none(Attributes, product_id=variant.id, attribute_id=3).value_as_text

    if get_or_none(Attributes, product_id=variant.id, attribute_id=4) != None:
        sizeNum = get_or_none(Attributes, product_id=variant.id, attribute_id=4).value_as_text

    if get_or_none(Attributes, product_id=variant.id, attribute_id=6) != None:
        oneSize = "One Size"

    if sizeX != "" and sizeY != "":
        divider = " x "
    variantsize = str(sizeSet) + str(sizeX) + divider + str(sizeY) + str(sizeNum) + str(oneSize)
    caseFunc = str.capitalize if not isSizeSet else str.upper

    return str(color).capitalize(), caseFunc(variantsize)


def get_sizetype(variants):
    for variant in variants:
        if hasattr(variant.attr, 'size_set'):
            return SIZE_SET
        elif hasattr(variant.attr, 'size_dimension_x') or hasattr(variant.attr, 'size_dimension_y'):
            return SIZE_DIM
        elif hasattr(variant.attr, 'size_number'):
            return SIZE_NUM
        elif hasattr(variant.attr, 'one_size'):
            return ONE_SIZE
        return "0"


def get_min_price(item):
    return str(convert_to_currency(item.min_child_price_excl_tax))


def get_variants_httpresponse(request, shop_slug, item_slug, group_by=None):
    shop = get_object_or_404(Shop, slug__iexact=shop_slug)
    item = get_object_or_404(Product, slug__iexact=item_slug, shop_id=shop.id, parent__isnull=True)
    # if request.is_ajax():
    return HttpResponse(get_variants(item, group_by), content_type='application/json')


def confirm_at_least_one(i):
    if i == 0:
        raise SuspiciousOperation()  # Should have at least one size


def _populateColorsAndQuantitiesForSize(i, postCopy, prefix, sizes):
    j = 0
    while (True):
        primary_color = next((c for c in postCopy.keys() if prefix + '_pc' in c
                      and "_colorSelection" in c), None)


        colorRowNum = None
        if primary_color:
            m = re.search(r'\d+$', primary_color)
            if m is not None:
                colorRowNum = m.group()

            quantity = next((q for q in postCopy.keys() if prefix + '_' in q
                             and "_quantityField" in q and q.endswith(colorRowNum)), None)
            secondary_color = next((c for c in postCopy.keys() if prefix + '_sc' in c
                            and "_colorSelection" in c and c.endswith(colorRowNum)), None)

        if primary_color is not None and quantity is not None:
            if postCopy[primary_color] and postCopy[quantity]:
                sizes[i]["colorsAndQuantities"].append(
                    {
                        "primary_color": postCopy[primary_color],
                        "secondary_color": postCopy[secondary_color] if secondary_color is not None else None,
                        "colorFieldName": primary_color.replace('_pc_', '_'),
                        "quantity": postCopy[quantity],
                        "quantityFieldName": quantity
                    }
                )
        else:
            confirm_at_least_one(j)
            break
        j += 1
        postCopy.pop(primary_color)
        if secondary_color is not None:
            postCopy.pop(secondary_color)

        #We need to remove original select field as well
        if primary_color.replace('_pc_', '_') in postCopy:
            postCopy.pop(primary_color.replace('_pc_', '_'))
        postCopy.pop(quantity)


def get_sizes_colors_and_quantities(sizeType, post):
    postCopy = post.copy()
    sizes = []
    numSizes = 0
    if sizeType == SIZE_SET:
        while (True):
            # Find a size set, there should be at least one
            set = next((s for s in postCopy.keys() if "sizeSetSelectionTemplate" in s
                        and "_sizeSetSelection" in s), None)
            if set:
                if postCopy[set]:
                    sizes.append(
                        {
                            "sizeSet": postCopy[set],
                            "sizeFieldName": set,
                            "colorsAndQuantities": []
                        }
                    )
                    prefix = set[0:set.find("_")]
                    _populateColorsAndQuantitiesForSize(numSizes, postCopy, prefix, sizes)
                    numSizes += 1
                postCopy.pop(set)
            else:
                confirm_at_least_one(numSizes)
                break
        return sizes

    if sizeType == SIZE_DIM:
        while (True):
            sizeX = next((x for x in postCopy.keys() if "sizeDimensionSelectionTemplate" in x
                                            and "_sizeDimWidth" in x), None)
            sizeY = None
            if sizeX:
                sizeY = sizeX.replace("Width", "Length")

            sizeDimensionSelection = {
                                        "x": sizeX,
                                        "y": sizeY
                                     }
            if sizeDimensionSelection["x"] and sizeDimensionSelection["y"]:
                if postCopy[sizeDimensionSelection["x"]] and postCopy[sizeDimensionSelection["y"]]:
                    sizes.append(
                        {
                            "sizeX": postCopy[sizeDimensionSelection["x"]],
                            "sizeY": postCopy[sizeDimensionSelection["y"]],
                            "sizeFieldNameX": sizeDimensionSelection["x"],
                            "sizeFieldNameY": sizeDimensionSelection["y"],
                            "colorsAndQuantities": []
                        }
                    )
                    prefix = sizeDimensionSelection["x"][0:sizeDimensionSelection["x"].find("_")]
                    _populateColorsAndQuantitiesForSize(numSizes, postCopy, prefix, sizes)
                    numSizes += 1
                postCopy.pop(sizeDimensionSelection["x"])
                postCopy.pop(sizeDimensionSelection["y"])
            else:
                confirm_at_least_one(numSizes)
                break
        return sizes

    if sizeType == SIZE_NUM:
        while (True):
            # Find a size set, there should be at least one
            number = next((n for n in postCopy.keys() if "sizeNumberSelectionTemplate" in n
                        and "_sizeNumberSelection" in n), None)
            if number:
                if postCopy[number]:
                    sizes.append(
                        {
                            "sizeNum": postCopy[number],
                            "sizeFieldName": number,
                            "colorsAndQuantities": []
                        }
                    )
                    prefix = number[0:number.find("_")]
                    _populateColorsAndQuantitiesForSize(numSizes, postCopy, prefix, sizes)
                    numSizes += 1
                postCopy.pop(number)
            else:
                confirm_at_least_one(numSizes)
                break
        return sizes

    if sizeType == ONE_SIZE:
        while (True):
            number = next((n for n in postCopy.keys() if "oneSizeSelectionTemplate" in n and "_oneSizeSelection" in n), None)
            if number:
                if postCopy[number]:
                    sizes.append(
                        {
                            "oneSize": True,
                            "colorsAndQuantities": []
                        }
                    )
                    prefix = number[0:number.find("_")]
                    _populateColorsAndQuantitiesForSize(numSizes, postCopy, prefix, sizes)
                    numSizes += 1
                postCopy.pop(number)
            else:
                confirm_at_least_one(numSizes)
                break
        return sizes


#private method no Auth
def renderShopEditor(request, shop, productCreationForm=None, aboutForm=None, colorPickerForm=None, logoUploadForm=None,
                     returnPolicyForm=None, bannerUploadForm=None, item=None, tab=None, productImageFormSet=None):
    editItem = item is not None
    products = get_filtered_products(shop)
    shopCategories, shopCategoryNames = get_filter_lists(shop).categorylist()
    if not editItem or (editItem and request.is_ajax()):
        template = 'designer_shop/shopeditor.html'
        page_template = 'designer_shop/all_gallery.html'

        context = {
            'editmode': True,
            'shop': shop,
            'productCreationForm': productCreationForm or ProductCreationForm(instance=item if editItem else None, shop=shop),
            'productImageFormSet': productImageFormSet or ProductImageFormSet(instance=item if editItem else None),
            'editItemMode': editItem,
            'bannerUploadForm': bannerUploadForm or BannerUploadForm(instance=shop),
            'logoUploadForm': logoUploadForm or LogoUploadForm(initial=
                                                               {
                                                                   "logo": shop.logo
                                                               }),
            'designerShopColorPicker': colorPickerForm or DesignerShopColorPicker(initial=
                                                                                  {
                                                                                      "color": shop.color
                                                                                  }),
            'aboutBoxForm': aboutForm or AboutBoxForm(instance=shop),
            'returnPolicyForm': returnPolicyForm or ReturnPolicyForm(instance=shop),
            'colors': AttributeOption.objects.filter(group=2),
            'sizeSetOptions': AttributeOption.objects.filter(group=1),
            'shopcategories': shopCategoryNames,
            'shopgenders': get_filter_lists(shop).genderlist(),
            'products': products,
            'shopProductCount': len(products),
            'tab' : tab or 'Default'
        }

        if request.is_ajax() and 'page' in request.GET:
            template = page_template
            context = {'products': products,
                       'editmode': True,
                        'shop': shop,
                        'productCreationForm': productCreationForm or ProductCreationForm(instance=item if editItem else None, shop=shop),
                        'productImageFormSet': productImageFormSet or ProductImageFormSet(instance=item if editItem else None),
                        'editItemMode': editItem
                    }
        return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        return redirect('designer_shop.views.shopeditor', shop.slug)


#private method no Auth
@transaction.atomic
def processShopEditorForms(request, shop_slug, item_slug=None):
    shop = get_object_or_404(Shop, slug__iexact=shop_slug)

    form = None
    item = get_object_or_404(Product, slug__iexact=item_slug, parent__isnull=True) if item_slug else None
    is_create = item is None
    if request.method == 'POST':
        if request.POST.__contains__('bannerUploadForm'):
            form = BannerUploadForm(request.POST, request.FILES, instance=shop)
            if form.is_valid():
                form.save()
                return renderShopEditor(request, shop)
            return renderShopEditor(request, shop, bannerUploadForm=form)
        # Jon M TODO - Put back and cleanup if we support Logo again
        # elif request.POST.__contains__('logoUploadForm'):
        #     form = LogoUploadForm(request.POST, request.FILES)
        #     if form.is_valid():
        #         shutil.rmtree(settings.MEDIA_ROOT + '/shops/{0}/logo'.format(shop.slug), ignore_errors=True)
        #         shop.logo = form.cleaned_data["logo"]
        #         shop.save(update_fields=["logo"])
        #     return renderShopEditor(request, shop, logoUploadForm=form)
        elif request.POST.__contains__('aboutBoxForm'):
            form = AboutBoxForm(request.POST, request.FILES, instance=shop)
            if form.is_valid():
                form.save()
                return renderShopEditor(request, shop, tab='about')
            return renderShopEditor(request, shop, aboutForm=form)
        elif request.POST.__contains__('returnPolicyForm'):
            form = ReturnPolicyForm(request.POST, instance=shop)
            if form.is_valid():
                form.save()
                return renderShopEditor(request, shop, tab='returnPolicy')
            return renderShopEditor(request, shop, returnPolicyForm=form)
        elif request.GET.__contains__('genderfilter'):
            products = get_filtered_products(shop, request.GET, True)
            return render(request, 'designer_shop/shop_items.html', {
                'shop': shop,
                'products': products,
                'shopProductCount': len(products),
            })
        else:
            sizeVariationType = get_dict_value_or_suspicious_operation(request.POST, "sizeVariation")
            sizes = get_sizes_colors_and_quantities(sizeVariationType, request.POST)

            if is_create:
                form = ProductCreationForm(request.POST, request.FILES, sizes=sizes, shop=shop)
            else:
                form = ProductCreationForm(request.POST, request.FILES, instance=item if item else None,
                                           sizes=sizes, shop=shop)
            if not _valid_variants(sizes):
                form.add_error(None, "Duplicate size or color detected, please delete duplicates")

            if form.is_valid():
                try:
                    with transaction.atomic():
                        canonicalProduct = form.save(shop, sizes, sizeVariationType)
                        image_formset = ProductImageFormSet(request.POST, request.FILES, instance=canonicalProduct)

                        if image_formset.is_valid():
                            image_formset.save()
                            messages.success(request,
                                         ("Item has been successfully {0}!").format("created" if is_create else "updated"))
                            return renderShopEditor(request, shop, item=item)
                        else:
                            raise IntegrityError("Image error")
                except IntegrityError as e:
                    form.data['sizeVariation'] = SIZE_TYPES_AND_EMPTY[0]
                    messages.error(request, "There was a problem uploading your image(s). Please try a different image(s).")
                    logger.warning("Invalid image formset - Exception: %s" % str(e))
                    image_formset = ProductImageFormSet(instance=item if item else None)
            else:
                form.data['sizeVariation'] = SIZE_TYPES_AND_EMPTY[0]
                image_formset = ProductImageFormSet(instance=item if item else None)
            return renderShopEditor(request, shop, productCreationForm=form, item=item, productImageFormSet=image_formset)
    else:
        return renderShopEditor(request, shop, item=item)


def _valid_variants(variants):
    if 'sizeSet' in variants[0]:
        if len([v['sizeSet'] for v in variants]) != len(set(v['sizeSet'] for v in variants)):
            return False

    if 'sizeNum' in variants[0]:
        if len([v['sizeNum'].rstrip('0').rstrip('.') if '.' in v['sizeNum'] else v['sizeNum'] for v in variants]) != \
                len(set(v['sizeNum'].rstrip('0').rstrip('.') if '.' in v['sizeNum'] else v['sizeNum'] for v in variants)):
            return False

    if 'sizeX' in variants[0]:
        if len([v['sizeX'].rstrip('0').rstrip('.') if '.' in v['sizeX'] else v['sizeX'] + 'x' + v['sizeY'].rstrip('0').rstrip('.') if '.' in v['sizeY'] else v['sizeY'] for v in variants]) != \
                len(set(v['sizeX'].rstrip('0').rstrip('.') if '.' in v['sizeX'] else v['sizeX'] + 'x' + v['sizeY'].rstrip('0').rstrip('.') if '.' in v['sizeY'] else v['sizeY'] for v in variants)):
            return False

    for variant in variants:
        colors = variant['colorsAndQuantities']
        if len([str(c['primary_color']) + '/' + str(c['secondary_color']) for c in colors]) != len(set(str(c['primary_color']) + '/' + str(c['secondary_color']) for c in colors)):
            return False

    return True


def _replaceCroppedFile(form, file_field, file_name, cropped_field_name):
    if not form.cleaned_data[file_field.field.attname]:
        # False means that the clear checkbox was checked
        if file_field is not None:
            file_field.delete()
        return True
    else:
        if form.cleaned_data[cropped_field_name] and len(form.cleaned_data[cropped_field_name]) > 0:
            file_field.save(file_name, ContentFile(form.cleaned_data[cropped_field_name].decode("base64")))
            return True
        return False


@IsShopOwnerDecoratorUsingItem
def delete_product(request, shop_slug, item_slug):
    item = get_object_or_404(Product, slug__iexact=item_slug, parent__isnull=True)
    product = Product.objects.get(pk=item.id).delete()
    return redirect('designer_shop.views.shopeditor', shop_slug)