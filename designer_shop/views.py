from django.shortcuts import render, get_object_or_404

from django.views.generic import CreateView

from oscar.core.loading import get_model

from designer_shop.models import Shop
from designer_shop.forms import ProductCreationForm, AboutBoxForm

def shopper(request, slug):
    return render(request, 'designer_shop/shopper.html', {
        'shop': get_object_or_404(Shop, slug__exact=slug)
    })

def shopeditor(request):
    return render(request, 'designer_shop/shopeditor.html',
                  {'productCreationForm': ProductCreationForm, 'aboutBoxForm': AboutBoxForm})

def shopabout(request):
    
    if request.method == 'POST':
        form = AboutBoxForm(request.POST)

        if form.is_valid():
            
            currentshop = Shop.objects.get( name = "Demo" )
            currentshop.aboutContent = form.aboutContent
            currentshop.save()
            
            success_url = reverse('home')
            return HttpResponseRedirect(success_url)
        
