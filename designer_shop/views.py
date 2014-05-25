import json
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest

from oscar.core.loading import get_model
from designer_shop.models import Shop, SIZE_SET, SIZE_NUM, SIZE_DIM
from designer_shop.forms import ProductCreationForm, AboutBoxForm, DesignerShopColorPicker, BannerUploadForm, \
    LogoUploadForm
from catalogue.models import Product

from common.utils import get_list_or_empty

AttributeOption = get_model('catalogue', 'AttributeOption')


def shopper(request, slug):
    model_class = get_model('catalogue', 'Category')
    categories = model_class.objects.all()
    shop = get_object_or_404(Shop, slug__exact=slug)
    return render(request, 'designer_shop/shopper.html', {
        'shop': shop,
        'categories': categories,
        'products': get_list_or_empty(Product, shop=shop.id)
        # 'categories': get_object_or_404(get_model('catalogue', 'AbstrastCategory')).objects.all()
    })


def shopeditor(request, slug):
    shop = get_object_or_404(Shop, slug__exact=slug)
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
            return renderShopEditor(request, shop, productCreationForm=form)
    else:
        return renderShopEditor(request, shop)

def ajax_about(request, slug):
    if request.method == 'POST':
        form = AboutBoxForm(request.POST)
        currentshop = Shop.objects.get(slug=slug)
        if request.is_ajax() and form.is_valid():
            currentshop.aboutContent = form.cleaned_data["aboutContent"]
            currentshop.save(update_fields=["aboutContent"])
            return HttpResponse(json.dumps({'errors': form.errors}), mimetype='application/json')

    # return renderShopEditor(request, currentShop, colorPickerForm=form)
    return HttpResponseBadRequest(json.dumps(form.errors), mimetype="application/json")


def ajax_color(request, slug):
    if request.method == 'POST':
        currentShop = Shop.objects.get(slug=slug)
        form = DesignerShopColorPicker(request.POST)

        if request.is_ajax() and form.is_valid():
            currentShop.color = form.cleaned_data["color"]
            currentShop.save(update_fields=["color"])
            return HttpResponse(json.dumps({'errors': form.errors}), mimetype='application/json')

    return HttpResponseBadRequest(json.dumps(form.errors), mimetype="application/json")


def get_sizes_colors_and_quantities(sizeType, post):
    if sizeType == SIZE_SET:
        sizes = {}
        i = 0
        while (True):
            sizeSetTemplate = "sizeSetSelectionTemplate" + str(i)
            sizeSetSelection = sizeSetTemplate + "_sizeSetSelection"
            if post[sizeSetSelection]:
                sizes[i] = {
                    "size": post[sizeSetSelection],
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


def renderShopEditor(request, shop, productCreationForm=None, aboutForm=None, colorPickerForm=None, logoUploadForm=None,
                     bannerUploadForm=None):
    return render(request, 'designer_shop/shopeditor.html', {
        'shop': shop,
        'productCreationForm': productCreationForm or ProductCreationForm,
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
        'sizeSetOptions': AttributeOption.objects.filter(group=1)
    })


def uploadbanner(request, slug):
    currentShop = Shop.objects.get(slug=slug)
    if request.method == 'POST':
        form = BannerUploadForm(request.POST, request.FILES)

        if form.is_valid():

            currentShop.banner = form.cleaned_data["banner"]
            currentShop.save(update_fields=["banner"])

    return renderShopEditor(request, currentShop, bannerUploadForm=form)

def uploadlogo(request, slug):
    currentShop = Shop.objects.get(slug=slug)
    if request.method == 'POST':

        form = LogoUploadForm(request.POST, request.FILES)

        if form.is_valid():

            currentShop.logo = form.cleaned_data["logo"]
            currentShop.save(update_fields=["logo"])

    return renderShopEditor(request, currentShop, logoUploadForm=form)

