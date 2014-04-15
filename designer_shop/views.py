from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from designer_shop.models import Shop
from designer_shop.forms import ProductCreationForm, DesignerShopColorPicker
from django.core.urlresolvers import reverse

def shopper(request, slug):
    return render(request, 'designer_shop/shopper.html', {
        'shop': get_object_or_404(Shop, slug__exact=slug)
    })

def shopeditor(request):
    return render(request, 'designer_shop/shopeditor.html',
                  {'productCreationForm': ProductCreationForm, 'designerShopColorPicker': DesignerShopColorPicker,
                   })

def postcolor(request):
    if request.method == 'POST':
        form = DesignerShopColorPicker(request.POST)
        if form.is_valid():
            #create initial entry for User object
            currentShop = Shop.objects.get(name="Demo")
            color = form.cleaned_data['color']
            currentShop.color = color
            currentShop.save()


    return shopeditor(request)