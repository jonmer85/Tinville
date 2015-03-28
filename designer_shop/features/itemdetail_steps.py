# -*- coding: utf-8 -*-
from autoslug.utils import slugify
from lettuce import *
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

@step(u'I have at least (\d+) items in the demo shop')
def given_I_have_at_least_some_items_in_the_shop(step, amount):
    assert len(world.browser.find_elements_by_css_selector(".shopItem")) >= int(amount), "there are not at least " + amount + " items in the shop!"

@step(u'I click on the "(.*)" item')
def when_i_click_on_the_item(step, itemname):
    theitem = world.browser.find_element_by_css_selector("a[href='/demo/" + slugify(itemname) +"']")
    step.scenario.context['itemurl'] = theitem.get_attribute("href")
    theitem.click()

@step(u'the item detail page is displayed')
def then_the_item_detail_page_is_displayed(step):
    assert world.browser.current_url == step.scenario.context['itemurl'] + "/", world.browser.current_url + " does not equal " + step.scenario.context['itemurl']

@step('I am on an item detail page')
def given_i_am_on_an_item_detail_page(step):
    step.behave_as("Given the demo shop")
    step.behave_as("Given I have an item in the demo shop")
    step.behave_as("When I click on the {0} item".format('"TestSizeSetItem"'))
    step.behave_as("Then the item detail page is displayed")

@step(u'I can see the following elements')
def then_i_can_see_the_following_elements(step):
    for itemdetailclass in step.hashes:
        theitemclass = str(itemdetailclass["Class"])
        try:
            wait_for_element_with_css_selector_to_exist("." + theitemclass)
            # Jon M TODO: Put back when this is more stable with Selenium and FIrefox driver :(
            # myelements = wait_for_element_with_css_selector_to_be_displayed("." + theitemclass)
        except:
            assert False, theitemclass + " is not displayed"

@step(u'the default values for an item are as follows')
def then_the_default_values_for_an_item_are_as_follows(step):
    # wait_for_ajax_to_complete()
    for itemdetailvalues in step.hashes:
        theitem = str(itemdetailvalues["ID"])
        thedefaultvalue = str(itemdetailvalues["DefaultValue"]).replace('"', '')
        theselector = wait_for_element_with_id_to_be_clickable(theitem)

        if theselector.tag_name == 'select':
            theselectedvalue = str(Select(theselector).first_selected_option.text)
        elif theselector.tag_name == "input":
            theselectedvalue = str(theselector.get_attribute('value'))
        assert theselectedvalue == thedefaultvalue,  theselectedvalue + " does not equal" + thedefaultvalue

@step(u'I select the color (.*)')
def when_i_select_a_color(step, color):
    time.sleep(1)
    Select(world.browser.find_element_by_id("itemColorSelection")).select_by_value(str(color))

@step(u'my color is (.*)')
def then_my_color_is(step, color):
   theselectedvalue = str(Select(world.browser.find_element_by_id("itemColorSelection")).first_selected_option.text)
   assert theselectedvalue == str(color), theselectedvalue + " does not equal " + str(color)

@step(u'I try to select a size there are no options')
def when_i_try_select_a_size_before_selecting_color(step):
    amountofoptions = len(Select(world.browser.find_element_by_id("itemSizeSelection")).all_selected_options)
    assert amountofoptions == 1, "there should only be one option in the select (Choose a size), but there is " + str(amountofoptions)

@step(u'I select the size (.*)')
def when_I_select_a_size(step, size):
    Select(world.browser.find_element_by_id("itemSizeSelection")).select_by_value(str(size))

@step(u'my size is (.*)')
def then_my_size_is(step, size):
   theselectedvalue = str(Select(world.browser.find_element_by_id("itemSizeSelection")).first_selected_option.text)
   assert theselectedvalue == str(size), theselectedvalue + " does not equal " + str(size)

@step(u'I select a quantity of (.*)')
def when_I_select_a_size(step, quantity):
    world.browser.find_element_by_id("buyQuantity").clear()
    world.browser.find_element_by_id("buyQuantity").send_keys(str(quantity))

@step(u'my quantity is (.*)')
def then_my_size_is(step, quantity):
   theselectedvalue = str(world.browser.find_element_by_id("buyQuantity").get_attribute("value"))
   assert theselectedvalue == str(quantity), theselectedvalue + " does not equal " + str(quantity)

@step(u'my stock quantity is (.*)')
def then_my_stock_quantity_is(step, quantity):
    theselectedvalue = str(world.browser.find_element_by_class_name("itemStockQuantity").text)
    assert theselectedvalue == str(quantity) + " remaining", theselectedvalue + " does not equal " + str(quantity) + " remaining"
