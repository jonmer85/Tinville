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
    world.browser.get(lettuce.django.get_server().url())
    change_viewport_md()

@step(u'Given a mobile shopper')
def Given_mobile_shopper(step):
    world.browser.get(lettuce.django.get_server().url())
    change_viewport_xs()

@step(u'When I click the Desktop Shopping cart button')
def When_Click_Desktop_Shopping_Cart_Button(step):
    world.browser.find_element_by_css_selector("#shoppingcartBtn").click()

@step(u'When I click the Mobile Shopping cart button')
def When_Click_Mobile_Shopping_Cart_Button(step):
    world.browser.find_element_by_css_selector("#shoppingcartMobileBtn").click()

@step(u'Then the Shopping cart opens')
def Then_Shopping_Cart_Opens(step):
    contains = "display: block;" in world.browser.find_element_by_css_selector('#shoppingcart').get_attribute("style")
    assert contains == True

@step(u'Then the Shopping cart closes')
def Then_Shopping_Cart_Closes(step):
    time.sleep(1)
    contains = "display: none;" in world.browser.find_element_by_css_selector('#shoppingcart').get_attribute("style")
    assert contains == True

@step(u'When I add an item to my cart')
def When_add_item_to_cart(step):
    world.browser.get(lettuce.django.get_server().url("/Demo/TestSizeSetItem"))
    Select(world.browser.find_element_by_id("itemColorSelection")).select_by_value("Blue")
    Select(world.browser.find_element_by_id("itemSizeSelection")).select_by_value("SM")
    wait_for_element_with_css_selector_to_be_clickable("#id_AddToCart").click()

@step(u'Then the item is added to my cart')
def Then_item_added_to_cart(step):
    assert_id_exists("-1")

@step(u'When I remove an item from my cart')
def When_remove_item_from_cart(step):
    world.browser.find_element_by_id("deleteBtnId_-1").click()

@step(u'Then the item is removed from my cart')
def Then_item_removed_from_cart(step):
    assert_id_does_not_exist("-1")

@step(u'When I click the Menu button')
def When_click_Menu_button(step):
    world.browser.find_element_by_id("mobileNavButton").click()

@step(u'When I log in')
def When_I_log_in(step):
    sign_in('foo@user.com','password')

@step(u'Then the item is added to my backend')
def Then_item_added_to_backend(step):
    assert_id_exists("1")

@step(u'When I log out')
def When_I_log_out(step):
    sign_in('foo@user.com','password')

@step(u'Then all items are removed from my cart')
def Then_all_items_removed_from_cart(step):
    assert_id_does_not_exist("1")
