from datetime import datetime

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Hidden
from crispy_forms.bootstrap import AppendedText

from user.models import TinvilleUser
from designer_shop.models import Shop

class TinvilleUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    helper = FormHelper()
    helper.form_show_labels = False
    helper.form_class = 'form-horizontal'
    helper.field_class = 'col-xs-12 col-sm-8 col-sm-offset-2'
    
    helper.layout = Layout(
        Field('email', placeholder="Email"),
        Field('password', placeholder="Password"),
        Field('password2', placeholder="Confirm password"),
        Field('is_seller', template="apply_for_shop.html", required=False),
        Div(
            Field('shop_name', placeholder="Shop name"),
            id="shop_fields",
        ),
        Submit('userForm', 'Register', css_class='tinvilleButton registerButton')
    )

    class Meta:
        model = TinvilleUser
        fields = ['email', 'password', 'is_seller', 'shop_name']

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(TinvilleUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        if user.is_seller:
            user.shop = Shop.objects.create(user=user, name=self.cleaned_data['shop_name'])

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
                Div(HTML("""{{ form.non_field_errors }}"""), css_id='message_area', css_class='messageError'),
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
