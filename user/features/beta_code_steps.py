from common.lettuce_utils import *
import cssselect
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
from user.models import TinvilleUser
import lettuce.django
from selenium.common.exceptions import *


@step(u'Given the beta shop')
def given_the_beta_shop(step):
    world.browser.get(lettuce.django.get_server().url('/access_code?shop=BetaShop'))

@step(u'Then the access code page is displayed')
def then_the_access_code_page_is_displayed(step):
    assert_id_exists('betaform')

@step(u'And I enter the access code')
def and_i_enter_the_access_code(step):
    # user = TinvilleUser.objects.get(name = 'joe@schmoe.com')
    user = TinvilleUser.objects.get(email="joe@schmoe.com")
    form = fill_in_access_form(access_code=user.access_code)
    form.submit()

def fill_in_access_form(access_code):
    world.user_info = {
        "access_code": access_code
    }
    form = world.browser.find_element_by_id("betaform")
    form.find_element_by_name("access_code").send_keys(access_code)
    return form

@step(u'Then I should be redirected to the beta shop')
def then_I_should_be_redirected_to_the_beta_shop(step):
    world.browser.get(lettuce.django.get_server().url('/BetaShop'))