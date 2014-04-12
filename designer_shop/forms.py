from django import forms

from oscar.core.loading import get_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Fieldset, HTML

from tinymce.widgets import TinyMCE


SIZE_TYPES = [
    ('1', "Set (eg. Small, Medium, Large)"),
    ('2', "Dimensions (eg. Length X Width)"),
    ('3', "Number (eg. Dress size)")
]

SIZE_TYPES_AND_EMPTY = [('0', '*Choose a size type*')] + SIZE_TYPES

class ProductCreationForm(forms.ModelForm):

    sizeVariation = forms.ChoiceField(label='Size type',
                                         choices=SIZE_TYPES_AND_EMPTY,
                                         initial='0')

    sizeSetSelection = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                              objects.filter(group=1))

    colorSelection = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                              objects.filter(group=2))

    quantityField = forms.IntegerField()


    def __init__(self, *args, **kwargs):
        super(ProductCreationForm, self).__init__(*args, **kwargs)
        # password = forms.CharField(label='Password', widget=forms.PasswordInput)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        # helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Div(
                Fieldset('General',
                         Field('title', placeholder='Title'),
                         Field('description', placeholder='Description'),
                         Field('product_class', placeholder='Product Class')
                ),
                Fieldset('Sizes and Colors',
                         Field('sizeVariation', placeholder='Choose a variation'),
                         Div(
                             Fieldset('Sizes',
                                      Div(
                                          Div(
                                              Field('sizeSetSelection', css_class="sizeSetSelection"),
                                              css_class="accordion-heading"
                                          ),
                                          Div(
                                              Div(
                                                  Div(
                                                      Div(Field('colorSelection', placeholder="Choose a color"),
                                                          css_class="col-xs-2 col-xs-offset-8"
                                                      ),
                                                      Div(Field('quantityField', placeholder="Choose a quantity"),
                                                          css_class="col-xs-2"
                                                      ),
                                                      css_class="row hidden row-color-quantity", css_id="rowColorQuantityTemplate"
                                                  ),
                                                  css_class="accordion-inner"
                                              ),
                                              css_class="accordion-body collapse collapse-colors-quantity"
                                          ),
                                          css_class="accordion-group hidden", css_id="sizeSetSelectionTemplate"
                                      ),
                                    css_id="sizesFieldSet", css_class="hidden"
                                 ),
                             ),
                             css_class="accordion", css_id="accordion2"
                         ),
                Submit('productCreationForm', 'Create', css_class='tinvilleButton'),
                css_class="container"
            )

        )

    class Meta:
        model = get_model('catalogue', 'Product')
        # fields = ['title', 'description', 'product_class']

class AboutBoxForm( forms.Form ):
    
    aboutContent = forms.CharField( widget = TinyMCE( attrs = { 'cols': 50, 'rows': 30 }))
    
    helper = FormHelper()
    helper.form_show_labels = False
    
    helper.layout = Layout(
        Div(
            Field('aboutContent', placeholder="Enter Text Here"),
            Submit('aboutBoxForm', 'Submit', css_class='tinvilleButton'),
            css_class="container"
        )) 

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
                               #HTML("""<table class="table" id="sizegrid1">
                                         #              <thead>
                                         #                    <tr>
                                         #                        <td><b>ID</b></td>
                                         #                        <td><b>Name</b></td>
                                         #                        <td><b>Description</b><b></b></td>
                                         #                        <td><b>Color</b></td>
                                         #                    </tr>
                                         #                </thead>
                                         #                <tbody>
                                         #                    <tr>
                                         #                        <td>1</td>
                                         #                        <td>Banana</td>
                                         #                        <td>Bright and bent</td>
                                         #                        <td>Yellow</td>
                                         #                    </tr>
                                         #                    <tr>
                                         #                        <td>2</td>
                                         #                        <td>Apple</td>
                                         #                        <td>Kind of round</td>
                                         #                        <td>Red</td>
                                         #                    </tr>
                                         #                    <tr>
                                         #                        <td>3</td>
                                         #                        <td>Orange</td>
                                         #                        <td>Round</td>
                                         #                        <td>Orange</td>
                                         #                    </tr>
                                         #                </tbody>
                                         #            </table>
                                         #      """
                                         #
                                         #     ),
