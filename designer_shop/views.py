import json
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest


from oscar.core.loading import get_model
from designer_shop.models import Shop, SIZE_SET, SIZE_NUM, SIZE_DIM
from designer_shop.forms import ProductCreationForm, AboutBoxForm, DesignerShopColorPicker, BannerUploadForm, \
    LogoUploadForm
from catalogue.models import Product

from common.utils import get_list_or_empty

AttributeOption = get_model('catalogue', 'AttributeOption')

def user_shop_owner(request, shop):
    if request.user.is_authenticated():
        if request.user.id == shop.user_id:
            return True
        else:
                return False
    else:
        return False


def shopper(request, slug):
    shop = get_object_or_404(Shop, slug__iexact=slug)
    return render(request, 'designer_shop/shopper.html', {
        'shop': shop,
        'categories': get_model('catalogue', 'Category').objects.all(),
        'products': get_list_or_empty(Product, shop=shop.id)
        # 'categories': get_object_or_404(get_model('catalogue', 'AbstrastCategory')).objects.all()
    })


def shopeditor(request, slug):
    shop = get_object_or_404(Shop, slug__iexact=slug)
    if(user_shop_owner(request, shop)):
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
            return renderShopEditor(request, shop)
    else:
        return redirect('home')

def ajax_about(request, slug):
    if request.method == 'POST':
        form = AboutBoxForm(request.POST)
        currentshop = Shop.objects.get(slug__iexact=slug)
        if request.is_ajax() and form.is_valid():
            currentshop.aboutContent = form.cleaned_data["aboutContent"]
            currentshop.save(update_fields=["aboutContent"])
            return HttpResponse(json.dumps({'errors': form.errors}), mimetype='application/json')

    # return renderShopEditor(request, currentShop, colorPickerForm=form)
    return HttpResponseBadRequest(json.dumps(form.errors), mimetype="application/json")


def ajax_color(request, slug):
    if request.method == 'POST':
        currentShop = Shop.objects.get(slug__iexact=slug)
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


def renderShopEditor(request, shop, productCreationForm=None, aboutForm=None, colorPickerForm=None, logoUploadForm=None,
                     bannerUploadForm=None):
    if(user_shop_owner(request, shop)):
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
        'sizeSetOptions': AttributeOption.objects.filter(group=1),
        'categories': get_model('catalogue', 'Category').objects.all(),
        'products': get_list_or_empty(Product, shop=shop.id)
    })
    else:
        return redirect('home')

def uploadbanner(request, slug):
    currentShop = Shop.objects.get(slug__iexact=slug)
    if request.method == 'POST':
        form = BannerUploadForm(request.POST, request.FILES)

        if form.is_valid():

            currentShop.banner = form.cleaned_data["banner"]
            currentShop.save(update_fields=["banner"])

    return renderShopEditor(request, currentShop, bannerUploadForm=form)

def uploadlogo(request, slug):
    currentShop = Shop.objects.get(slug__iexact=slug)
    if request.method == 'POST':

        form = LogoUploadForm(request.POST, request.FILES)

        if form.is_valid():

            currentShop.logo = form.cleaned_data["logo"]
            currentShop.save(update_fields=["logo"])

    return renderShopEditor(request, currentShop, logoUploadForm=form)

