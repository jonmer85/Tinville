from designer_shop.models import Shop
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin.sites import NotRegistered
from django.contrib.contenttypes import generic

class ImageInline(generic.GenericTabularInline):
    model = Shop

class ShopAdmin(admin.ModelAdmin):
    # inlines = [
    #     ImageInline,
    # ]

    list_display = ('name',
                    'banner',
                    'logo'
                    )

    list_filter = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'banner', 'logo')}),

    )
    add_fieldsets = (
        (None, {
            'fields': ('name', 'banner', 'logo')}
        ),
    )
    #search_fields = ('email', 'shop_name')
    ordering = ('name',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Shop, ShopAdmin)
