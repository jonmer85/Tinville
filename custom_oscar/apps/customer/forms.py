from crispy_forms import helper
from crispy_forms.bootstrap import AppendedText
from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.apps.address.forms import UserAddressForm as CoreUserAddressForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from oscar.core.loading import get_model

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