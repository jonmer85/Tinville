from crispy_forms import helper
from crispy_forms.bootstrap import AppendedText
from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.apps.address.forms import UserAddressForm as CoreUserAddressForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from oscar.core.loading import get_model
from django.conf import settings
import easypost

import logging
logger = logging.getLogger(__name__)

Country = get_model('address', 'Country')

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

        #Generate the easpost api key for address validation
        easypost.api_key = settings.EASYPOST_API_KEY

        if {'first_name', 'last_name', 'line1', 'line4', 'state', 'postcode'}.issubset(self.cleaned_data):

            try:
                verified_address = easypost.Address.create_and_verify(
                    name=self.cleaned_data['first_name'] + ' ' + self.cleaned_data['last_name'],
                    street1=self.cleaned_data['line1'],
                    city=self.cleaned_data['line4'],
                    state=self.cleaned_data['state'],
                    zip=self.cleaned_data['postcode'],
                    country='US')
                if(self.cleaned_data['state'].lower() != verified_address.state.lower()):
                    raise forms.ValidationError(_('Invalid state: %s') % self.cleaned_data['state'])
                if(self.cleaned_data['line4'].lower() != verified_address.city.lower()):
                    raise forms.ValidationError(_('Invalid city: %s') % self.cleaned_data['line4'])
            except Exception, Argument:
                logger.info( "custom_oscar.apps.checkout.forms.ShippingAddressForm.clean(): failed to verify address")
                raise forms.ValidationError(_('Please enter a valid address. %s') % Argument.message )


    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Field('first_name', placeholder="First Name"),
        Field('last_name', placeholder="Last Name"),
        Field('line1', placeholder="First Line of Address"),
        Field('line2', placeholder="Second Line of Address"),
        Field('line3', placeholder="Third Line of Address"),
        Field('line4', placeholder="City"),
        Field('state', placeholder="State"),
        Field('postcode', placeholder="Zip code"),
        # Field('country', placeholder="Country"),
        Field('phone_number', placeholder="Phone Number")
    )
