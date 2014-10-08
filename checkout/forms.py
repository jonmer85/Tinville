from crispy_forms import helper
from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.apps.checkout.forms import GatewayForm as CoreGatewayForm, ShippingAddressForm as CoreShippingAddressForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Hidden


class GatewayForm(CoreGatewayForm):
    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Field('username', placeholder="Email"),
        Field('options', placeholder="Options"),
        Field('password', placeholder="Password")
    )

class ShippingAddressForm(CoreShippingAddressForm):
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