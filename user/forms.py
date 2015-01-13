from datetime import datetime
import urlparse
from autoslug.utils import slugify

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy, resolve, Resolver404

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Fieldset
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
                Field('email', placeholder="Email"),
                Field('password', placeholder="Password"),
                Field('redirect_url'),
                Div(
                    Field('shop_name', placeholder="Shop name"),
                    id="shop_fields",
                ), css_class=""
            ),
            Div(Div(
                Submit('userForm', 'Register'), css_class="container col-xs-offset-2 col-xs-8 col-sm-offset-3 col-sm-4"
            ), css_class="row")
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

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_show_labels = False
        self.helper.form_class = 'loginPopupForm'
        # self.helper.field_class = 'test'

        self.helper.layout = Layout(
            # Jon M TODO Consolidate messages into a common tag that can be loaded in
            Div(
                Div(HTML("""{{ form.non_field_errors }}"""), css_class='messageError message_area'),
                # Div(HTML("""<a id="loginFacebookButton" class="btn btn-facebook col-xs-12">
                #             <i class="icon-facebook"></i> | Sign in with Facebook
                #         </a""")),
                # HTML("""<img class="col-xs-12" src="{{ STATIC_URL }}img/or_login.gif" style=" margin-top: 5%; margin-bottom: 5%; "/>"""),
                Div(css_class='clearfix'),
                Div(
                    Field('username', placeholder="Email"),
                    css_class="alignField",
                ),
                Div(
                    Field('password', type='password', placeholder="Password"),
                    css_class="alignField",
                ),


                HTML("""<div for="id_remember_me" id="rememberLoginLabel" class="checkbox">
                        <label>
                            <input checked="checked" class=" checkboxinput" id="id_remember_me" name="remember_me"
                             type="checkbox" value="true">Remember Me
                             </input>
                        </label>
                    </div>"""),
                Submit('submit', 'Sign in', css_class='full-screen btn btn-primary tinvilleButton'),
                # HTML("""<div class="formField pull-left loginForgot">
                #         <p>Forgot
                #         <a href="#" id="loginForgotUsernameLink" class=" ">username</a>
                #          or
                #         <a href="#" id="loginForgotPasswordLink" class="">password?</a></p>
                #         </div>"""),
                # Div(css_class='clearfix'),
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
    full_legal_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

    def __init__(self, *args, **kwargs):
        super(PaymentInfoFormWithFullName, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Div(
                PaymentInfoForm.header_payment_layout,
                Field('full_legal_name',  placeholder="Full Legal Name", css_class='input-group'),
                PaymentInfoForm.base_payment_layout,
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
