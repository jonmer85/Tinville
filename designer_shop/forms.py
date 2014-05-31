import uuid
from django import forms
from oscar.apps.catalogue.models import ProductImage

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

    price = forms.DecimalField(decimal_places=2, max_digits=12)

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
                         Field('product_class', placeholder='Product Class'),
                         Field('price', placeholder='Price')
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

        if sizes:
            for i, size in enumerate(sizes):
                if "sizeSet" in sizes[i]:
                    self.fields['sizeSetSelectionTemplate%s_sizeSetSelection' % i] \
                        = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                                      objects.filter(group=1), empty_label="Choose a size...", initial=sizes[i]["sizeSet"])
                    for j, colorAndQuantity in enumerate(sizes[i]["colorsAndQuantities"]):
                        self.fields['sizeSetSelectionTemplate{}_colorSelection{}'.format(i, j)] \
                        = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                                      objects.filter(group=2), empty_label="Choose a color...",
                                                 initial=sizes[i]["colorsAndQuantities"][j]["color"])
                        self.fields['sizeSetSelectionTemplate{}_quantityField{}'.format(i, j)] \
                        = forms.IntegerField(initial=sizes[i]["colorsAndQuantities"][j]["quantity"])

                elif "sizeX" in sizes[i] and "sizeY" in sizes[i]:
                    self.fields['sizeDimensionSelectionTemplate%s_sizeDimWidth' %i] \
                        = forms.IntegerField(initial=sizes[i]["sizeX"])
                    self.fields['sizeDimensionSelectionTemplate%s_sizeDimLength' %i] \
                        = forms.IntegerField(initial=sizes[i]["sizeY"])
                    for j, colorAndQuantity in enumerate(sizes[i]["colorsAndQuantities"]):
                        self.fields['sizeDimensionSelectionTemplate{}_colorSelection{}'.format(i, j)] \
                        = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                                      objects.filter(group=2), empty_label="Choose a color...",
                                                 initial=sizes[i]["colorsAndQuantities"][j]["color"])
                        self.fields['sizeDimensionSelectionTemplate{}_quantityField{}'.format(i, j)] \
                        = forms.IntegerField(initial=sizes[i]["colorsAndQuantities"][j]["quantity"])

                elif "sizeNum" in sizes[i]:
                    self.fields['sizeNumberSelectionTemplate%s_sizeNumberSelection' % i] \
                        = forms.IntegerField(initial=sizes[i]["sizeNum"])
                    for j, colorAndQuantity in enumerate(sizes[i]["colorsAndQuantities"]):
                        self.fields['sizeNumberSelectionTemplate{}_colorSelection{}'.format(i, j)] \
                        = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                                      objects.filter(group=2), empty_label="Choose a color...",
                                                 initial=sizes[i]["colorsAndQuantities"][j]["color"])
                        self.fields['sizeNumberSelectionTemplate{}_quantityField{}'.format(i, j)] \
                        = forms.IntegerField(initial=sizes[i]["colorsAndQuantities"][j]["quantity"])



    def create_variant_product_from_canonical(self, canonical, shop, sizeSet=None, sizeDim=None, sizeNum=None, color=None, quantity=None):
        variantProduct = canonical
        variantProduct.pk = None
        variantProduct.id = None
        variantProduct.parent_id = canonical.id
        if sizeSet:
            setattr(variantProduct.attr, 'size_set', sizeSet)
        if sizeDim:
            setattr(variantProduct.attr, 'size_dimension_x', sizeDim['x'])
            setattr(variantProduct.attr, 'size_dimension_y', sizeDim['y'])
        if sizeNum:
            setattr(variantProduct.attr, 'size_number', sizeNum)
        if color:
            setattr(variantProduct.attr, 'color', color)
        variantProduct.save()

        partner = get_partner_from_shop(shop)

        stockRecord \
            = get_model('partner', 'StockRecord')(product=variantProduct,
                                                    price_excl_tax=self.cleaned_data['price'],
                                                    partner=partner)
        if(quantity):
            stockRecord.num_in_stock = quantity
        # Hack to ensure unique SKU. We should look into how real SKUs should work TODO

        stockRecord.partner_sku = uuid.uuid4()
        stockRecord.save()


    def save(self, shop):
        canonicalProduct = super(ProductCreationForm, self).save(commit=False)
        if not canonicalProduct.upc:
            canonicalProduct.upc = None
        canonicalProduct.shop = shop
        canonicalProduct.save()
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
                        self.create_variant_product_from_canonical(canonicalProduct, shop, sizeSet=sizeSet,
                                                                   color=color, quantity=quantity)
                    else:
                        if not j:
                            self.create_variant_product_from_canonical(canonicalProduct, shop, sizeSet=sizeSet)
                        break
                    j += 1
                i += 1
            # Tom Bowman was here 5-25-14
            elif ('sizeDimensionSelectionTemplate%s_sizeDimWidth' % i) in self.cleaned_data and\
                            ('sizeDimensionSelectionTemplate%s_sizeDimLength' % i) in self.cleaned_data:
                sizeDimX = self.cleaned_data['sizeDimensionSelectionTemplate%s_sizeDimWidth' % i]
                sizeDimY = self.cleaned_data['sizeDimensionSelectionTemplate%s_sizeDimLength' % i]
                j = 0
                while True:
                    if ('sizeDimensionSelectionTemplate{}_colorSelection{}'.format(i, j) in self.cleaned_data and
                            'sizeDimensionSelectionTemplate{}_colorSelection{}'.format(i, j) in self.cleaned_data):
                        color = self.cleaned_data['sizeDimensionSelectionTemplate{}_colorSelection{}'.format(i, j)]
                        quantity = self.cleaned_data['sizeDimensionSelectionTemplate{}_quantityField{}'.format(i, j)]
                        self.create_variant_product_from_canonical(canonicalProduct, shop, sizeDim={"x": sizeDimX,
                                                                        "y": sizeDimY}, color=color, quantity=quantity)
                    else:
                        if not j:
                            self.create_variant_product_from_canonical(canonicalProduct, shop, sizeDim={"x": sizeDimX,
                                                                                                    "y": sizeDimY})
                        break
                    j += 1
                i += 1
            elif ('sizeNumberSelectionTemplate%s_sizeNumberSelection' % i) in self.cleaned_data:
                sizeNum = self.cleaned_data['sizeNumberSelectionTemplate%s_sizeNumberSelection' % i]
                j = 0
                while True:
                    if ('sizeNumberSelectionTemplate{}_colorSelection{}'.format(i, j) in self.cleaned_data and
                            'sizeNumberSelectionTemplate{}_colorSelection{}'.format(i, j) in self.cleaned_data):
                        color = self.cleaned_data['sizeNumberSelectionTemplate{}_colorSelection{}'.format(i, j)]
                        quantity = self.cleaned_data['sizeNumberSelectionTemplate{}_quantityField{}'.format(i, j)]
                        self.create_variant_product_from_canonical(canonicalProduct, shop, sizeNum=sizeNum,
                                                                   color=color, quantity=quantity)
                    else:
                        if not j:
                            self.create_variant_product_from_canonical(canonicalProduct, shop, sizeNum=sizeNum)
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


def get_partner_from_shop(shop):
    Partner = get_model('partner', 'Partner')
    shop_owner = shop.user

    if Partner.objects.filter(users__id=shop_owner.id).exists():
        return Partner.objects.filter(users__id=shop_owner.id)[0]
    else:
        partner = Partner(name=shop_owner.email, code=shop_owner.slug)
        partner.save()
        partner.users.add(shop_owner)
        return partner

class AboutBoxForm(forms.Form):

    aboutContent = forms.CharField(widget=TinyMCE( attrs = { 'cols': 50, 'rows': 30 }))

    helper = FormHelper()
    helper.form_show_labels = False
    helper.form_class = 'aboutForm'
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

class BannerUploadForm(forms.Form):

    banner = forms.ImageField(required=False)

    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Fieldset('Banner Image',
                     'banner',
                     # HTML("""{% if form.banner.value %}<img class="img-responsive" src="{{ MEDIA_URL }}{{ form.banner.value }}">{% endif %}""", ),
                    ),
            Submit('bannerUploadForm', 'Submit Banner', css_class='tinvilleButton', css_id="bannerUpload"),
            css_class="container"
        ))

class LogoUploadForm(forms.Form):

    logo = forms.ImageField(required=False)

    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Fieldset('Logo Image',
                     'logo',
                     # HTML("""{% if form.logo.value %}<img class="img-responsive" src="{{ MEDIA_URL }}{{ form.logo.value }}">{% endif %}""", ),
                     ),
            Submit('logoUploadForm', 'Submit Logo', css_class='tinvilleButton', css_id="logoUpload"),
            css_class="container"
        ))
