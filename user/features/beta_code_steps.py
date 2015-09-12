from common.lettuce_utils import *
import cssselect
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
from user.models import TinvilleUser
import lettuce.django
from selenium.common.exceptions import *


@step(u'Given the beta shop')
def given_the_beta_shop(step):
    world.browser.get(get_server().url('/BetaShop/'))
    wait_for_browser_to_have_url(get_server().url('/access_code?shop=BetaShop'))

@step(u'Given a subsequent visit to the beta shop')
def given_a_subsequent_visit_to_the_beta_shop(step):
    world.browser.get(get_server().url('/BetaShop/'))

@step(u'Then the access code page is displayed')
def then_the_access_code_page_is_displayed(step):
    assert_id_exists('betaform')

@step(u'And I enter the access code')
def and_i_enter_the_access_code(step):
    user = TinvilleUser.objects.get(email="joe@schmoe.com")
    form = fill_in_access_form(access_code=user.access_code)
    form.submit()


@step(u'Then I should be redirected to the beta shop')
def then_I_should_be_redirected_to_the_beta_shop(step):
    world.browser.get(get_server().url('/BetaShop/'))