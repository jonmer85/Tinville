from django import forms

from oscar.core.loading import get_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Fieldset, HTML

from tinymce.widgets import TinyMCE
from color_utils import widgets

from . import models



SIZE_TYPES_AND_EMPTY = [('0', 'How is this item sized?')] + models.SIZE_TYPES

class ProductCreationForm(forms.ModelForm):

    sizeVariation = forms.ChoiceField(label='Size type',
                                         choices=SIZE_TYPES_AND_EMPTY,
                                         initial='0')

    sizeSetSelection = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                              objects.filter(group=1), empty_label="Choose a size...")

    colorSelection0 = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                              objects.filter(group=2), empty_label="Choose a color...")

    product_class = forms.ModelChoiceField(queryset=get_model('catalogue', 'ProductClass').objects.all(),
                                           empty_label="What are you selling?")

    quantityField = forms.IntegerField()


    def __init__(self, *args, **kwargs):
        sizes = kwargs.pop('sizes', [])
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
                             Fieldset('Sizes', css_id="sizesFieldSet", css_class="hidden"))
                         ,css_class="accordion", css_id="accordion2"),
                Submit('productCreationForm', 'Create', css_class='tinvilleButton'),
                css_class="container"
            )

        )
        self.fields['description'].widget = TinyMCE()

        for i, size in enumerate(sizes):
            self.fields['sizeSetSelectionTemplate%s_sizeSetSelection' % i] \
                = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                              objects.filter(group=1), empty_label="Choose a size...", initial=sizes[i]["size"])
            for j, colorAndQuantity in enumerate(sizes[i]["colorsAndQuantities"]):
                self.fields['sizeSetSelectionTemplate{}_colorSelection{}'.format(i, j)] \
                = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                              objects.filter(group=2), empty_label="Choose a color...",
                                         initial=sizes[i]["colorsAndQuantities"][j]["color"])

    class Meta:
        model = get_model('catalogue', 'Product')
        # fields = ['title', 'description', 'product_class']

class AboutBoxForm( forms.Form ):
    
    aboutContent = forms.CharField( widget = TinyMCE( attrs = { 'cols': 50, 'rows': 30 }))
    
    helper = FormHelper()
    helper.form_show_labels = False
    
    helper.layout = Layout(
        Div(
            Fieldset('aboutContent', placeholder="Enter Text Here"),
            Submit('aboutBoxForm', 'Submit', css_class='tinvilleButton'),
            css_class="container"
        ))
    
class DesignerShopColorPicker(forms.Form):

    color = forms.CharField(widget=widgets.FarbtasticColorPicker, initial = "#000000")
    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Field('color'),
            Submit('designerShopColorPicker', 'Create', css_class='tinvilleButton', css_id="shopColorPicker"),
            css_class="container"
        ))