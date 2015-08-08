from common.lettuce_extensions import get_server
from lettuce import step
from django.core.management import call_command
import lettuce.django
import os
import time
import math

from Tinville.settings.base import MEDIA_ROOT
from designer_shop.models import Shop
from user.models import TinvilleUser
from selenium.webdriver.support.ui import Select
from common.lettuce_utils import *

@step(u'Given a desktop shopper')
def Given_desktop_shopper(step):
    world.browser.get(get_server().url())
    change_viewport_md()

@step(u'Given a mobile shopper')
def Given_mobile_shopper(step):
    world.browser.get(get_server().url())
    change_viewport_xs()

@step(u'When I click the Desktop Shopping cart button')
def When_Click_Desktop_Shopping_Cart_Button(step):
    wait_for_element_with_css_selector_to_exist("#shoppingcartBtn")
    wait_for_element_with_css_selector_to_be_clickable("#shoppingcartBtn #shoppingcart").click()

@step(u'When I click the Mobile Shopping cart button')
def When_Click_Mobile_Shopping_Cart_Button(step):
    world.browser.find_element_by_css_selector("#shoppingcartMobileBtn").click()

@step(u'Then the Shopping cart opens')
def Then_Shopping_Cart_Opens(step):
    assert_selector_does_exist('#shoppingcart.open')

@step(u'Then the Shopping cart closes')
def Then_Shopping_Cart_Closes(step):
    time.sleep(1)
    contains = "display: none;" in world.browser.find_element_by_css_selector('#shoppingcart').get_attribute("style")
    assert contains == True

@step(u'When I add an item to my cart')
def When_add_item_to_cart(step):
    world.browser.get(get_server().url("/Demo/TestSizeSetItem"))
    Select(world.browser.find_element_by_id("itemColorSelection")).select_by_value("Blue")
    Select(world.browser.find_element_by_id("itemSizeSelection")).select_by_value("SM")
    wait_for_element_with_css_selector_to_exist("#id_AddToCart")
    wait_for_element_with_css_selector_to_be_clickable("#id_AddToCart").click()

@step(u'Then the item is added to my cart')
def Then_item_added_to_cart(step):
    wait_for_element_with_css_selector_to_exist(".shoppingcartitem[id^=lineId]")
    assert_number_of_selectors(".shoppingcartitem[id^=lineId]", 1)

@step(u'And check the Added to bag button')
def And_check_added_to_bag(step):
    assert_selector_contains_text("#id_AddToCart","Added to bag")

@step(u'Then add another item is still in my cart')
def add_and_still_in_my_cart(step):
    world.browser.get(get_server().url("/Demo/TestSizeSetItem"))
    Select(world.browser.find_element_by_id("itemColorSelection")).select_by_value("Blue")
    Select(world.browser.find_element_by_id("itemSizeSelection")).select_by_value("XS")
    wait_for_element_with_css_selector_to_exist("#id_AddToCart")
    wait_for_element_with_css_selector_to_be_clickable("#id_AddToCart").click()
    wait_for_javascript_to_complete()
    wait_for_element_with_css_selector_to_exist(".shoppingcartitem[id^=lineId]")
    assert_number_of_selectors(".shoppingcartitem[id^=lineId]", 2)

@step(u'When I remove an item from my cart')
def When_remove_item_from_cart(step):
    wait_for_element_with_css_selector_to_be_clickable("a[id^=deleteBtnId_]").click()

@step(u'Then the item is removed from my cart')
def Then_item_removed_from_cart(step):
    assert_number_of_selectors(".shoppingcartitem[id^=lineId]", 0)

@step(u'When I click the Menu button')
def When_click_Menu_button(step):
    world.browser.find_element_by_id("mobileNavButton").click()

@step(u'When I log in or out')
def When_I_log_in(step):
    sign_in(email='foo@bar.com', password='foobar')

@step(u'Then all items are removed from my cart')
def Then_all_items_removed_from_cart(step):
    assert_number_of_selectors(".shoppingcartitem[id^=lineId]", 0)

@step(u'When I register for a shopper account')
def when_i_register_for_a_shopper_account(step):
    form = fill_in_user_form(email='foo@bar.com', password='foobar')
    submit_form_and_activate_user(form)

def fill_in_user_form(email, password):
    world.browser.get(get_server().url('/register'))
    world.user_info = {
        "email": email,
        "password": password,
    }
    form = world.browser.find_element_by_id("registrationForm")
    form.find_element_by_name("email").send_keys(email)
    form.find_element_by_name("password").send_keys(password)
    return form

def submit_form_and_activate_user(form, expectSuccess=True):
    form.submit()
    if(expectSuccess):
        wait_for_element_with_id_to_exist("messagesModal")
        assert_selector_contains_text("#messagesModal .alert-success", world.user_info['email'])
        wait_for_element_with_css_selector_to_be_clickable("#messagesModal .close").click()
        wait_for_element_with_id_to_not_be_displayed("messagesModal")
        user = TinvilleUser.objects.get(email=world.user_info['email'].lower())
        user.is_active = True
        user.save()

@step(u'(?:When|And) I sign in')
def and_i_sign_in(step):
    sign_in(email='foo@bar.com', password='foobar')
