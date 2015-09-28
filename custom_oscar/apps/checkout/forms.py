from crispy_forms import helper
from crispy_forms.bootstrap import AppendedText
from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.apps.dashboard.orders.views import *
from oscar.apps.checkout.forms import GatewayForm as CoreGatewayForm, ShippingAddressForm as CoreShippingAddressForm
from oscar.apps.checkout.forms import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Hidden, Fieldset
from parsley.decorators import parsleyfy

import easypost
import logging
logger = logging.getLogger(__name__)

class GatewayForm(CoreGatewayForm):
    helper = FormHelper()
    helper.form_show_labels = False
    helper.form_tag = False

    helper.layout = Layout(
        Field('username', placeholder="Email"),
        # Field('options', placeholder="Options"),
        Field('password', placeholder="Password"),
        Hidden('form', 'submitted-form'))

    GUEST, NEW, EXISTING = 'anonymous', 'new', 'existing'
    CHOICES = (
        (GUEST, _('I am a new customer and want to checkout as a guest')),
        (NEW, _('I am a new customer and want to create an account '
                'before checking out')),
        (EXISTING, _('I am a returning customer, and my password is')))
    # options = forms.ChoiceField(widget=forms.widgets.RadioSelect,
    #                             choices=CHOICES, initial=GUEST)

class GatewayFormGuest(CoreGatewayForm):
    helper = FormHelper()
    helper.form_show_labels = False
    helper.form_tag = False
    helper.layout = Layout(
        Field('username', placeholder="Email"),
        Hidden('form2', 'submitted-form'))

@parsleyfy
class ShippingAddressForm(CoreShippingAddressForm):
    helper = FormHelper()
    helper.form_show_labels = False
    first_name = forms.CharField(label='First Name', error_messages={'required': 'Please enter your first name.'})
    last_name = forms.CharField(label='Last Name', error_messages={'required': 'Please enter your last.'})
    line1 = forms.CharField(label='Address', error_messages={'required': 'Please enter an address.'})
    line4 = forms.CharField(label='City', error_messages={'required': 'Please enter a city.'})
    state = forms.CharField(label='State', max_length='2', error_messages={'required': 'Please enter a state.',
                'maxlength': 'Please use the abbreviated version of the state name.'})
    postcode = forms.CharField(label='Zip Code', error_messages={'required': 'Please enter a United States zip code.'})

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

@parsleyfy
class PaymentInfoForm(forms.Form):
    stripe_token = forms.CharField()
    card_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'data-stripe': 'number',
                                                                'pattern': '\d*', 'autocomplete': 'off',
                                                                'data-parsley-cardNum': 'data-parsley-cardNum'}))

    expiration_date = forms.CharField(required=False, widget=forms.TextInput(attrs={'data-stripe': 'exp-date',
                                                                     'pattern': '\d*', 'autocomplete': 'off',
                                                                     'data-parsley-group': 'cardexpiry',
                                                                     'data-parsley-cardexpiry': 'data-parsley-cardexpiry'}))

    cvc = forms.CharField(required=False, max_length=4, widget=forms.PasswordInput(attrs={'data-stripe': 'cvc',
                                                                         'pattern': '\d*', 'autocomplete': 'off',
                                                                         'data-parsley-cardcvc': 'cardcvc'}))

    helper = FormHelper()
    helper.form_id = 'payment-info-form'
    helper.form_class = 'parsley-form'
    helper.form_show_labels = False
    helper.attrs = {'autocomplete': 'off'}
    # helper.form_action = reverse_lazy('checkout:payment-details')
    header_payment_layout = Layout(
        Div(HTML('<span class="payment-errors bg-danger"></span>'), style="margin-bottom:10px")
    )

    base_payment_layout = Layout(
        Div(
            Field('card_number', placeholder="Valid Card Number"),
            # Jon - IMPORTANT! DO not remove, this is to trick Chrome into "autofilling" hidden fields since it ignores autofill="off"
            HTML('<input type="text" name="prevent_autofill" id="prevent_autofill" value="" style="display:none;" />'),
            HTML('<input type="password" name="password_fake" id="password_fake" value="" style="display:none;" />'),
            Div(
                Fieldset('Expiration Date',
                         Div(
                             Div(Field('expiration_date', placeholder="MM-YY"), css_class='col-xs-12', autocomplete='off'),
                             css_class="row"
                         ),
                         css_class='col-xs-6'
                ),
                Fieldset('CV Code',
                    Div(
                        HTML('<input type="password" name="password_fake" id="password_fake" value="" style="display:none;" data-parsley-ui-enabled="false"/>'),
                        Div(Field('cvc', placeholder="CV Code"), css_class='col-xs-12', autocomplete='off'),
                        css_class="row"
                    ),
                    css_class='col-xs-6'),
                css_class="row"
            ),
        )
    )

    helper.layout = base_payment_layout

@parsleyfy
class PaymentInfoFormWithTotal(PaymentInfoForm):
    full_legal_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

    def __init__(self, authenticated=False, *args, **kwargs):
        super(PaymentInfoFormWithTotal, self).__init__(*args, **kwargs)
        save_for_later = ''
        if authenticated:
            save_for_later = '<input type="checkbox" name="save_for_later"/> Save Card for Future Use'

        self.helper.layout = Layout(
            Div(
                PaymentInfoForm.header_payment_layout,
                PaymentInfoForm.base_payment_layout,
                Field('field_name', type="checkbox"),
                HTML(save_for_later),
                Submit('paymentForm', 'Pay {{ payment_currency }}{{ total }}', css_class='btn btn-primary col-xs-12', style='margin-top: 10px')
            )
        )

