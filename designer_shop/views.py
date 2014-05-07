from django.shortcuts import render, get_object_or_404, redirect


from designer_shop.models import Shop
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