from oscar.apps.catalogue.views import ProductDetailView as CoreProductDetailView
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from designer_shop.models import Shop
from custom_oscar.apps.catalogue.models import Product
class ProductDetailView(CoreProductDetailView):

    template_name = 'itemdetail.html'
    enforce_paths = False
    def get_object(self, queryset=None):

        shop = get_object_or_404(Shop, slug__iexact=self.kwargs['shop_slug'])
        item = get_object_or_404(Product, slug__iexact=self.kwargs['item_slug'], shop_id=shop.id, parent__isnull=True)
        return item

    def get_context_data(self, **kwargs):
        ctx = super(ProductDetailView, self).get_context_data(**kwargs)
        ctx['reviews'] = self.get_reviews()
        ctx['alert_form'] = self.get_alert_form()
        ctx['has_active_alert'] = self.get_alert_status()
        ctx['shop'] = get_object_or_404(Shop, slug__iexact=self.kwargs['shop_slug'])
        return ctx

