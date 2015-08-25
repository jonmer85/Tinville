from django.template.context import RequestContext
from django.shortcuts import render_to_response
from designer_shop.views import get_filtered_products,get_category_products,get_filter_lists, get_types
from designer_shop.models import Shop,FeaturedShop
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from common.utils import get_list_or_empty, get_or_none, passes_test_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView
import random

# @passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
# @csrf_protect
def home_gallery(request):
    template = "home.html"
    page_template = "designer_shop/all_gallery.html"
    menproducts = get_category_products(genderfilter="Men")
    womenproducts = get_category_products(genderfilter="Women")
    menproducts = menproducts.order_by('?')[:5]
    womenproducts = womenproducts.order_by('?')[:5]

    context = {
        'homemode': True,
        'menproducts': menproducts,
        'womenproducts': womenproducts,
    }
    if request.is_ajax():
        template = page_template
    return render_to_response(template, context, context_instance=RequestContext(request))

def gender_home(request, gender):
    template = "homepage/" + gender + "_home.html"

    page_template = "designer_shop/all_gallery.html"

    if gender is None or gender == "all":
        gender = None
    homepage = request.META.get('HTTP_REFERER')
    if request.method == 'GET':
        if request.GET.__contains__('genderfilter'):
            products = get_filtered_products(post=request.GET, filter=True)
            shopCategoryNames = get_types(request=request,shop_slug=None,group_by=request.GET['genderfilter'])
            template = 'designer_shop/shop_items.html'
            context = {
                'homemode': True,
                'products': products,
                'shopProductCount': len(products),
                'shopcategories': shopCategoryNames,
                'homepage': homepage
            }

            return template, context

    products = get_category_products()
    shopCategories, shopCategoryNames = get_filter_lists().categorylist()
    context = {
        'homemode': True,
        'products': products,
        'shopcategories': shopCategoryNames,
        'shopgenders': get_filter_lists().genderlist(),
        'shopProductCount' : len(products),
        'homepage': homepage
    }
    if request.is_ajax():
        template = page_template

    return template, context

def men_home(request):
    template, context = gender_home(request,'men')
    if request.method == 'GET':
        return render(request,template,context)
    else:
        return render_to_response(template, context, context_instance=RequestContext(request))


def women_home(request):
    template, context = gender_home(request,'women')
    if request.method == 'GET':
        return render(request,template,context)
    else:
        return render_to_response(template, context, context_instance=RequestContext(request))

def shop_gallery(request):
    template, context = gender_home(request,'all')
    if request.method == 'GET':
        return render(request,template,context)
    else:
        return render_to_response(template, context, context_instance=RequestContext(request))


