from datetime import datetime

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Hidden

from Tinville.user.models import TinvilleUser

class TinvilleUserCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        request = kwargs.pop("request", None)

        super(TinvilleUserCreationForm, self).__init__(*args, **kwargs)

        self.isDesigner = False

        self.fields['shop_name'].required = False


        self.helper = FormHelper()
        self.helper.form_show_labels = False



    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = TinvilleUser
        # fields = ('email',
        #           'first_name',
        #           'last_name',
        #           'middle_name',
        #           'is_seller',
        #           'other_site_url',
        #           'shop_name'
        #         )

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
        user.is_seller = self.isDesigner
        if commit:
            user.save()
        return user


class TinvilleShopperCreationForm(TinvilleUserCreationForm):

    def __init__(self, *args, **kwargs):
        super(TinvilleShopperCreationForm, self).__init__(*args, **kwargs)

        self.isDesigner = False

        self.fields['shop_name'].required = False

        self.helper.layout = Layout(
            Div(
                Field('first_name', placeholder="First name", css_class="col-xs-12 formField registerField"),
                Field('last_name', placeholder="Last name", css_class="col-xs-12 formField registerField"),
                Hidden('last_login', datetime.now()),
                Field('email', placeholder="Email", css_class="col-xs-12 formField registerField"),
                Field('password', placeholder="Password", css_class="col-xs-12 formField registerField"),
                Field('password2', placeholder="Confirm password", css_class="col-xs-12 formField registerField"),
                Submit('submit', 'Register', css_class='registerButton tinvilleButton registerField formField pull-right')
            )
        )

class TinvilleDesignerCreationForm(TinvilleUserCreationForm):

    def __init__(self, *args, **kwargs):
        super(TinvilleDesignerCreationForm, self).__init__(*args, **kwargs)

        self.isDesigner = True

        self.fields['shop_name'].required = True

        self.helper.layout = Layout(
            Div(
                Field('first_name', placeholder="First name", css_class="col-xs-5 registerField"),
                Field('last_name', placeholder="Last name", css_class="col-xs-5 col-xs-offset-2 registerField"),
                Hidden('last_login', datetime.now()),
                Field('shop_name', placeholder="Shop name", css_class="col-xs-12 registerField"),
                Field('email', placeholder="Email", css_class="col-xs-12 registerField"),
                Field('password', placeholder="Password", css_class="col-xs-5 registerField"),
                Field('password2', placeholder="Confirm password", css_class="col-xs-5 col-xs-offset-2 registerField"),
                Submit('submit', 'Register', css_class='tinvilleButton registerField pull-right')
            )
        )





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
        self.helper.form_class = "loginForm"
        self.helper.layout = Layout(
            # Jon M TODO Consolidate messages into a common tag that can be loaded in
            Div(
                HTML("""{{ form.non_field_errors }}"""
                ),
            css_id="message_area", css_class='messageError'),
            Div(
                HTML("""<a id="loginFacebookButton" class="btn col-xs-10 col-xs-offset-1 btn-facebook">
                            <i class="icon-facebook"></i> | Sign in with Facebook
                        </a""")
            ),

            #HTML ("""<strong class="line-thru col-xs-10 col-xs-offset-1">or</strong>"""),
            HTML("""<img class="col-xs-10 col-xs-offset-1" src="{{ STATIC_URL }}img/or_login.gif" style=" margin-top: 5%; "/>"""),
            #HTML("""<div class="col-xs-1 formField"> or </div>"""),
            #HTML("""<div class="loginFormLine col-xs-3 col-xs-offset-1"></div>"""),

            Field('username', placeholder="Email", css_class='col-xs-10 col-xs-offset-1 formField'),
            Field('password', type='password', placeholder="Password", css_class='col-xs-10 col-xs-offset-1 formField'),

            HTML("""<div for="id_remember_me" id="rememberLoginLabel" class=" checkbox  col-xs-10 col-xs-offset-1">
                        <input checked="checked" class=" checkboxinput" id="id_remember_me" name="remember_me"
                         type="checkbox" value="true">
                        Remember Me </input>
                    </div>"""),
            Div(
                Submit('submit', 'Sign in', css_class='btn btn-primary col-xs-10 col-xs-offset-1 tinvilleButton')
            ),
            HTML("""<div class="formField col-xs-10 col-xs-offset-1 pull-left loginForgot">
                    <p>Forgot
                    <a href="#" id="loginForgotUsernameLink" class=" ">username</a>
                     or
                    <a href="#" id="loginForgotPasswordLink" class="">password?</a></p>
                    </div>"""),


            HTML("""<div class="formField col-xs-10 col-xs-offset-1 pull-left loginRegister">
                    <p>Don't have an Account?
                    <a href="#" id="loginRegisterLink" class=" ">Register</a></p>
                    </div>""")


        )
