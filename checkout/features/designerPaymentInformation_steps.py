__author__ = 'mervetuccar'
from lettuce import *
from common.lettuce_utils import *

@step("a designer is logged in")
def designer_is_logged_in(step):
    world.browser.get(lettuce.django.get_server().url())
    sign_in('Demo@user.com', 'tinville')

@step("designer clicks on user icon")
def step_impl(step):
    assert_selector_does_exist('#clickedLogin-lg') #this verifies if the icon exists
    world.browser.find_element_by_css_selector('#clickedLogin-lg').click() #clicking on the icon

@step("drop down menu is displayed")
def drop_down_menu_displayed(step):
    wait_for_element_with_css_selector_to_be_displayed('#loginIcon-lg + .dropdown-menu')

@step("click on My Payment Info")
def click_on_my_payment_info(step):
    world.browser.find_element_by_partial_link_text('My Payment Info').click()

@step("payment info form is displayed")
def payment_info_form_displayed(step):
    assert_id_exists('payment-info-form')

@step("the payment info form")
def given_the_payment_info(step):
    step.given('a designer is logged in')
    step.when('designer clicks on user icon')
    step.then('drop down menu is displayed')
    step.then('click on My Payment Info')
    step.then('payment info form is displayed')

@step("the '(.*)' '(.*)' is displayed") #Payment Form Display, given the payment info form
def step_impl(step, name, fieldtype):
    field = world.browser.find_element_by_name(name)
    assert field.is_displayed()==True
    assert field.get_attribute('type')==fieldtype, "fieldtype should be " + fieldtype + " but is " + field.tag_name


@step("the payment info form")
def payment_info_form(step)





