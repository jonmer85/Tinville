from crispy_forms import helper
from crispy_forms.bootstrap import AppendedText
from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.apps.checkout.forms import GatewayForm as CoreGatewayForm, ShippingAddressForm as CoreShippingAddressForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Hidden, Fieldset


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


class PaymentInfoForm(forms.Form):
    stripe_token = forms.CharField()
    last4 = forms.CharField(max_length=4, min_length=4)
    card_number = forms.CharField(required=True,
                                  widget=forms.TextInput(attrs={'data-stripe': 'number',
                                                                'pattern': '\d*', 'autocomplete': 'off'}))
    expiration_month = forms.CharField(required=True, max_length=2,
                                       widget=forms.TextInput(attrs={'data-stripe': 'exp-month',
                                                                     'pattern': '\d*', 'autocomplete': 'off'}))
    expiration_year = forms.CharField(required=True, max_length=2,
                                       widget=forms.TextInput(attrs={'data-stripe': 'exp-year',
                                                                     'pattern': '\d*', 'autocomplete': 'off'}))
    cvc = forms.CharField(required=True, max_length=4,
                                       widget=forms.PasswordInput(attrs={'data-stripe': 'cvc',
                                                                         'pattern': '\d*', 'autocomplete': 'off'}))

    helper = FormHelper()
    helper.form_id = 'payment-info-form'
    helper.form_show_labels = False
    # helper.form_action = reverse_lazy('checkout:payment-details')

    base_payment_layout = Layout(
        Div(
            AppendedText('card_number',  '<span class="glyphicon glyphicon-lock"></span>',
                         placeholder="Valid Card Number"),
            Div(
                Fieldset('Expiration Date',
                    Div(Field('expiration_month', placeholder="MM"), css_class='col-xs-5', style='padding-left: 0'),
                    Div(Field('expiration_year', placeholder="YY"), css_class=' col-xs-offset-2 col-xs-5', style='padding-right: 0'),
                    css_class='col-xs-5', style='padding-left: 0'
                ),
                Fieldset('CV Code',
                    Div(Field('cvc', placeholder="CV Code"), css_class='col-xs-8', style='padding-left: 0'),
                    css_class='col-xs-offset-2 col-xs-5', style='padding-right: 0')
            ),
            Submit('paymentForm', 'Submit')
        )
    )

    helper.layout = base_payment_layout