from copy import copy
import uuid
from django import forms
from django.core.files.base import ContentFile
from django.forms import inlineformset_factory
from django_bleach.forms import BleachField

from oscar.core.loading import get_model
from django.core.exceptions import ObjectDoesNotExist

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Fieldset, HTML, Button, Hidden
from crispy_forms.bootstrap import PrependedText, Accordion, AccordionGroup
from tinymce.widgets import TinyMCE
from color_utils import widgets
from django.core.validators import RegexValidator
from parsley.decorators import parsleyfy
from image_cropping import ImageCropWidget

from .models import SIZE_DIM, SIZE_NUM, SIZE_SET, SIZE_TYPES, Shop
from common.utils import get_or_none
from common.widgets import AdvancedFileInput, TinvilleImageCropWidget


SIZE_TYPES_AND_EMPTY = [('', 'How is this item sized?')] + SIZE_TYPES

Product = get_model("catalogue", "Product")
ProductImage = get_model("catalogue", "ProductImage")

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

        self.fields['price'] \
            = forms.DecimalField(decimal_places=2, max_digits=12, initial=self.get_value_if_in_edit_mode('price', None))

        self.helper = FormHelper()
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(Accordion(
                    AccordionGroup('General',
                             Field('title', placeholder='Title', data_parsley_group="General"),
                             AccordionGroup('Description',
                                            Field('description', placeholder='Description'), style="padding-bottom: 10px"),
                             Field('category', placeholder='Choose a Category', data_parsley_group="General"),
                             Field('price', placeholder='Price', data_parsley_group="General")
                    ),
                    AccordionGroup('Images',
                             HTML("""<p>Select up to 5 images for this item. Image size recommendations are 400x500</p>"""),
                             HTML('{% load crispy_forms_tags %}{% crispy productImageFormSet %}'),
                    ),
                    AccordionGroup('Sizes and Colors',
                             Field('sizeVariation', placeholder='Choose a variation', data_parsley_group="SizeAndColor"),
                             Div(
                                 Fieldset('Sizes', css_id="sizesFieldSet", css_class="hidden")),
                             css_class="accordion", css_id="accordion2"),
                    ),
                Submit('productCreationForm', 'Edit' if self.instance.pk else 'Create', css_class='tinvilleButton'),
                css_class="container col-xs-12",
                css_id="addItemEditor"
            )

        )

        self.fields['description'] = BleachField(required=False)
        self.fields['description'].widget = TinyMCE()
        self.fields['category'] = forms.ModelChoiceField(queryset=get_model('catalogue', 'Category').objects.filter(depth=3),
                                                         empty_label="Choose a Category", required=True,
                                                         initial=self.get_value_if_in_edit_mode('category', None))
        self.fields['price'].label = ""

        # Jon M TBD - Right now we only use 1 product class - "Apparel"
        self.instance.product_class = get_model('catalogue', 'ProductClass').objects.all()[:1].get()

        if sizes:
            for i, size in enumerate(sizes):
                if "sizeSet" in sizes[i] and sizes[i]["sizeSet"]:
                    self.fields[sizes[i]["sizeFieldName"]] \
                        = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                                      objects.filter(group=1), empty_label="Choose a size...", required=True, initial=sizes[i]["sizeSet"])
                    for j, colorAndQuantity in enumerate(sizes[i]["colorsAndQuantities"]):
                        if colorAndQuantity['color'] and colorAndQuantity['quantity']:
                            self.fields[colorAndQuantity['colorFieldName']] \
                            = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                                          objects.filter(group=2), empty_label="Choose a color...",
                                                     initial=sizes[i]["colorsAndQuantities"][j]["color"], required=False)
                            self.fields[colorAndQuantity['quantityFieldName']] \
                            = forms.IntegerField(initial=sizes[i]["colorsAndQuantities"][j]["quantity"], required=False)

                elif "sizeX" in sizes[i] and sizes[i]["sizeX"] and "sizeY" in sizes[i] and sizes[i]["sizeY"]:
                    self.fields[sizes[i]["sizeFieldNameX"]] \
                        = forms.DecimalField(initial=sizes[i]["sizeX"])
                    self.fields[sizes[i]["sizeFieldNameY"]] \
                        = forms.DecimalField(initial=sizes[i]["sizeY"])
                    for j, colorAndQuantity in enumerate(sizes[i]["colorsAndQuantities"]):
                        self.fields[colorAndQuantity['colorFieldName']] \
                        = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                                      objects.filter(group=2), empty_label="Choose a color...",
                                                 initial=sizes[i]["colorsAndQuantities"][j]["color"])
                        self.fields[colorAndQuantity['quantityFieldName']] \
                        = forms.IntegerField(initial=sizes[i]["colorsAndQuantities"][j]["quantity"])

                elif "sizeNum" in sizes[i] and sizes[i]["sizeNum"]:
                    self.fields[sizes[i]["sizeFieldName"]] \
                        = forms.DecimalField(initial=sizes[i]["sizeNum"])
                    for j, colorAndQuantity in enumerate(sizes[i]["colorsAndQuantities"]):
                        self.fields[colorAndQuantity['colorFieldName']] \
                        = forms.ModelChoiceField(queryset=get_model('catalogue', 'AttributeOption').
                                                      objects.filter(group=2), empty_label="Choose a color...",
                                                 initial=sizes[i]["colorsAndQuantities"][j]["color"])
                        self.fields[colorAndQuantity['quantityFieldName']] \
                        = forms.IntegerField(initial=sizes[i]["colorsAndQuantities"][j]["quantity"])


    def create_variant_product_from_canonical(self, canonical, canonicalId, shop, sizeSet=None, sizeDim=None, sizeNum=None, color=None, quantity=None):
        variantProduct = copy(canonical)
        #IMPORTANT: The setting of the canonical id to the parent_id has to come before the clearing since it is the same reference!!!
        variantProduct.parent_id = canonicalId
        variantProduct.structure = Product.CHILD
        variantProduct.pk = None
        variantProduct.id = None
        variantProduct.save()
        variantProduct.attr.product = variantProduct # Switch attributes to the variant
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
        products = Product

        if self.instance.pk and self.get_value_from_instance("title") == title:
            return title  # Ok to have the same title if this is an edit

        try:
            products.objects.get(title__iexact=title, parent__isnull=True)
        except ObjectDoesNotExist:
            return title
        raise forms.ValidationError('Item name already exist.')

    def save(self, shop, sizes, sizeType):
        is_edit = self.instance.pk is not None
        canonicalProduct = super(ProductCreationForm, self).save(commit=False)
        if not canonicalProduct.upc:
            canonicalProduct.upc = None
        canonicalProduct.shop = shop
        canonicalProduct.structure = Product.PARENT

        canonicalProduct.save()
        canonicalId = canonicalProduct.id

        productCategory = get_model('catalogue', 'ProductCategory').objects.get_or_create(product=canonicalProduct,
                                            category = self.instance.categories.all()[0]
                                                        if is_edit else self.cleaned_data['category'])[0]
        productCategory.category = self.cleaned_data['category']
        productCategory.save()

        if is_edit:
            # Remove all variants since they will get recreated below
            Product.objects.filter(parent=canonicalId).delete()


        for size in sizes:
            if sizeType == SIZE_SET:
                if size["sizeFieldName"] in self.cleaned_data:
                    sizeSet = self.cleaned_data[size["sizeFieldName"]]
                    for colorQuantity in size["colorsAndQuantities"]:
                        if colorQuantity["colorFieldName"] in self.cleaned_data and colorQuantity["quantityFieldName"] in self.cleaned_data:
                            color = self.cleaned_data[colorQuantity["colorFieldName"]]
                            quantity = self.cleaned_data[colorQuantity["quantityFieldName"]]
                            self.create_variant_product_from_canonical(canonicalProduct, canonicalId, shop, sizeSet=sizeSet,
                                                                       color=color, quantity=quantity)
                        else:
                            # Jon M TBD Should we allow no color/quantity?
                            # For now ignore it
                            pass
            # Tom Bowman was here 5-25-14
            elif sizeType == SIZE_DIM:
                if size["sizeFieldNameX"] in self.cleaned_data and size["sizeFieldNameY"] in self.cleaned_data:
                    sizeDimX = self.cleaned_data[size["sizeFieldNameX"]]
                    sizeDimY = self.cleaned_data[size["sizeFieldNameY"]]
                    for colorQuantity in size["colorsAndQuantities"]:
                        if colorQuantity["colorFieldName"] in self.cleaned_data and colorQuantity["quantityFieldName"] in self.cleaned_data:
                            color = self.cleaned_data[colorQuantity["colorFieldName"]]
                            quantity = self.cleaned_data[colorQuantity["quantityFieldName"]]
                            self.create_variant_product_from_canonical(canonicalProduct, canonicalId, shop, sizeDim={"x": sizeDimX,
                                                                            "y": sizeDimY}, color=color, quantity=quantity)
                        else:
                            # Jon M TBD Should we allow no color/quantity?
                            # For now ignore it
                            pass
            elif sizeType == SIZE_NUM:
                if size["sizeFieldName"] in self.cleaned_data:
                    sizeNum = self.cleaned_data[size["sizeFieldName"]]
                    for colorQuantity in size["colorsAndQuantities"]:
                        if colorQuantity["colorFieldName"] in self.cleaned_data and colorQuantity["quantityFieldName"] in self.cleaned_data:
                            color = self.cleaned_data[colorQuantity["colorFieldName"]]
                            quantity = self.cleaned_data[colorQuantity["quantityFieldName"]]
                            self.create_variant_product_from_canonical(canonicalProduct, canonicalId, shop, sizeNum=sizeNum,
                                                                       color=color, quantity=quantity)
                        else:
                            # Jon M TBD Should we allow no color/quantity?
                            # For now ignore it
                            pass
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
        if not self.instance.pk or not self.instance.is_top_level:
            return default
        return self.get_value_from_instance(field_name)

    def get_value_from_instance(self, field_name):
        if field_name == 'sizeVariation':
            return self.get_size_variation()
        if field_name == 'price':
            return self.instance.min_variant_price_excl_tax
        if field_name == 'category':
            categories = self.instance.categories.all()
            return categories[0] if categories.count() > 0 else None
        else:
            return getattr(self.instance, field_name)

    class Meta:
        model = Product
        fields = ['title', 'description']
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

class ProductImageForm(forms.ModelForm):

    helper = FormHelper()
    # helper.form_tag = False
    helper.form_show_labels = False


    class Meta:
        model = ProductImage
        exclude = ('display_order', 'caption')

        widgets = {
            'original': TinvilleImageCropWidget,
        }

    def save(self, *args, **kwargs):
        # We infer the display order of the image based on the order of the
        # image fields within the formset.
        kwargs['commit'] = False
        obj = super(ProductImageForm, self).save(*args, **kwargs)
        obj.display_order = self.get_display_order()
        obj.save()
        return obj

    def get_display_order(self):
        return self.prefix.split('-').pop()

    def has_changed(self):
        """
        Returns True if data differs from initial.
        """
        return bool(self.changed_data) \
            and not (len(self.changed_data) == 1 and self.changed_data[0] == 'cropping' and self.empty_permitted)

    def __init__(self, *args, **kwargs):
        super(ProductImageForm, self).__init__(*args, **kwargs)


BaseProductImageFormSet = inlineformset_factory(
    Product, ProductImage, form=ProductImageForm, extra=4, can_delete=True, max_num=5, min_num=1, validate_min=True, validate_max=True)


class ProductImageFormSet(BaseProductImageFormSet):

    def __init__(self, *args, **kwargs):
        super(ProductImageFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.fields["original"].label = ""
            form.fields["cropping"].label = ""

class AboutBoxForm(forms.ModelForm):

    # aboutContent = BleachField(widget=TinyMCE( attrs = { 'cols': 50, 'rows': 30 }))
    # aboutImg = forms.ImageField(required=False, max_length=255, widget=AdvancedFileInput)
    # aboutImgCropped = forms.CharField(required=False)

    helper = FormHelper()
    helper.form_show_labels = False
    helper.layout = Layout(
        Div(
            # AccordionGroup('About',
             HTML("""<p>If no image is selected, clicking submit will clear current about image</p>"""),
             Field('aboutImg', css_class="autoHeight"),
             Field('aboutImgCropping'),
             Field('aboutContent', placeholder="Enter Text Here"),
            # ),
            Submit('aboutBoxForm', 'Submit', css_class='tinvilleButton', css_id="id_SubmitAboutContent"),
            css_class="container col-xs-12"
        ))

    def __init__(self, *args, **kwargs):
        super(AboutBoxForm, self).__init__(*args, **kwargs)

        self.fields['aboutContent'].widget = TinyMCE( attrs = { 'cols': 50, 'rows': 30 })


    class Meta:
        model = Shop
        fields = ['aboutImg', 'aboutContent', 'aboutImgCropping']
        widgets = {
            'aboutImg': TinvilleImageCropWidget,
        }

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
            css_class="container col-xs-12"
        ))

    def clean_color(self):
        tinville_color = self.cleaned_data['color']
        if tinville_color == '#f46430':
            raise forms.ValidationError('Tinville Branding is not Allowed to be Used.')
        return tinville_color

class BannerUploadForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Fieldset('Banner Image',
                     HTML("""<p>If no image is selected, clicking submit will clear current banner</p>
                     <div rel="tooltip" title="info here"></div>"""),
                     Field('banner', css_class="autoHeight"),
                     Field('bannerCropping')),

            Fieldset('Mobile Banner Image',
                     HTML("""<p>If no image is selected, clicking submit will clear current banner</p>"""),
                     Field('mobileBanner', css_class="autoHeight"),
                     Field('mobileBannerCropping')),
            Submit('bannerUploadForm', 'Submit Banner', css_class='tinvilleButton', css_id="id_SubmitBanner"),
            css_class="container col-xs-12"
        ))

    class Meta:
        model = Shop
        fields = ['banner', 'mobileBanner', 'bannerCropping', 'mobileBannerCropping']
        widgets = {
            'banner': TinvilleImageCropWidget,
            'mobileBanner': TinvilleImageCropWidget,
        }

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
            css_class="container col-xs-12"
        ))

