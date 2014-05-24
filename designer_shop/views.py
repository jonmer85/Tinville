from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.shortcuts import redirect

from oscar.core.loading import get_model
from designer_shop.models import Shop, SIZE_SET, SIZE_NUM, SIZE_DIM
from designer_shop.forms import ProductCreationForm, AboutBoxForm, DesignerShopColorPicker
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
    shop = get_object_or_404(Shop, slug__exact=slug)
    return render(request, 'designer_shop/shopper.html', {
        'shop': shop,
        'products': get_list_or_empty(Product, shop=shop.id)
        # 'categories': get_object_or_404(get_model('catalogue', 'AbstrastCategory')).objects.all()
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

        form = ProductCreationForm(request.POST, request.FILES, sizes=sizes)
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
    if user_shop_owner(request, shop) :
        return render(request, 'designer_shop/shopeditor.html', {
        'shop': shop,
        'productCreationForm': productCreationForm or ProductCreationForm,
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
    else:
        return redirect('home')



