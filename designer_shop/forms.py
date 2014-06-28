import uuid
from django import forms
from oscar.apps.catalogue.models import ProductImage

from oscar.core.loading import get_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Fieldset, HTML
from crispy_forms.bootstrap import PrependedText

from tinymce.widgets import TinyMCE
from color_utils import widgets
from django.core.validators import RegexValidator

from .models import SIZE_DIM, SIZE_NUM, SIZE_SET, SIZE_TYPES

SIZE_TYPES_AND_EMPTY = [('0', 'How is this item sized?')] + SIZE_TYPES

class ProductCreationForm(forms.ModelForm):




    price = forms.DecimalField(decimal_places=2, max_digits=12)

    def __init__(self, *args, **kwargs):
        sizes = kwargs.pop('sizes', [])
        super(ProductCreationForm, self).__init__(*args, **kwargs)

        self.fields['sizeVariation'] = forms.ChoiceField(label='Size type',
                                         choices=SIZE_TYPES_AND_EMPTY,
                                         initial=self.get_value_if_in_edit_mode('sizeVariation', '0'))


        # self.fields['product_image'] = forms.ImageField(required=False)

        self.fields['price'] \
            = forms.DecimalField(decimal_places=2, max_digits=12, initial=self.get_value_if_in_edit_mode('price', None))

        self.fields['product_image'] \
            = forms.ImageField(required=False)



        self.helper = FormHelper()
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                Fieldset('General',
                         Field('title', placeholder='Title'),
                         HTML("""<p>Description</p>"""),
                         Field('description', placeholder='Description'),
                         PrependedText('price', '$', placeholder='Price')
                ),
                Fieldset('Images',
                         'product_image',
                ),
                Fieldset('Sizes and Colors',
                         Field('sizeVariation', placeholder='Choose a variation'),
                         Div(
                             Fieldset('Sizes', css_id="sizesFieldSet", css_class="hidden"))
                         ,
                         css_class="accordion", css_id="accordion2"),
                Submit('productCreationForm', 'Create', css_class='tinvilleButton'),
                css_class="container col-xs-12 col-lg-8",
                css_id="addItemEditor"
            )

        )
        self.fields['description'].widget = TinyMCE()
        self.fields['price'].label = ""

        if sizes:
            for i, size in enumerate(sizes):
                if "sizeSet" in sizes[i] and sizes[i]["sizeSet"]:
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

                elif "sizeX" in sizes[i] and sizes[i]["sizeX"] and "sizeY" in sizes[i] and sizes[i]["sizeY"]:
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

                elif "sizeNum" in sizes[i] and sizes[i]["sizeNum"]:
                    self.fields['sizeNumberSelectionTemplate%s_sizeNumberSelection' % i] \
                        = forms.IntegerField(initial=sizes[i]["sizeNum"])
                    for j, colorAndQuantity in enumerate(sizes[i]["colorsAndQuantities"]):
                        self.fields['sizeNumberSelectionTemplate{}_colorSelection{}'.format(i, j)] \
                        = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                                      objects.filter(group=2), empty_label="Choose a color...",
                                                 initial=sizes[i]["colorsAndQuantities"][j]["color"])
                        self.fields['sizeNumberSelectionTemplate{}_quantityField{}'.format(i, j)] \
                        = forms.IntegerField(initial=sizes[i]["colorsAndQuantities"][j]["quantity"])



    def create_variant_product_from_canonical(self, canonical, canonicalId, shop, sizeSet=None, sizeDim=None, sizeNum=None, color=None, quantity=None):
        variantProduct = canonical
        #IMPORTANT: The setting of the canonical id to the parent_id has to come before the clearing since it is the same reference!!!
        variantProduct.parent_id = canonicalId
        variantProduct.pk = None
        variantProduct.id = None
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

    def clean(self):
        cleaned_data = super(ProductCreationForm, self).clean()
        # do your custom validations / transformations here
        # and some more
        return cleaned_data


    def save(self, shop):
        canonicalProduct = super(ProductCreationForm, self).save(commit=False)
        if not canonicalProduct.upc:
            canonicalProduct.upc = None
        canonicalProduct.shop = shop
        # Jon M TBD - Right now we only use 1 product class - "Apparel"
        canonicalProduct.product_class = get_model('catalogue', 'ProductClass').objects.all()[:1].get()
        canonicalProduct.save()
        canonicalId = canonicalProduct.id
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
                        self.create_variant_product_from_canonical(canonicalProduct, canonicalId, shop, sizeSet=sizeSet,
                                                                   color=color, quantity=quantity)
                    else:
                        if not j:
                            self.create_variant_product_from_canonical(canonicalProduct, canonicalId, shop, sizeSet=sizeSet)
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
                        self.create_variant_product_from_canonical(canonicalProduct, canonicalId, shop, sizeDim={"x": sizeDimX,
                                                                        "y": sizeDimY}, color=color, quantity=quantity)
                    else:
                        if not j:
                            self.create_variant_product_from_canonical(canonicalProduct, canonicalId, shop, sizeDim={"x": sizeDimX,
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
                        self.create_variant_product_from_canonical(canonicalProduct, canonicalId, shop, sizeNum=sizeNum,
                                                                   color=color, quantity=quantity)
                    else:
                        if not j:
                            self.create_variant_product_from_canonical(canonicalProduct, canonicalId,  shop, sizeNum=sizeNum)
                        break
                    j += 1
                i += 1
            else:
                break
        return canonicalProduct

    def get_size_variation(self):
        if not self.instance or not self.instance.is_group:
            return "0"

        for variant in self.instance.variants.all():
            if hasattr(variant.attr, 'size_set'):
                return SIZE_SET
            elif hasattr(variant.attr, 'size_dimension_x') or hasattr(variant.attr, 'size_dimension_y'):
                return SIZE_DIM
            elif hasattr(variant.attr, 'size_number'):
                return SIZE_NUM
        return "0"

    def get_value_if_in_edit_mode(self, field_name, default):
        if not self.instance or not self.instance.is_group:
            return default
        return self.get_value_from_instance(field_name)


    def get_value_from_instance(self, field_name):
        if field_name == 'sizeVariation':
            return self.get_size_variation()
        if field_name == 'price':
            return self.instance.min_variant_price_excl_tax
        if field_name == 'product_image':
            return self.instance.primary_image().original.url
        else:
            return getattr(self.instance, field_name)


    class Meta:
        model = get_model('catalogue', 'Product')
        exclude = ('slug', 'status', 'score',
                   'recommended_products', 'product_options',
                   'attributes', 'categories', 'shop', 'product_class')
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
            Fieldset('About',
            Field('aboutContent', placeholder="Enter Text Here")),
            Submit('aboutBoxForm', 'Submit', css_class='tinvilleButton', css_id="id_SubmitAboutContent"),
            css_class="container"
        ))

class DesignerShopColorPicker(forms.Form):

    color = forms.CharField(widget=widgets.FarbtasticColorPicker, initial = "#663399", max_length=7, min_length = 6,
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

    def clean_color(self):
        tinville_color = self.cleaned_data['color']
        if tinville_color == '#f46430':
            raise forms.ValidationError('Tinville Branding is not Allowed to be Used.')
        return tinville_color




class BannerUploadForm(forms.Form):

    banner = forms.ImageField(required=False, max_length=255, widget=forms.FileInput)

    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(

            Fieldset('Banner Image',
                     HTML("""<p>If nothing is selected and clicked submit, then it will remove banner</p>"""),
                     'banner'),
            Submit('bannerUploadForm', 'Submit Banner', css_class='tinvilleButton', css_id="id_SubmitBanner"),
            css_class="container col-xs-12 col-sm-10"
        ))



class LogoUploadForm(forms.Form):

    logo = forms.ImageField(required=False, max_length=255, widget=forms.FileInput)

    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Fieldset('Logo Image',
                     HTML("""<p>If nothing is selected and clicked submit, then it will remove logo</p>"""),
                     'logo'),
            Submit('logoUploadForm', 'Submit Logo', css_class='tinvilleButton', css_id="id_SubmitLogo"),
            css_class="container col-xs-12 col-sm-10"
        ))
