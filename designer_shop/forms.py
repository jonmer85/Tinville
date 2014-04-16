from django import forms

from oscar.core.loading import get_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Fieldset, HTML

from tinymce.widgets import TinyMCE
from color_utils import widgets


SIZE_TYPES = [
    ('1', "Set (eg. Small, Medium, Large)"),
    ('2', "Dimensions (eg. Length X Width)"),
    ('3', "Number (eg. Dress size)")
]

SIZE_TYPES_AND_EMPTY = [('0', 'How is this item sized?')] + SIZE_TYPES

class ProductCreationForm(forms.ModelForm):

    sizeVariation = forms.ChoiceField(label='Size type',
                                         choices=SIZE_TYPES_AND_EMPTY,
                                         initial='0')

    sizeSetSelection = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                              objects.filter(group=1), empty_label="Choose a size...")

    colorSelection = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                              objects.filter(group=2), empty_label="Choose a color...")

    product_class = forms.ModelChoiceField(queryset=get_model('catalogue', 'ProductClass').objects.all(),
                                           empty_label="What are you selling?")

    quantityField = forms.IntegerField()


    def __init__(self, *args, **kwargs):
        super(ProductCreationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False

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
                                                  HTML("""<table class="table">
                                                      <thead>
                                                            <tr>
                                                                <td class="col-xs-8"><b>Color</b></td>
                                                                <td class="col-xs-4"><b>Quantity</b></td>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            <tr class="hidden row-color-quantity" id="rowColorQuantityTemplate">
                                                                <td>"""),
                                                  Div(Field('colorSelection', placeholder="Choose a color"),
                                                          css_class="row-color"
                                                      ),
                                                  HTML("""</td>
                                                     <td>"""),
                                                  Div(Field('quantityField', placeholder="Choose a quantity"),
                                                          css_class=""
                                                      ),
                                                  HTML("""
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                    """
                                                  ), css_class="accordion-inner table-responsive"
                                             ),
                                              css_class="accordion-body collapse collapse-colors-quantity col-xs-8 col-xs-offset-4"
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
        self.fields['description'].widget = TinyMCE()

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