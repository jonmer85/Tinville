from django.contrib.admin import ModelAdmin
from user.models import TinvilleUser, DesignerPayout
from user.forms import TinvilleUserCreationForm, TinvilleUserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin.sites import NotRegistered

class TinvilleUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = TinvilleUserChangeForm
    add_form = TinvilleUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email',
                    'is_admin',
                    'is_seller',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'access_code'
                    )
    list_filter = ('is_admin', 'is_superuser', 'is_seller')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_seller', 'access_code')}),
        ('Permissions', {'fields': ('is_superuser', 'is_admin', 'is_active', 'is_staff')}),
        # ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


@admin.register(DesignerPayout)
class DesignerPayoutAdmin(ModelAdmin):

    list_display = ('designer',
                    'amount',
                    'reference',
                    'datetime',
                    )
    list_filter = ('designer',)
    fieldsets = (
        (None, {'fields': ('designer', 'amount', 'reference', 'datetime')}),
    )
    readonly_fields = ('designer', 'amount', 'reference', 'datetime')
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password')}
    #     ),
    # )
    # search_fields = ('email',)
    # ordering = ('email',)
    # filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(TinvilleUser, TinvilleUserAdmin)
# ... and, since we're not using Django's builtin permissions,
# unregister the Group model from admin.
#TODO should we unregister? Group permissions may help
try:
    admin.site.unregister(Group)
except NotRegistered:
    pass
