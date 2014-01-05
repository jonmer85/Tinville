from designer_shop.models import Shop
from django.shortcuts import render, get_object_or_404

def shopper(request, name):
    return render(request, 'designer_shop/shopper.html', {
        'shop': get_object_or_404(Shop, name__exact=name)
    })
