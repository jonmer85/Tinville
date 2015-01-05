import json
import collections
import shutil
from operator import itemgetter
from functools import wraps
from custom_oscar.apps.catalogue.models import Product
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.core.files.base import ContentFile

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
import os

from oscar.apps.catalogue.models import ProductAttributeValue as Attributes
from oscar.apps.partner.models import StockRecord as StockRecords
from oscar.apps.catalogue.models import ProductCategory as Categories
from oscar.apps.catalogue.models import ProductImage as ProductImages
from oscar.apps.catalogue.models import Category as Category
from oscar.core.loading import get_model

from designer_shop.models import Shop, SIZE_SET, SIZE_NUM, SIZE_DIM
from designer_shop.forms import ProductCreationForm, AboutBoxForm, DesignerShopColorPicker, BannerUploadForm, \
    LogoUploadForm

from common.utils import get_list_or_empty, get_or_none, get_dict_value_or_suspicious_operation

from django.views.generic import ListView

AttributeOption = get_model('catalogue', 'AttributeOption')

class ShopListView(ListView):
    template_name = "shoplist.html"
    model = Shop
    context_object_name = "shop_list"


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


class get_filter_lists:
    def __init__(self, shop):
        self.shop = shop
        self.shop_products = get_list_or_empty(Product, shop_id=shop.id, parent__isnull=True)

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
    products = get_list_or_empty(Product, shop=shop.id)
    if request.method == 'POST':
        if request.POST.__contains__('genderfilter'):
            return render(request, 'designer_shop/shop_items.html', {
                'shop': shop,
                'products': get_filtered_products(shop, request.POST),
                'shopProductCount': len(products)
            })

    if request.method == 'GET':
        shopcategories, shopcategorynames = get_filter_lists(shop).categorylist()
        return render(request, 'designer_shop/shopper.html', {
            'shop': shop,
            'shopgenders': get_filter_lists(shop).genderlist(),
            'shopcategories': shopcategorynames,
            'products': products,
            'shopProductCount': len(products)
        })


def itemdetail(request, shop_slug, item_slug=None):
    shop = get_object_or_404(Shop, slug__iexact=shop_slug)
    item = get_object_or_404(Product, slug__iexact=item_slug, shop_id=shop.id, parent__isnull=True)
    variants = get_list_or_empty(Product, parent=item.id)
    images = get_list_or_empty(ProductImages, product_id=item.id)
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
        'images': images,
        # What what in the butt (Tom Bowman) 6-22-14
    })


def get_filtered_products(shop, post):
    genderfilter = get_dict_value_or_suspicious_operation(post, 'genderfilter')
    itemtypefilter = get_dict_value_or_suspicious_operation(post, 'typefilter')
    sortfilter = get_dict_value_or_suspicious_operation(post, 'sortfilter')
    filteredProductList = get_sort_order(Product.objects.filter(
        Q(shop_id=shop.id, parent__isnull=True) & get_valid_categories_for_filter(genderfilter, itemtypefilter)),
                                         sortfilter)
    return filteredProductList


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
        return filteredobjects.order_by('?')
    elif sortfilter == 'pop-dsc':
        return filteredobjects.order_by('?')
    else:
        return filteredobjects.order_by('?')


@IsShopOwnerDecorator
def shopeditor(request, shop_slug):
    return processShopEditorForms(request, shop_slug)


@IsShopOwnerDecoratorUsingItem
def shopeditor_with_item(request, shop_slug, item_slug):
    return processShopEditorForms(request, shop_slug, item_slug)


# @IsShopOwnerDecorator
# def about(request, slug):
# if request.method == 'POST':
#             form = AboutBoxForm(request.POST)
#             currentshop = Shop.objects.get(slug__iexact=slug)
#             if request.is_ajax() and form.is_valid():
#                 currentshop.aboutContent = form.cleaned_data["aboutContent"]
#                 currentshop.save(update_fields=["aboutContent"])
#                 return HttpResponse(json.dumps({'errors': form.errors}), mimetype='application/json')
#         return HttpResponseBadRequest(json.dumps(form.errors), mimetype="application/json")

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


def get_types(request, shop_slug, group_by=None):
    shop = get_object_or_404(Shop, slug__iexact=shop_slug)
    shopCategoryNames = []
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
    types = {'types': shopCategoryNames}
    return HttpResponse(json.dumps(types), content_type='application/json')


def get_variants(item, group=None):
    variants = get_list_or_empty(Product, parent=item.id)

    if group is None:
        colorsizequantitydict = []
    else:
        colorsizequantitydict = collections.defaultdict(list)

    for variant in variants:
        color = ""
        sizeSet = ""
        isSizeSet = False
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
            sizeSetNum = get_or_none(Attributes, product_id=variant.id, attribute_id=1).value_option_id
            sizeSet = get_or_none(Attributes, product_id=variant.id, attribute_id=1).value_as_text
            isSizeSet = True

        if get_or_none(Attributes, product_id=variant.id, attribute_id=2) != None:
            sizeX = get_or_none(Attributes, product_id=variant.id, attribute_id=2).value_as_text

        if get_or_none(Attributes, product_id=variant.id, attribute_id=3) != None:
            sizeY = get_or_none(Attributes, product_id=variant.id, attribute_id=3).value_as_text

        if get_or_none(Attributes, product_id=variant.id, attribute_id=4) != None:
            sizeNum = get_or_none(Attributes, product_id=variant.id, attribute_id=4).value_as_text

        if sizeX != "" and sizeY != "":
            divider = " x "
        variantsize = str(sizeSet) + str(sizeX) + divider + str(sizeY) + str(sizeNum)
        caseFunc = str.capitalize if not isSizeSet else str.upper

        if group is None:
            if isSizeSet == True:
                quantitysize = {'color': str(color).capitalize(), 'size': caseFunc(variantsize), 'quantity': quantity,
                                'price': price, 'currency': currency, 'sizeorder': sizeSetNum}
            else:
                quantitysize = {'color': str(color).capitalize(), 'size': caseFunc(variantsize), 'quantity': quantity,
                                'price': price, 'currency': currency}
            colorsizequantitydict.append(quantitysize)
        else:
            if isSizeSet == True:
                groupdict = {'color': str(color).capitalize(), 'size': caseFunc(variantsize), 'quantity': quantity,
                             'price': price, 'currency': currency, 'sizeorder': sizeSetNum}
            else:
                groupdict = {'color': str(color).capitalize(), 'size': caseFunc(variantsize), 'quantity': quantity,
                             'price': price, 'currency': currency}
            mysort = groupdict[group]
            groupdict.pop(group)
            quantitysize = groupdict
            colorsizequantitydict[mysort].append(quantitysize)
            if str(group) == 'color':
                if isSizeSet == True:
                    colorsizequantitydict[mysort] = sorted(colorsizequantitydict[mysort], key=itemgetter('sizeorder'))
                else:
                    colorsizequantitydict[mysort] = sorted(colorsizequantitydict[mysort], key=itemgetter('size'))
            elif group == 'size':
                colorsizequantitydict[mysort] = sorted(colorsizequantitydict[mysort], key=itemgetter('color'))

    addsizetype = {'sizetype': get_sizetype(variants), 'variants': colorsizequantitydict,
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
    quantity = get_or_none(StockRecords, product_id=variant.id).net_stock_level
    price = str(get_or_none(StockRecords, product_id=variant.id).price_excl_tax)
    currency = get_or_none(StockRecords, product_id=variant.id).price_currency

    if get_or_none(Attributes, product_id=variant.id, attribute_id=5) != None:
        color = get_or_none(Attributes, product_id=variant.id, attribute_id=5).value_as_text

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

    if sizeX != "" and sizeY != "":
        divider = " x "
    variantsize = str(sizeSet) + str(sizeX) + divider + str(sizeY) + str(sizeNum)
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
        return "0"


def get_min_price(item):
    return str(item.min_child_price_excl_tax)


def get_variants_httpresponse(request, shop_slug, item_slug, group_by=None):
    shop = get_object_or_404(Shop, slug__iexact=shop_slug)
    item = get_object_or_404(Product, slug__iexact=item_slug, shop_id=shop.id, parent__isnull=True)
    # if request.is_ajax():
    return HttpResponse(get_variants(item, group_by), content_type='application/json')


def confirm_at_least_one(i):
    if i == 0:
        raise SuspiciousOperation()  # Should have at least one size


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
                        confirm_at_least_one(j)
                        break
                    j += 1
                i += 1
            else:
                confirm_at_least_one(i)
                break
        return sizes

    if sizeType == SIZE_DIM:
        sizes = {}
        i = 0
        while (True):
            sizeDimensionTemplate = "sizeDimensionSelectionTemplate" + str(i)
            sizeDimensionSelection = {"x": sizeDimensionTemplate + "_sizeDimWidth",
                                      "y": sizeDimensionTemplate + "_sizeDimLength"}
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
                        confirm_at_least_one(j)
                        break
                    j += 1
                i += 1
            else:
                confirm_at_least_one(i)
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
                        confirm_at_least_one(j)
                        break
                    j += 1
                i += 1
            else:
                confirm_at_least_one(i)
                break
        return sizes


#private method no Auth
def renderShopEditor(request, shop, productCreationForm=None, aboutForm=None, colorPickerForm=None, logoUploadForm=None,
                     bannerUploadForm=None, item=None):
    editItem = item is not None
    shopCategories, shopCategoryNames = get_filter_lists(shop).categorylist()
    products = get_list_or_empty(Product, shop=shop.id)
    return render(request, 'designer_shop/shopeditor.html', {
        'editmode': True,
        'shop': shop,
        'productCreationForm': productCreationForm or ProductCreationForm(instance=item if editItem else None),
        'editItemMode': editItem,
        'bannerUploadForm': bannerUploadForm or BannerUploadForm(initial=
                                                                 {
                                                                     "banner": shop.banner,
                                                                     "mobileBanner": shop.mobileBanner
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
                                                      "aboutContent": shop.aboutContent,
                                                      "aboutImg": shop.aboutImg
                                                  }),
        'colors': AttributeOption.objects.filter(group=2),
        'sizeSetOptions': AttributeOption.objects.filter(group=1),
        'shopcategories': shopCategoryNames,
        'shopgenders': get_filter_lists(shop).genderlist(),
        'products': products,
        'shopProductCount': len(products)
    })


#private method no Auth
def processShopEditorForms(request, shop_slug, item_slug=None):
    shop = get_object_or_404(Shop, slug__iexact=shop_slug)

    form = None
    item = get_object_or_404(Product, slug__iexact=item_slug, parent__isnull=True) if item_slug else None
    if request.method == 'POST':
        if request.POST.__contains__('bannerUploadForm'):
            form = BannerUploadForm(request.POST, request.FILES)
            if form.is_valid():
                bannerFullPrefix = settings.MEDIA_ROOT + '/shops/{0}/banner'.format(shop.slug)
                mobileBannerFullPrefix = settings.MEDIA_ROOT + '/shops/{0}/mobileBanner'.format(shop.slug)
                bannerFullPath = bannerFullPrefix + "/banner.jpg"
                bannerUrl = settings.MEDIA_URL + 'shops/{0}/banner/banner.jpg'.format(shop.slug)
                mobileBannerFullPath = mobileBannerFullPrefix + "/mobileBanner.jpg"
                mobileBannerUrl = settings.MEDIA_URL + 'shops/{0}/mobileBanner/mobileBanner.jpg'.format(shop.slug)

                if _replaceCroppedFile(form, shop.banner, 'banner.jpg', "bannerCropped"):
                    shop.save(update_fields=["banner"])

                if _replaceCroppedFile(form, shop.mobileBanner, 'mobileBanner.jpg', "mobileBannerCropped"):
                    shop.save(update_fields=["mobileBanner"])

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
            form = AboutBoxForm(request.POST, request.FILES)
            if form.is_valid():
                _replaceCroppedFile(form, shop.aboutImg, 'about.jpg', 'aboutImgCropped')
                shop.aboutContent = form.cleaned_data["aboutContent"]
                shop.save(update_fields=["aboutContent", "aboutImg"])
            return renderShopEditor(request, shop, aboutForm=form)
        elif request.POST.__contains__('genderfilter'):
            return render(request, 'designer_shop/shop_items.html', {
                'editmode': True,
                'shop': shop,
                'products': get_filtered_products(shop, request.POST),
                'shopProductCount': len(get_list_or_empty(Product, shop=shop.id))
            })
        else:
            if request.method == 'POST':
                sizeVariationType = get_dict_value_or_suspicious_operation(request.POST, "sizeVariation")
                sizes = get_sizes_colors_and_quantities(sizeVariationType, request.POST)
                is_create = item is None
                if is_create:
                    form = ProductCreationForm(request.POST, request.FILES, sizes=sizes)
                else:
                    form = ProductCreationForm(request.POST, request.FILES, instance=item if item else None,
                                               sizes=sizes)
                if form.is_valid():
                    canonicalProduct = form.save(shop)
                    form = ProductCreationForm()
                    messages.success(request,
                                     ("Item has been successfully {0}!").format("created" if is_create else "updated"))
            return renderShopEditor(request, shop, productCreationForm=form)
    else:
        return renderShopEditor(request, shop, item=item)


def _replaceCroppedFile(form, file_field, file_name, cropped_field_name):
    if form.cleaned_data[cropped_field_name] and len(form.cleaned_data[cropped_field_name]) > 0:
        file_field.save(file_name, ContentFile(form.cleaned_data[cropped_field_name].decode("base64")))
        return True
    return False


@IsShopOwnerDecoratorUsingItem
def delete_product(request, shop_slug, item_slug):
    item = get_object_or_404(Product, slug__iexact=item_slug, parent__isnull=True)
    product = Product.objects.get(pk=item.id).delete()
    return redirect('designer_shop.views.shopeditor', shop_slug)
