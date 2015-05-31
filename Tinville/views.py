from django.template.context import RequestContext
from django.shortcuts import render_to_response
from designer_shop.views import get_filtered_products,get_category_products,get_filter_lists
from designer_shop.models import Shop,FeaturedShop
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from common.utils import get_list_or_empty, get_or_none



def home_gallery(request):
    template = "home.html"
    page_template = "designer_shop/all_gallery.html"
    products = get_filtered_products()
    featured_shop = get_list_or_empty(FeaturedShop)
    featured_shop_ids = [f.featured_id for f in featured_shop]
    fshops = Shop.objects.filter(id__in=featured_shop_ids)
    shopCategories, shopCategoryNames = get_filter_lists().categorylist()

    context = {
        'products': products,
        'fshops' : fshops,
        'shopcategories': shopCategoryNames,
        'shopgenders': get_filter_lists().genderlist(),
        'shopProductCount' : len(products)

    }
    if request.is_ajax():
        template = page_template
    return render_to_response(template, context, context_instance=RequestContext(request))


def men_gallery(request):
    template = "homepage/men_home.html"
    page_template = "designer_shop/all_gallery.html"
    products = get_category_products(genderfilter="Men")
    shopCategories, shopCategoryNames = get_filter_lists().categorylist()

    context = {
        'products': products,
        'shopcategories': shopCategoryNames,
        'shopgenders': get_filter_lists().genderlist(),
        'shopProductCount' : len(products)
    }
    if request.is_ajax():
        template = page_template
    return render_to_response(template, context, context_instance=RequestContext(request))

def women_gallery(request):
    template = "homepage/women_home.html"
    page_template = "designer_shop/all_gallery.html"
    products = get_category_products(genderfilter="Women")
    shopCategories, shopCategoryNames = get_filter_lists().categorylist()

    context = {
        'products': products,
        'shopcategories': shopCategoryNames,
        'shopgenders': get_filter_lists().genderlist(),
        'shopProductCount' : len(products)
    }
    if request.is_ajax():
        template = page_template
    return render_to_response(template, context, context_instance=RequestContext(request))
