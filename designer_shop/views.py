from django.shortcuts import render, get_object_or_404, redirect


from designer_shop.models import Shop, SIZE_SET, SIZE_DIM, SIZE_NUM
from designer_shop.forms import ProductCreationForm, AboutBoxForm, DesignerShopColorPicker

def shopper(request, slug):
    return render(request, 'designer_shop/shopper.html', {
        'shop': get_object_or_404(Shop, slug__exact=slug)
    })

def shopeditor(request, slug):
    shop = get_object_or_404(Shop, slug__exact=slug)
    return render(request, 'designer_shop/shopeditor.html', {
        'shop': shop,
        'productCreationForm': ProductCreationForm,
        'designerShopColorPicker': DesignerShopColorPicker,
        'aboutBoxForm': AboutBoxForm(initial=
                                     {
                                         "aboutContent": shop.aboutContent
                                     })
    })

def shopabout(request, slug):
    
    if request.method == 'POST':
        form = AboutBoxForm(request.POST)

        if form.is_valid():
            currentshop = Shop.objects.get(slug = slug)
            currentshop.aboutContent = form.cleaned_data["aboutContent"]
            currentshop.save(update_fields=["aboutContent"])
        
            return redirect("designer_shop.views.shopeditor", slug)

def postcolor(request, slug):

    if request.method == 'POST':
        form = DesignerShopColorPicker(request.POST)

        if form.is_valid():
            currentShop = Shop.objects.get(slug=slug)
            currentShop.color = form.cleaned_data["color"]
            currentShop.save(update_fields=["color"])

            return redirect("designer_shop.views.shopeditor", slug)

def create_product(request, slug):
    if request.method == 'POST':
        sizeVariationType = request.POST["sizeVariation"]
        sizes = get_sizes_colors_and_quantities(sizeVariationType, request.POST)





def get_sizes_colors_and_quantities(sizeType, post):
    if sizeType == SIZE_NUM:
        sizes = {}
        i = 0
        while(True):
            sizeSet = "sizeSetSelection"+str(i)
            if post[sizeSet]:
                sizes[sizeSet] = {
                    "size": post[sizeSet],
                    "colorAndQuantities": []
                }

                while(True):
                    j = 0
                    color = post[sizeSet + "_colorSelection" + j]
                    quantity = post[sizeSet + "_quantityField" + j]
                    if color and quantity:
                        sizes[sizeSet]["colorAndQuantities"].append({"color": color, "quantity": quantity})
                    ++j
            ++i

