from django.views.generic import ListView

from custom_oscar.apps.catalogue.models import Product


class HomeListView(ListView):
    template_name = "home.html"
    model = Product
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()


