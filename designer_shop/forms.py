import uuid
from django import forms
from oscar.apps.catalogue.models import ProductImage

from oscar.core.loading import get_model
from django.core.exceptions import ObjectDoesNotExist

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Fieldset, HTML, Button
from crispy_forms.bootstrap import PrependedText
from south.orm import _FakeORM

from tinymce.widgets import TinyMCE
from color_utils import widgets
from django.core.validators import RegexValidator
from parsley.decorators import parsleyfy

from .models import SIZE_DIM, SIZE_NUM, SIZE_SET, SIZE_TYPES
from common.utils import get_or_none
from common.widgets import AdvancedFileInput



SIZE_TYPES_AND_EMPTY = [('', 'How is this item sized?')] + SIZE_TYPES

@parsleyfy
class ProductCreationForm(forms.ModelForm):

    price = forms.DecimalField(decimal_places=2, max_digits=12)
    title = forms.CharField(label="title",max_length=80)

    def __init__(self, *args, **kwargs):
        sizes = kwargs.pop('sizes', [])
        super(ProductCreationForm, self).__init__(*args, **kwargs)

        self.fields['sizeVariation'] = forms.ChoiceField(label='Size type',
                                         choices=SIZE_TYPES_AND_EMPTY, required=True,
                                         initial=self.get_value_if_in_edit_mode('sizeVariation', '0'))


        # self.fields['product_image'] = forms.ImageField(required=False)

        self.fields['price'] \
            = forms.DecimalField(decimal_places=2, max_digits=12, initial=self.get_value_if_in_edit_mode('price', None))

        self.helper = FormHelper()
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                Fieldset('General',
                         Field('title', placeholder='Title'),
                         HTML("""<p>Description</p>"""),
                         Field('description', placeholder='Description'),
                         Field('category', placeholder='Choose a Category'),
                         Field('price', placeholder='Price')
                ),
                Fieldset('Images',
                         Field( 'product_image', css_id="id_productImage" ),
                         Field( 'product_image1', css_id="id_productImage1", css_class='hidden'),
                         Field( 'product_image2', css_id="id_productImage2", css_class='hidden'),
                         Field( 'product_image3', css_id="id_productImage3", css_class='hidden'),
                         Field( 'product_image4', css_id="id_productImage4", css_class='hidden')
                ),
                Fieldset('Sizes and Colors',
                         Field('sizeVariation', placeholder='Choose a variation'),
                         Div(
                             Fieldset('Sizes', css_id="sizesFieldSet", css_class="hidden"))
                         ,
                         css_class="accordion", css_id="accordion2"),
                Submit('productCreationForm', 'Edit' if self.instance.pk else 'Create', css_class='tinvilleButton'),
                css_class="container col-xs-offset-1 col-xs-10 col-sm-offset-0 col-sm-11 col-lg-6",
                css_id="addItemEditor"
            )

        )

        self.fields['product_image'] \
            = forms.ImageField(required=False, initial=self.get_value_if_in_edit_mode('product_image', None),
                               widget=AdvancedFileInput)
        self.fields['product_image1'] = forms.ImageField(required=False, initial=self.get_value_if_in_edit_mode('product_image1', None),
                                                         widget=forms.ClearableFileInput)
        self.fields['product_image2'] = forms.ImageField(required=False, initial=self.get_value_if_in_edit_mode('product_image2', None),
                                                         widget=forms.ClearableFileInput)
        self.fields['product_image3'] = forms.ImageField(required=False, initial=self.get_value_if_in_edit_mode('product_image3', None),
                                                         widget=forms.ClearableFileInput)
        self.fields['product_image4'] = forms.ImageField(required=False, initial=self.get_value_if_in_edit_mode('product_image4', None),
                                                         widget=forms.ClearableFileInput)

        self.fields['description'].widget = TinyMCE()
        self.fields['category'] = forms.ModelChoiceField(queryset=get_model('catalogue', 'Category').objects.filter(depth=3),
                                                         empty_label="Choose a Category", required=True,
                                                         initial=self.get_value_if_in_edit_mode('category', None))
        self.fields['price'].label = ""

        if sizes:
            for i, size in enumerate(sizes):
                if "sizeSet" in sizes[i] and sizes[i]["sizeSet"]:
                    self.fields['sizeSetSelectionTemplate%s_sizeSetSelection' % i] \
                        = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                                      objects.filter(group=1), empty_label="Choose a size...", required=True, initial=sizes[i]["sizeSet"])
                    for j, colorAndQuantity in enumerate(sizes[i]["colorsAndQuantities"]):
                        self.fields['sizeSetSelectionTemplate{}_colorSelection{}'.format(i, j)] \
                        = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                                      objects.filter(group=2), empty_label="Choose a color...",
                                                 initial=sizes[i]["colorsAndQuantities"][j]["color"])
                        self.fields['sizeSetSelectionTemplate{}_quantityField{}'.format(i, j)] \
                        = forms.IntegerField(initial=sizes[i]["colorsAndQuantities"][j]["quantity"])

                elif "sizeX" in sizes[i] and sizes[i]["sizeX"] and "sizeY" in sizes[i] and sizes[i]["sizeY"]:
                    self.fields['sizeDimensionSelectionTemplate%s_sizeDimWidth' %i] \
                        = forms.DecimalField(initial=sizes[i]["sizeX"])
                    self.fields['sizeDimensionSelectionTemplate%s_sizeDimLength' %i] \
                        = forms.DecimalField(initial=sizes[i]["sizeY"])
                    for j, colorAndQuantity in enumerate(sizes[i]["colorsAndQuantities"]):
                        self.fields['sizeDimensionSelectionTemplate{}_colorSelection{}'.format(i, j)] \
                        = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                                      objects.filter(group=2), empty_label="Choose a color...",
                                                 initial=sizes[i]["colorsAndQuantities"][j]["color"])
                        self.fields['sizeDimensionSelectionTemplate{}_quantityField{}'.format(i, j)] \
                        = forms.IntegerField(initial=sizes[i]["colorsAndQuantities"][j]["quantity"])

                elif "sizeNum" in sizes[i] and sizes[i]["sizeNum"]:
                    self.fields['sizeNumberSelectionTemplate%s_sizeNumberSelection' % i] \
                        = forms.DecimalField(initial=sizes[i]["sizeNum"])
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
        variantProduct.description = canonical.description
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


    def clean_title(self):
        title = self.cleaned_data['title']
        products = get_model('catalogue', 'Product')

        if self.instance.pk and self.get_value_from_instance("title") == title:
            return title  # Ok to have the same title if this is an edit

        try:
            products.objects.get(title__iexact=title, parent__isnull=True)
        except ObjectDoesNotExist:
            return title
        raise forms.ValidationError('Item name already exist.')

    def save(self, shop):
        is_edit = self.instance.pk is not None
        canonicalProduct = super(ProductCreationForm, self).save(commit=False)
        if not canonicalProduct.upc:
            canonicalProduct.upc = None
        canonicalProduct.shop = shop
        # Jon M TBD - Right now we only use 1 product class - "Apparel"
        canonicalProduct.product_class = get_model('catalogue', 'ProductClass').objects.all()[:1].get()
        canonicalProduct.save()
        canonicalId = canonicalProduct.id

        productCategory = get_model('catalogue', 'ProductCategory').objects.get_or_create(product=canonicalProduct,
                                            category = self.instance.categories.all()[0]
                                                        if is_edit else self.cleaned_data['category'])[0]
        productCategory.category = self.cleaned_data['category']
        productCategory.save()

        if is_edit:
            # Remove all variants since they will get recreated below
            get_model('catalogue', 'Product').objects.filter(parent=canonicalId).delete()


        #if not is_edit:
        # Tommy Leedberg TODO!!!! Make this work for editing images and remove if statement above!!!
        self.save_image_if_needed(canonicalProduct, "product_image", 0)
        self.save_image_if_needed(canonicalProduct, "product_image1", 1)
        self.save_image_if_needed(canonicalProduct, "product_image2", 2)
        self.save_image_if_needed(canonicalProduct, "product_image3", 3)
        self.save_image_if_needed(canonicalProduct, "product_image4", 4)

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

    def save_image_if_needed(self, product, image_field, display_order):
        if self.cleaned_data[image_field] is not None:
            if not self.cleaned_data[image_field]:
                # False means that the clear checkbox was checked
                existing = get_or_none(ProductImage, display_order=display_order, product=product)
                existing.delete()

            else:
                newFileExists = get_or_none(ProductImage, original=self.cleaned_data[image_field].name, product=product)
                if not newFileExists:
                    existing = get_or_none(ProductImage, display_order=display_order, product=product)
                    if existing:
                        existing.delete()
                    productImage = ProductImage(product=product, display_order=display_order)
                    productImage.original = self.cleaned_data[image_field]
                    productImage.save()

    def load_image(self, product, display_order):
        image = get_or_none(ProductImage, product=product, display_order=display_order)
        retVal = None if not image else image.original
        return retVal

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
        if not self.instance.pk or not self.instance.is_top_level:
            return default
        return self.get_value_from_instance(field_name)

    def get_value_from_instance(self, field_name):
        if field_name == 'sizeVariation':
            return self.get_size_variation()
        if field_name == 'price':
            return self.instance.min_variant_price_excl_tax
        if field_name == 'product_image':
            return self.load_image(self.instance.pk, 0)
        if field_name == 'product_image1':
            return self.load_image(self.instance.pk, 1)
        if field_name == 'product_image2':
            return self.load_image(self.instance.pk, 2)
        if field_name == 'product_image3':
            return self.load_image(self.instance.pk, 3)
        if field_name == 'product_image4':
            return self.load_image(self.instance.pk, 4)
        if field_name == 'category':
            categories = self.instance.categories.all()
            return categories[0] if categories.count() > 0 else None
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
    aboutImg = forms.ImageField(required=False, max_length=255, widget=forms.FileInput)

    helper = FormHelper()
    helper.form_show_labels = False
    helper.layout = Layout(
        Div(
            Fieldset('About',
                     HTML("""<p>If no image is selected, clicking submit will clear current about image</p>"""),
                     Field('aboutImg', css_class="autoHeight"),
                     Field('aboutContent', placeholder="Enter Text Here")),
            Submit('aboutBoxForm', 'Submit', css_class='tinvilleButton', css_id="id_SubmitAboutContent"),
            css_class="container col-xs-offset-1 col-xs-10 col-sm-offset-0 col-sm-12 col-lg-8"
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
            css_class="container col-xs-offset-1 col-xs-10 col-sm-offset-0 col-sm-12 col-lg-8"
        ))

    def clean_color(self):
        tinville_color = self.cleaned_data['color']
        if tinville_color == '#f46430':
            raise forms.ValidationError('Tinville Branding is not Allowed to be Used.')
        return tinville_color

class BannerUploadForm(forms.Form):

    banner = forms.ImageField(required=False, max_length=255, widget=forms.FileInput)
    mobileBanner = forms.ImageField(required=False, max_length=255, widget=forms.FileInput)
    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Fieldset('Banner Image',
                     HTML("""<p>If no image is selected, clicking submit will clear current banner</p>
                     <div rel="tooltip" title="info here"><i class="fa fa-question-circle"></i></div>"""),
                     Field('banner', css_class="autoHeight")),
            Fieldset('Mobile Banner Image',
                     HTML("""<p>If no image is selected, clicking submit will clear current banner</p>"""),
                     Field('mobileBanner', css_class="autoHeight")),
            Submit('bannerUploadForm', 'Submit Banner', css_class='tinvilleButton', css_id="id_SubmitBanner"),
            css_class="container col-xs-offset-1 col-xs-10 col-sm-offset-0 col-sm-11 col-lg-6"
        ))

class LogoUploadForm(forms.Form):

    logo = forms.ImageField(required=False, max_length=255, widget=forms.FileInput)

    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Fieldset('Logo Image',
                     HTML("""<p>If no image is selected, clicking submit will clear current logo</p>"""),
                     Field('logo', css_class="autoHeight")),
            Submit('logoUploadForm', 'Submit Logo', css_class='tinvilleButton', css_id="id_SubmitLogo"),
            css_class="container col-xs-offset-1 col-xs-10 col-sm-offset-0 col-sm-12 col-lg-8"
        ))

