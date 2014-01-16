
from django.contrib import admin
from django.contrib.sites.models import Site
from .models import MailingListItem

class HiddenAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class MailingListItemAdmin(admin.ModelAdmin):

    list_display = ('email',
                    'ip_address',
                    'creation_time'
                    )

    list_filter = ('email',)
    search_fields = ('email', 'ip_address', 'creation_time')
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MailingListItem, MailingListItemAdmin)

admin.site.unregister(Site)
admin.site.register(Site, HiddenAdmin)

