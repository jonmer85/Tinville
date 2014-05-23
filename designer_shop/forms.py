from django import forms
from oscar.apps.catalogue.models import ProductImage, LogoImage, BannerImage

from oscar.core.loading import get_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Fieldset, HTML

from tinymce.widgets import TinyMCE
from color_utils import widgets
from django.core.validators import RegexValidator

from . import models

SIZE_TYPES_AND_EMPTY = [('0', 'How is this item sized?')] + models.SIZE_TYPES

class ProductCreationForm(forms.ModelForm):

    sizeVariation = forms.ChoiceField(label='Size type',
                                         choices=SIZE_TYPES_AND_EMPTY,
                                         initial='0')

    product_class = forms.ModelChoiceField(queryset=get_model('catalogue', 'ProductClass').objects.all(),
                                           empty_label="What are you selling?")

    product_image = forms.ImageField(required=False)

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
                Fieldset('Images',
                         'product_image',
                         HTML("""{% if form.product_image.value %}<img class="img-responsive" src="{{ MEDIA_URL }}{{ form.product_image.value }}">{% endif %}""", ),
                ),
                Fieldset('Sizes and Colors',
                         Field('sizeVariation', placeholder='Choose a variation'),
                         Div(
                             Fieldset('Sizes', css_id="sizesFieldSet", css_class="hidden"))
                         ,
                         css_class="accordion", css_id="accordion2"),
                Submit('productCreationForm', 'Create', css_class='tinvilleButton'),
                css_class="container col-sm-12"
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
                self.fields['sizeSetSelectionTemplate{}_quantityField{}'.format(i, j)] \
                = forms.IntegerField(initial=sizes[i]["colorsAndQuantities"][j]["quantity"])

    def save(self, shop):
        canonicalProduct = super(ProductCreationForm, self).save(commit=False)
        if not canonicalProduct.upc:
            canonicalProduct.upc = None
        canonicalProduct.shop = shop
        canonicalProduct.save()
        canonicalProductId = canonicalProduct.id
        productImage = ProductImage(product=canonicalProduct)
        productImage.original = self.cleaned_data['product_image']
        productImage.save()

        i = 0
        while True:
            if ('sizeSetSelectionTemplate%s_sizeSetSelection' % i) in self.cleaned_data:
                sizeSet = self.cleaned_data['sizeSetSelectionTemplate%s_sizeSetSelection' % i]
                j = 0
                while True:
                    if ('sizeSetSelectionTemplate{}_colorSelection{}'.format(i, j) in self.cleaned_data and
                            'sizeSetSelectionTemplate{}_colorSelection{}'.format(i, j) in self.cleaned_data):
                        color = self.cleaned_data['sizeSetSelectionTemplate{}_colorSelection{}'.format(i, j)]
                        quantity = self.cleaned_data['sizeSetSelectionTemplate{}_quantityField{}'.format(i, j)]

                        variantProduct = canonicalProduct
                        variantProduct.pk = None
                        variantProduct.id = None
                        variantProduct.parent_id = canonicalProductId
                        setattr(variantProduct.attr, 'size_set', sizeSet)
                        setattr(variantProduct.attr, 'color', color)
                        variantProduct.save()
                    else:
                        break
                    j += 1
                i += 1
            else:
                break


        return canonicalProduct

    class Meta:
        model = get_model('catalogue', 'Product')
        exclude = ('slug', 'status', 'score',
                   'recommended_products', 'product_options',
                   'attributes', 'categories', 'shop')
        # fields = ['title', 'description', 'product_class']

class AboutBoxForm(forms.Form):

    aboutContent = forms.CharField(widget=TinyMCE( attrs = { 'cols': 50, 'rows': 30 }))

    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Field('aboutContent', placeholder="Enter Text Here"),
            Submit('aboutBoxForm', 'Submit', css_class='tinvilleButton'),
            css_class="container"
        ))

class DesignerShopColorPicker(forms.Form):

    color = forms.CharField(widget=widgets.FarbtasticColorPicker, initial = "#ffffff", max_length=7, min_length = 6,
                             validators=[
        RegexValidator(
            regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
            message='Invalid hex code',
        ),])

    helper = FormHelper()
    helper.form_show_labels = False
    helper.form_class = 'colorForm'
    helper.layout = Layout(
        Div(
            Field('color'),
            Submit('designerShopColorPicker', 'Select', css_class='tinvilleButton', css_id="shopColorPicker"),
            css_class="container"
        ))

class BannerUploadForm( forms.Form ):

    banner = forms.ImageField()

    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Fieldset('Images',
                     'banner',
                      HTML("""{% if form.banner.value %}<img class="img-responsive" src="{{ MEDIA_URL }}{{ form.banner.value }}">{% endif %}""", ),
                ),
            Submit('bannerUploadForm', 'Submit', css_class='tinvilleButton'),
            css_class="container"
        ))

class LogoUploadForm( forms.Form ):

    logo = forms.ImageField()

    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Fieldset('Images',
                     'logo',
                     HTML("""{% if form.logo.value %}<img class="img-responsive" src="{{ MEDIA_URL }}{{ form.logo.value }}">{% endif %}""", ),
                ),
            Submit('logoUploadForm', 'Submit', css_class='tinvilleButton'),
            css_class="container"
        ))

    def save(self, shop):
        tempLogo = super(LogoUploadForm, self).save(commit=False)
        if not tempLogo.upc:
            tempLogo.upc = None
        tempLogo.shop = shop
        tempLogo.save()
        canonicalProductId = tempLogo.id
        logoImage = LogoImage(product=tempLogo)
        logoImage.original = self.cleaned_data['logo']
        logoImage.save()