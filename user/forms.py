from datetime import datetime
import urlparse
from autoslug.utils import slugify
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy, resolve, Resolver404
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Fieldset, Hidden
from crispy_forms.bootstrap import AppendedText
from parsley.decorators import parsleyfy
from user.models import TinvilleUser
from designer_shop.models import Shop
from custom_oscar.apps.checkout.forms import PaymentInfoForm


class TinvilleUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    shop_name = forms.CharField(label='Shop name', required=False)
    redirect_url = forms.CharField(widget=forms.HiddenInput, required=False)

    helper = FormHelper()
    helper.form_show_labels = False
    
    helper.layout = Layout(
        Div(
            Div(
                HTML("""<div style="padding-top: 25px;"></div>"""),
                HTML('<input type="text" name="prevent_autofill" id="prevent_autofill" value="" style="display:none;" />'),
                HTML('<input type="password" name="password_fake" id="password_fake" value="" style="display:none;" />'),
                Field('email', placeholder="Email"),
                Field('password', placeholder="Password"),
                Field('redirect_url'),
                Div(
                    Field('shop_name', placeholder="Shop name"),
                    id="shop_fields",
                ), css_class=""
            ),
            Div(Div(
                Submit('userForm', 'Register'), css_class=""
            ), css_class="")
        )
    )

    def __init__(self, *args, **kwargs):
        self.host = kwargs.pop('host', None)
        super(TinvilleUserCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TinvilleUser
        fields = ['email', 'password']

    def clean_shop_name(self):
        shop_name = self.cleaned_data['shop_name']
        shop_exists = True
        try:
            Shop.objects.get(name__iexact=shop_name)
        except ObjectDoesNotExist:
            shop_exists = False # return shop_name  # if shop_name doesn't exist, this is good. We can create the shop
        if shop_exists:
            raise forms.ValidationError('Shop name is already taken.')
        # if the shop name resolves to a view that is not the shop.. it is trying to use a url that we already use.. dont let this happen!
        if len(shop_name) > 0 and resolve(urlparse.urlparse('/' + slugify(shop_name.lower()) + '/')[2]).view_name != 'designer_shop.views.shopper':
            raise forms.ValidationError('Not a valid shop name, please choose another')
        return shop_name

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(TinvilleUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        if self.cleaned_data["shop_name"]:
            user.is_seller = True
            user.shop = Shop.objects.create(user=user, name=self.cleaned_data["shop_name"])
            dashboard_access_perm = Permission.objects.get(
                codename='dashboard_access', content_type__app_label='partner')
            user.user_permissions.add(dashboard_access_perm)
            user.save()

        return user

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        if not url:
            return settings.LOGIN_REDIRECT_URL
        host = urlparse.urlparse(url)[1]
        if host and self.host and host != self.host:
            return settings.LOGIN_REDIRECT_URL
        return url


class TinvilleUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = TinvilleUser

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(label="Remember Me", widget=forms.CheckboxInput, initial=True, required=False)
    redirect_url = ''


    def __init__(self, *args, **kwargs):

        if 'redirect_url' in kwargs:
            self.redirect_url = kwargs['redirect_url']
            del kwargs['redirect_url']

        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_show_labels = False
        self.helper.form_class = 'loginPopupForm'
        # self.helper.field_class = 'test'
        hidden_field_name = forms.CharField(label='reset', max_length=256, widget=forms.HiddenInput())
        self.helper.layout = Layout(
            # Jon M TODO Consolidate messages into a common tag that can be loaded in
            Div(
                Div(HTML("""{{ form.non_field_errors }}"""), css_class='messageError message_area'),
                Div(HTML("""<a class="btn btn-facebook col-xs-12 loginFacebookButton"
                            href="social_accounts/facebook/login/?process=login">
                            <i class="fa fa-facebook"></i> | Sign in with Facebook
                        </a>""")),
                Div(HTML("""<a class="btn btn-instagram col-xs-12 loginInstagramButton" style="margin-top: 10px"
                            href="social_accounts/instagram/login/?process=login">
                            <i class="fa fa-instagram"></i> | Sign in with Instagram
                        </a>""")),
                HTML("""<img class="col-xs-12" src="{{ STATIC_URL }}img/or_login.gif" style=" margin-top: 5%; margin-bottom: 5%; "/>"""),
                Div(css_class='clearfix'),
                Div(
                    Field('username', placeholder="Email"),
                    css_class="alignField",
                ),
                Div(
                    Field('password', type='password', placeholder="Password"),
                    css_class="alignField",
                ),
                Div(
                    # Create hidden field which contains redirect url
                    Hidden('next', str(self.redirect_url))
                    # <input type="hidden" name="next" value="{{ this.redirect_url }}" />
                ),


                HTML("""<div for="id_remember_me" id="rememberLoginLabel" class="checkbox">
                        <label>
                            <input checked="checked" class=" checkboxinput" id="id_remember_me" name="remember_me"
                             type="checkbox" value="true">Remember Me
                             </input>
                        </label>
                    </div>"""),
                Submit('submit', 'Sign in', css_class='full-screen btn btn-primary tinvilleButton'),
                HTML("""<div class="formField pull-left loginForgot">
                        <p>Forgot Password?
                        <a href="/password-reset" id="loginForgotPasswordLink" class=""> Reset password</a></p>
                        </div>"""),
                        # <a href="#" id="loginForgotUsernameLink" class=" ">username</a>
                        #  or
                Div(css_class='clearfix'),
                HTML("""<div class="formField pull-left loginRegister">
                        <p>Don't have an Account?
                        <a href="/register" id="loginRegisterLink" class=" ">Register</a></p>
                        </div>""")
            )
        )

    def clean_username(self):
            return self.cleaned_data['username'].lower()

@parsleyfy
class PaymentInfoFormWithFullName(PaymentInfoForm):
    RECIPIENT_CHOICES = (
        ('1', 'Individual'),
        ('2', 'Business/Corporation'),
    )

    PAYMENT_CHOICES = (
        ('1', 'Debit Card'),
        ('2', 'Bank Account')
    )

    recipient_type = forms.ChoiceField(choices=RECIPIENT_CHOICES)
    payment_choice = forms.ChoiceField(choices=PAYMENT_CHOICES)
    tax_id = forms.CharField(max_length=11)
    full_legal_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    bank_account_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'data-stripe': 'number',
                                                                'pattern': '\d*', 'autocomplete': 'off',
                                                                'data-parsley-accountNum': 'data-parsley-accountNum'}))
    routing_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'data-stripe': 'number',
                                                                'pattern': '\d*', 'autocomplete': 'off',
                                                                'data-parsley-routingNum': 'data-parsley-routingNum'}))

    def __init__(self, *args, **kwargs):
        super(PaymentInfoFormWithFullName, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Div(
                PaymentInfoForm.header_payment_layout,
                Field('recipient_type'),
                Field('full_legal_name',  placeholder="Full Legal Name", css_class='input-group'),
                Field('tax_id',  placeholder="Tax ID (SSN or EIN if business/corporation)", css_class='input-group'),
                Field('payment_choice'),
                Div(
                    Div(
                        PaymentInfoForm.base_payment_layout,
                        css_class='hidden',
                        css_id="debitCard"
                    ),
                    Div(
                        Field('bank_account_number', placeholder="Bank Account Number"),
                        Field('routing_number', placeholder="Routing Number"),
                        css_class="hidden",
                        css_id="bankAccount"
                    ),
                ),
                Submit('payment-info', 'Submit', css_class='btn btn-primary col-xs-12', style='margin-top: 10px')
            )
        )

@parsleyfy
class BetaAccessForm(forms.Form):
    def clean_access_code(self):
        access_code_candidate = self.cleaned_data['access_code']

        try:
            TinvilleUser.objects.get(access_code = access_code_candidate)
        except ObjectDoesNotExist:
            raise forms.ValidationError('Incorrect Access Code')
        return access_code_candidate


    access_code = forms.CharField(max_length=5)
    shop = forms.CharField(widget=forms.HiddenInput, required=False)

    helper = FormHelper()
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Field('access_code', placeholder="Beta Access Code"),
            HTML('<input type="hidden" name="shop" value="{{ shop }}">'),
            Submit('betaForm', 'Submit', css_class='btn btn-primary', style='margin-top: 10px')
        )
    )
