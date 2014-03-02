from django import forms

from oscar.core.loading import get_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div



class ProductCreationForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_show_labels = False
    # helper.form_class = 'form-horizontal'

    helper.layout = Layout(
        Field('title', placeholder="Title"),
        Field('description', placeholder="Description"),
        Submit('productCreationForm', 'Create', css_class='tinvilleButton')
    )

    class Meta:
        model = get_model('catalogue', 'Product')
        fields = ['title', 'description']

    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password = self.cleaned_data.get("password")
    #     password2 = self.cleaned_data.get("passwosrd2")
    #     if password and password2 and password != password2:
    #         raise forms.ValidationError("Passwords do not match")
    #     return password2
    #
    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     user = super(TinvilleUserCreationForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #
    #     if commit:
    #         user.save()
    #
    #     if user.is_seller:
    #         user.shop = Shop.objects.create(user=user, name=self.cleaned_data['shop_name'])
    #
    #     return user
    #
    # def clean_email(self):
    #     return self.cleaned_data['email'].lower()