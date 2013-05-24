from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from Tinville.Site.models import TinvilleUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = TinvilleUser
        fields = ('email',
                  'first_name',
                  'last_name',
                  'middle_name',
                  'is_seller',
                  'other_site_url',
                  'shop_name'
                )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = TinvilleUser

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class TinvilleUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

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
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'middle_name', 'last_name', 'other_site_url', 'shop_name', 'is_seller', 'password1', 'password2')}
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