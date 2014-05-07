from django.shortcuts import render, get_object_or_404, redirect


from oscar.core.loading import get_model
from oscar.apps.catalogue.categories import create_from_breadcrumbs
from designer_shop.models import Shop
from designer_shop.forms import ProductCreationForm, AboutBoxForm

def shopper(request, slug):
    return render(request, 'designer_shop/shopper.html', {
        'shop': get_object_or_404(Shop, slug__exact=slug),
        'categories': get_object_or_404(get_model('catalogue', 'AbstrastCategory')).objects.all()
    })

def shopeditor(request, slug):
    shop = get_object_or_404(Shop, slug__exact=slug)
    return render(request, 'designer_shop/shopeditor.html', {
        'shop': shop,
        'productCreationForm': ProductCreationForm,
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
