from django.template.context import RequestContext
from django.shortcuts import render_to_response
from designer_shop.views import get_filtered_products


def home_gallery(request):
    template = "home.html"
    page_template = "designer_shop/item_gallery.html"
    products = get_filtered_products()
    context = {
        'products': products
    }
    if request.is_ajax():
        template = page_template
    return render_to_response(template, context, context_instance=RequestContext(request))