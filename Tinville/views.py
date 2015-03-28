from custom_oscar.apps.catalogue.models import Product

from designer_shop.models import Shop
from django.views.generic import ListView


class HomeListView(ListView):
    template_name = "home.html"
    model = Product
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(shop = Shop.objects.filter(user__is_approved = True))
