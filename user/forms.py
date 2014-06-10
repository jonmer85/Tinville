from datetime import datetime

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Hidden
from crispy_forms.bootstrap import AppendedText

from user.models import TinvilleUser
from designer_shop.models import Shop


class TinvilleUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    shop_name = forms.CharField(label='Shop name', required=False)

    helper = FormHelper()
    helper.form_show_labels = False
    
    helper.layout = Layout(
        Field('email', placeholder="Email"),
        Field('password', placeholder="Password"),
        Div(
            Field('shop_name', placeholder="Shop name"),
            id="shop_fields",
        ),
        Submit('userForm', 'Register')
    )

    class Meta:
        model = TinvilleUser
        fields = ['email', 'password']

    def clean_shop_name(self):
        shop_name = self.cleaned_data['shop_name']

        try:
            Shop.objects.get(name__iexact=shop_name.lower())
        except ObjectDoesNotExist:
            return shop_name  # if shop_name doesn't exist, this is good. We can create the shop
        raise forms.ValidationError('Shop name is already taken.')

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
                Div(HTML("""<a id="loginFacebookButton" class="btn btn-facebook col-xs-12">
                            <i class="icon-facebook"></i> | Sign in with Facebook
                        </a""")),
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


                HTML("""<div for="id_remember_me" id="rememberLoginLabel" class=" checkbox">
                        <input checked="checked" class=" checkboxinput" id="id_remember_me" name="remember_me"
                         type="checkbox" value="true">
                        Remember Me </input>
                    </div>"""),
                Submit('submit', 'Sign in', css_class='btn btn-primary tinvilleButton col-xs-12'),
                HTML("""<div class="formField pull-left loginForgot">
                        <p>Forgot
                        <a href="#" id="loginForgotUsernameLink" class=" ">username</a>
                         or
                        <a href="#" id="loginForgotPasswordLink" class="">password?</a></p>
                        </div>"""),
                Div(css_class='clearfix'),
                HTML("""<div class="formField pull-left loginRegister">
                        <p>Don't have an Account?
                        <a href="/register" id="loginRegisterLink" class=" ">Register</a></p>
                        </div>""")

            )
        )

    def clean_username(self):
            return self.cleaned_data['username'].lower()
