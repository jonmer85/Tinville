from common.lettuce_utils import *
from django.core.management import call_command
from selenium.webdriver.support.select import Select


@before.each_scenario
def load_all_fixtures(scenario):
    call_command('loaddata', 'countries_tinville.json')


@step(u'I access the addresses page as a new designer')
def i_access_the_addresses_page_as_a_new_designer(step):
    register_a_designer_account('joe@schmoe.com', 'test', 'ShmoeVille')
    sign_in('joe@schmoe.com', 'test')
    world.browser.get(lettuce.django.get_server().url('/accounts/addresses'))
    assert_selector_contains_text(".slidingContent2", "There are no addresses in your address book.")

@step(u'I access the addresses page as a new shopper')
def i_access_the_addresses_page_as_a_new_shopper(step):
    register_a_shopper_account('joe@schmoe.com', 'test')
    sign_in('joe@schmoe.com', 'test')
    world.browser.get(lettuce.django.get_server().url('/accounts/addresses'))
    assert_selector_contains_text(".slidingContent2", "There are no addresses in your address book.")

@step(u'I add a new address')
def i_add_a_new_address(step):
    wait_for_element_with_css_selector_to_be_clickable("a[href='/accounts/addresses/add/']").click()
    wait_for_element_with_name_to_be_displayed('first_name').send_keys('Joe')
    wait_for_element_with_name_to_be_displayed('last_name').send_keys('Schmoe')
    wait_for_element_with_name_to_be_displayed('line1').send_keys('143 Essex St')
    wait_for_element_with_name_to_be_displayed('line4').send_keys('Haverhill')
    wait_for_element_with_name_to_be_displayed('state').send_keys('MA')
    wait_for_element_with_name_to_be_displayed('postcode').send_keys('01832')
    wait_for_element_with_css_selector_to_be_clickable("button[type='submit']").click()
    wait_for_element_with_css_selector_to_be_clickable("#messagesModal .close").click()

@step(u'I should not see any default address types')
def i_should_not_see_any_default_address_types(step):
    assert_selector_does_not_exist('span.label')

@step(u'I should see all available designer address types as options to be added to the address')
def i_should_see_all_available_designer_address_types_as_options(step):
    assert_selector_does_exist(".dropdown-menu a[href$='default_for_shipping/']")
    assert_selector_does_exist(".dropdown-menu a[href$='default_for_shop/']")

@step(u'I should see all but shop shipping address available designer address types as options to be added to the address')
def i_should_see_all_available_designer_address_types_as_options(step):
    assert_selector_does_exist(".dropdown-menu a[href$='default_for_shipping/']")


@step(u'I should see all available shopper address types as options to be added to the address')
def i_should_see_all_available_designer_address_types_as_options(step):
    assert_selector_does_exist(".dropdown-menu a[href$='default_for_shipping/']")
    assert_selector_does_not_exist(".dropdown-menu a[href$='default_for_shop/']")


@step(u'I mark the address as the (.*) address')
def i_mark_the_address_as_a_type(step, type):
    wait_for_element_with_css_selector_to_be_clickable('button.dropdown-toggle').click()
    wait_for_element_with_css_selector_to_be_clickable(".dropdown-menu a[href$='default_for_{0}/']".format(type)).click()

@step(u'the shipping address badge is shown')
def the_shipping_address_badge_is_shown(step):
    wait_for_element_with_css_selector_to_be_displayed('.label-success')
    assert_selector_contains_text('.label-success', 'Default shipping address')

@step(u'the shop address badge is shown')
def the_shop_address_badge_is_shown(step):
    wait_for_element_with_css_selector_to_be_displayed('.label-primary')
    assert_selector_contains_text('.label-primary', 'Default shop shipping address')

