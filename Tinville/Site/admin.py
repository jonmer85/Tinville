
from django.contrib import admin
from django.contrib.sites.models import Site

class HiddenAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

admin.site.unregister(Site)
admin.site.register(Site, HiddenAdmin)

