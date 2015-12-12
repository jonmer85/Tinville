from crispy_forms import helper
from crispy_forms.bootstrap import AppendedText
from django import forms
from django.forms import Form
from django.utils.translation import ugettext_lazy as _

from oscar.apps.address.forms import UserAddressForm as CoreUserAddressForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit
from oscar.core.loading import get_model
from django.conf import settings
from parsley.decorators import parsleyfy
import easypost

import logging
logger = logging.getLogger(__name__)

Country = get_model('address', 'Country')

@parsleyfy
class UserAddressForm(CoreUserAddressForm):
    def __init__(self, *args, **kwargs):
        super(UserAddressForm, self).__init__(*args, **kwargs)
        self.adjust_country_field()

    def adjust_country_field(self):
        countries = Country._default_manager.filter(
            is_shipping_country=True)

        # No need to show country dropdown if there is only one option
        if len(countries) == 1:
            self.fields.pop('country', None)
            self.instance.country = countries[0]
        else:
            self.fields['country'].queryset = countries
            self.fields['country'].empty_label = None

    def clean(self):

        # Generate the easypost api key for address validation
        easypost.api_key = settings.EASYPOST_API_KEY

        if {'first_name', 'last_name', 'line1', 'line4', 'state', 'postcode'}.issubset(self.cleaned_data):

            strName=self.cleaned_data['first_name'].strip() + ' ' + self.cleaned_data['last_name'].strip()
            strStreet1=self.cleaned_data['line1'].strip()
            strStreet2=self.cleaned_data['line2'].strip()
            strStreet3=self.cleaned_data['line3'].strip()
            strCity=self.cleaned_data['line4'].strip().lower()
            strState=self.cleaned_data['state'].strip().lower()
            strZip=self.cleaned_data['postcode'].strip()

            try:
                verified_address = easypost.Address.create_and_verify(
                    name=strName,
                    street1=strStreet1,
                    street2=strStreet2,
                    street3=strStreet3,
                    city=strCity,
                    state=strState,
                    zip=strZip,
                    country='US')
                if(strState != verified_address.state.lower()):
                    raise forms.ValidationError(_('Invalid state: %s') % strState)
                if(strCity != verified_address.city.lower()):
                    raise forms.ValidationError(_('Invalid city: %s') % strCity)
            except Exception, Argument:
                logger.info( "custom_oscar.apps.checkout.forms.ShippingAddressForm.clean(): failed to verify address")
                raise forms.ValidationError(_('Please enter a valid address. %s') % Argument.message )

    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Field('first_name', placeholder="First Name"),
            Field('last_name', placeholder="Last Name"),
            Field('line1', placeholder="First Line of Address"),
            Field('line2', placeholder="Second Line of Address"),
            Field('line3', placeholder="Third Line of Address"),
            Field('line4', placeholder="City"),
            Field('state', placeholder="State", maxlength="2"),
            Field('postcode', placeholder="Zip code"),
            # Field('country', placeholder="Country"),
            Field('phone_number', placeholder="Phone Number"),
        css_class="container col-xs-12 col-sm-offset-3 col-sm-6"
        ))

class GeneratePromoCodeForm(Form):
    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Submit('submit', 'Generate my promo code!', css_class='btn btn-primary btn-lg')
        ))
