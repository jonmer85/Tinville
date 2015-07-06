from django.template.context import RequestContext
from django.shortcuts import render_to_response
from designer_shop.views import get_filtered_products,get_category_products,get_filter_lists, get_types
from designer_shop.models import Shop,FeaturedShop
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from common.utils import get_list_or_empty, get_or_none, passes_test_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView
import random

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
@csrf_protect
def home_gallery(request):
    template = "home.html"
    page_template = "designer_shop/all_gallery.html"
    menproducts = get_category_products(genderfilter="Men")
    menproducts = menproducts.order_by('?')
    womenproducts = get_category_products(genderfilter="Women")
    womenproducts = womenproducts.order_by('?')

    context = {
        'homemode': True,
        'menproducts': menproducts,
        'womenproducts': womenproducts,
    }
    if request.is_ajax():
        template = page_template
    return render_to_response(template, context, context_instance=RequestContext(request))


def shop_gallery(request):
    template = "homepage/all_home.html"
    page_template = "designer_shop/all_gallery.html"



    if request.method == 'GET':
        if request.GET.__contains__('genderfilter'):
            products = get_filtered_products(post=request.GET, filter=True)
            shopCategoryNames = get_types(request=request,shop_slug=None,group_by=request.GET['genderfilter'])
            return render(request, 'homepage/all_home.html', {
                'homemode': True,
                'products': products,
                'shopProductCount': len(products),
                'shopcategories': shopCategoryNames
            })

    products = get_filtered_products().order_by('?')
    shopCategories, shopCategoryNames = get_filter_lists().categorylist()
    context = {
        'homemode': True,
        'products': products,
        'shopcategories': shopCategoryNames,
        'shopgenders': get_filter_lists().genderlist(),
        'shopProductCount' : len(products)
    }
    if request.is_ajax():
        template = page_template
    return render_to_response(template, context, context_instance=RequestContext(request))
