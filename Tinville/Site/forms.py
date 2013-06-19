from crispy_forms.templatetags.crispy_forms_field import css_class
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, ButtonHolder

from Tinville.Site.models import TinvilleUser

class TinvilleDesignerCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TinvilleDesignerCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('first_name'), css_class="span3"),
                Div(Field('last_name'), css_class="span3"),
                css_class="row"
            ),
            Div(
                Div(Field('shop_name'), css_class="span5"),
                css_class="row"
            ),
            Div(
                Div(Field('email'), css_class="span3"),
                Div(Field('email2'), css_class="span3"),
                css_class="row"
            ),
            Div(
                Div(Field('password1'), css_class="span3"),
                Div(Field('password2'), css_class="span3"),
                css_class="row"
            ),
            Submit('submit', 'Register')
        )


    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    email2 = forms.EmailField(label="Re-enter email address")

    class Meta:
        model = TinvilleUser
        # fields = ('email',
        #           'first_name',
        #           'last_name',
        #           'middle_name',
        #           'is_seller',
        #           'other_site_url',
        #           'shop_name'
        #         )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email2(self):
        # Check that the two email addresses match
        email = self.cleaned_data["email"]
        email2 = self.cleaned_data["email2"]
        if email and email2 and email != email2:
            raise forms.ValidationError("Email addresses don't match")
        return email2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(TinvilleDesignerCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_seller = True
        if commit:
            user.save()
        return user


# class TinvilleDesignerCreationForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#
#     email2 = forms.EmailField(label="Re-enter email address")
#
#     class Meta:
#         model = TinvilleUser
#         fields = ('email',
#                   'first_name',
#                   'last_name',
#                   'middle_name',
#                   'is_seller',
#                   'other_site_url',
#                   'shop_name'
#                 )
#
#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2
#
#     def clean_email2(self):
#         # Check that the two email addresses match
#         email = self.cleaned_data["email"]
#         email2 = self.cleaned_data["email2"]
#         if email and email2 and email != email2:
#             raise forms.ValidationError("Email addresses don't match")
#         return email2
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(TinvilleDesignerCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         user.is_seller = True
#         if commit:
#             user.save()
#         return user


class TinvilleUserChangeForm(forms.ModelForm):
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


