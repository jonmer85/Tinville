from Tinville.Site.models import TinvilleUser
from Tinville.Site.forms import TinvilleUserCreationForm, TinvilleUserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group

class TinvilleUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = TinvilleUserChangeForm
    add_form = TinvilleUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email',
                    'first_name',
                    'middle_name',
                    'last_name',
                    'is_admin',
                    'is_seller',
                    'other_site_url',
                    'shop_name'
                    )
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_seller')}),
        ('Personal info', {'fields': ('first_name', 'middle_name', 'last_name', 'other_site_url', 'shop_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
        # ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'middle_name', 'last_name', 'other_site_url', 'shop_name', 'is_seller',
                       'password', 'password2')}
        ),
    )
    search_fields = ('email', 'shop_name')
    ordering = ('email', 'shop_name')
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(TinvilleUser, TinvilleUserAdmin)
# ... and, since we're not using Django's builtin permissions,
# unregister the Group model from admin.
#TODO should we unregister? Group permissions may help
admin.site.unregister(Group)