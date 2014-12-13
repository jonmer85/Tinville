from crispy_forms import helper
from crispy_forms.bootstrap import AppendedText
from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.apps.address.forms import UserAddressForm as CoreUserAddressForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class UserAddressForm(CoreUserAddressForm):
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
        Field('country', placeholder="Country"),
        Field('phone_number', placeholder="Phone Number")
    )
