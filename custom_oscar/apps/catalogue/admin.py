from oscar.apps.catalogue.admin import *  # noqa

class ProductAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'shop', 'structure',
                    'attribute_summary', 'date_created')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('shop',)
    inlines = [AttributeInline, CategoryInline, ProductRecommendationInline]

admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)