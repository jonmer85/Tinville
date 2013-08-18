from datetime import datetime

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Hidden
from crispy_forms.bootstrap import InlineCheckboxes

from Tinville.Site.models import TinvilleUser

class TinvilleUserCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        isDesigner = kwargs.pop('designer', False)
        super(TinvilleUserCreationForm, self).__init__(*args, **kwargs)

        self.isDesigner = isDesigner

        if isDesigner:
            userStrings = {'lowerCaseUser': 'designer', 'upperCaseUser': 'Designer',
                           'fashionInterestHeading': 'Select the Fashion Styles You Are Selling'}

        else:
            userStrings = {'lowerCaseUser': 'shopper', 'upperCaseUser': 'Shopper',
                           'fashionInterestHeading': 'Select the Fashion Styles That Interest You'}


        self.helper = FormHelper()
        self.helper.layout = Layout(

            HTML(
                """
                <div class="row">
                    <div class="span15">
                        <div id="tinvilleLogoDiv"class="span2">
                            <img id="tinvilleLogo" src="{{ STATIC_URL }}img/tinville_register_logo.png">
                        </div>
                        <div id="registerUserWrapperDiv" class="span13">
                            <div id="registrationUserContainerDiv" class="registrationContent">
                                <div id="registerUserDiv" class="registrationInfoDiv">
                                    <div class="row">
                                        <div id="registerNewUserPane" class="span6 first registerUserPane">
                                            <h1 id="registerNewUserHeading" class="orangeHeading">Register New %(upperCaseUser)s</h1>
                                            <p><img id="registerNewUserIcon" src="{{ STATIC_URL }}img/%(lowerCaseUser)s_big_logo.png"></p>
                                        </div>
                                        <div id= "registerUserFormDiv" class="span6 registerUserPane">
                            """ % userStrings
            ),
            Div(
                Div(Field('first_name'), css_class="span3"),
                Div(Field('last_name'), css_class="span3"),
                Hidden('last_login', datetime.now()),
                css_class="row"
            ),
            Div(
                Div(Field('shop_name', css_class="input-block-level"), css_class="span6"),
                css_class="row"
            ),
            Div(
                Div(Field('email', css_class="input-block-level"), css_class="span6"),
                css_class="row"
            ),
            Div(
                Div(Field('password'), css_class="span3"),
                Div(Field('password2'), css_class="span3"),
                css_class="row"
            ),
            HTML(
                """
                         </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            <div class="row">
                <div class="span15">
                    <div id="designerInfoAndFashionTypesContainerDiv" class="registrationContent cn">
                        <div id="designerInfoAndFashionTypesDiv" class="registrationInfoDiv inner">
                            <div class= "span7 first designerInfoDiv">
                                <hi class="orangeHeading">%(upperCaseUser)s Info:</hi>
                                <div class="designerInfoSection">
                                    <img class="infoLeft" src="{{ STATIC_URL }}img/question.png">
                                    <p class="designerInfo">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed iaculis quis risus congue hendrerit. Suspendisse venenatis sed lacus vel semper.
                                       Phasellus tristique lectus a eros interdum tempus. Cras vestibulum tellus eu risus iaculis euismod. Nunc sed nibh ac massa suscipit ultrices.
                                       Suspendisse sed gravida risus. Sed a nibh at orci rutrum lobortis in euismod ipsum. Duis consequat euismod dignissim. Proin sed lacus lectus.
                                    </p>
                                </div>
                                <div class="designerInfoSection">
                                    <img class="infoRight" src="{{ STATIC_URL }}img/question.png">
                                    <p class="designerInfo">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed iaculis quis risus congue hendrerit. Suspendisse venenatis sed lacus vel semper.
                                       Phasellus tristique lectus a eros interdum tempus. Cras vestibulum tellus eu risus iaculis euismod. Nunc sed nibh ac massa suscipit ultrices.
                                       Suspendisse sed gravida risus. Sed a nibh at orci rutrum lobortis in euismod ipsum. Duis consequat euismod dignissim. Proin sed lacus lectus.
                                    </p>
                                </div>
                                <div class="designerInfoSection">
                                    <img class="infoLeft" src="{{ STATIC_URL }}img/question.png">
                                    <p class="designerInfo">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed iaculis quis risus congue hendrerit. Suspendisse venenatis sed lacus vel semper.
                                       Phasellus tristique lectus a eros interdum tempus. Cras vestibulum tellus eu risus iaculis euismod. Nunc sed nibh ac massa suscipit ultrices.
                                       Suspendisse sed gravida risus. Sed a nibh at orci rutrum lobortis in euismod ipsum. Duis consequat euismod dignissim. Proin sed lacus lectus.
                                    </p>
                                </div>
                            </div>
                            <div class="span6">
                                <h1 id="fashionStylesHeading" class="orangeHeading">%(fashionInterestHeading)s</h1>
                                <div id="div_id_styles" class="control-group span6">
                                    <label class="checkbox span1"><input type="checkbox" name="styles" id="id_styles_1" value="1">Retro/Mod</label>
                                    <label class="checkbox span1"><input type="checkbox" name="styles" id="id_styles_2" value="2">Vintage</label>
                                    <label class="checkbox span1"><input type="checkbox" name="styles" id="id_styles_3" value="3">Formal</label>
                                    <label class="checkbox span1 clear"><input type="checkbox" name="styles" id="id_styles_4" value="4">Casual</label>
                                    <label class="checkbox span1"><input type="checkbox" name="styles" id="id_styles_5" value="5">Trendy</label>
                                    <label class="checkbox span1"><input type="checkbox" name="styles" id="id_styles_6" value="6">Industrial</label>
                                    <label class="checkbox span1 clear"><input type="checkbox" name="styles" id="id_styles_7" value="7">Boho</label>
                                    <label class="checkbox span1"><input type="checkbox" name="styles" id="id_styles_8" value="8">Punk</label>
                                    <label class="checkbox span1"><input type="checkbox" name="styles" id="id_styles_9" value="9">Lolita</label>
                                    <label class="checkbox span1 clear"><input type="checkbox" name="styles" id="id_styles_10" value="10">Steampunk</label>
                                    <label class="checkbox span1"><input type="checkbox" name="styles" id="id_styles_11" value="11">Eco</label>
                                    <label class="checkbox span1"><input type="checkbox" name="styles" id="id_styles_12" value="12">Accessories</label>
                                </div>
                                """ % userStrings
            ),
            Submit('submit', 'Register', css_class='registerButton'),
            HTML(
                """
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                """
            )
        )


    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    isDesigner = False
    userStrings = {}

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
        user.is_seller = True
        if commit:
            user.save()
        return user



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


