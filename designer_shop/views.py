from django.shortcuts import render, get_object_or_404, redirect

from oscar.core.loading import get_model


from designer_shop.models import Shop, SIZE_SET, SIZE_DIM, SIZE_NUM
from designer_shop.forms import ProductCreationForm, AboutBoxForm, DesignerShopColorPicker

def shopper(request, slug):
    return render(request, 'designer_shop/shopper.html', {
        'shop': get_object_or_404(Shop, slug__exact=slug)
    })

def shopeditor(request, slug):
    shop = get_object_or_404(Shop, slug__exact=slug)
    return renderShopEditor(request, shop)

def shopabout(request, slug):
    
    if request.method == 'POST':
        form = AboutBoxForm(request.POST)
        currentshop = Shop.objects.get(slug = slug)
        if form.is_valid():
            currentshop.aboutContent = form.cleaned_data["aboutContent"]
            currentshop.save(update_fields=["aboutContent"])
        
        return renderShopEditor(request, currentshop, aboutForm=form)

def postcolor(request, slug):

    if request.method == 'POST':
        currentShop = Shop.objects.get(slug=slug)
        form = DesignerShopColorPicker(request.POST)

        if form.is_valid():
            currentShop.color = form.cleaned_data["color"]
            currentShop.save(update_fields=["color"])

        return renderShopEditor(request, currentShop, colorPickerForm=form)

def create_product(request, slug):
    if request.method == 'POST':
        currentShop = Shop.objects.get(slug=slug)
        sizeVariationType = request.POST["sizeVariation"]
        sizes = get_sizes_colors_and_quantities(sizeVariationType, request.POST)

        form = ProductCreationForm(request.POST, sizes=sizes)
        if form.is_valid():
            canonicalProduct = form.save(currentShop)

        return renderShopEditor(request, currentShop, productCreationForm=form)

def get_sizes_colors_and_quantities(sizeType, post):
    if sizeType == SIZE_SET:
        sizes = {}
        i = 0
        while(True):
            sizeSetTemplate = "sizeSetSelectionTemplate"+str(i)
            sizeSetSelection = sizeSetTemplate + "_sizeSetSelection"
            if post[sizeSetSelection]:
                sizes[i] = {
                    "size": post[sizeSetSelection],
                    "colorsAndQuantities": []
                }

                j = 0
                while(True):
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


def renderShopEditor(request, shop, productCreationForm=None, aboutForm=None, colorPickerForm=None):
    return render(request, 'designer_shop/shopeditor.html', {
        'shop': shop,
        'productCreationForm': productCreationForm or ProductCreationForm,
        'designerShopColorPicker': colorPickerForm or DesignerShopColorPicker,
        'aboutBoxForm': aboutForm or AboutBoxForm(initial=
                                     {
                                         "aboutContent": shop.aboutContent
                                     }),
        'colors': get_model('catalogue', 'AttributeOption').objects.filter(group=2)
    })



