from common.lettuce_utils import *
from lettuce import step


@step(u'Given the BetaShop$')
def given_the_betashop(step):
    world.browser.get(lettuce.django.get_server().url('/BetaShop'))

@step(u'Then the access code page is displayed')
def then_the_access_code_page_is_displayed(step):
    world.browser.get(lettuce.django.get_server().url('/BetaShop'))
    assert_id_exists('betaform')

@step(u'And I enter the access code')
def and_I_enter_the_access_code(access_code):
    form = fill_in_access_form(access_code=access_code)
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