from django import forms

from oscar.core.loading import get_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div
from designer_shop.models import Shop
from color_utils import widgets

class ProductCreationForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_show_labels = False
    # helper.form_class = 'form-horizontal'

    helper.layout = Layout(
        Div(
            Field('title', placeholder="Title"),
            Field('description', placeholder="Description"),
            Field('product_class', placeholder="Product Class"),
            Submit('productCreationForm', 'Create', css_class='tinvilleButton'),
            css_class="container"
        )

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


class DesignerShopColorPicker(forms.Form):
    helper = FormHelper()
    helper.form_show_labels = False
    # helper.form_class = 'form-horizontal'
    colorField = forms.CharField(widget=widgets.FarbtasticColorPicker)

    helper.layout = Layout(
        Div(
            'colorField',
            Submit('designerShopColorPicker', 'Create', css_class='tinvilleButton'),
            css_class="container"
        )
    )


    #self.helper.layout = Layout(
    #DIV(HTML("""<h2>Color Picker</h2>
     #        Choose Color: <input type="color" name="color1" id="color1" /><br /><br />
      #       <input type="button" onClick="processData('color1')" value="Submit" />"""),))

    #function processData(c1) {
	#   var color1 = document.getElementById(c1).value;
	#   alert(color1);
	#   // end the values to server storage
    #}