# -*- coding: utf-8 -*-
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
from selenium.webdriver.support.ui import Select
from common.lettuce_utils import *

@step(u'Given I have an item in the demo shop')
def given_I_have_an_item_in_the_shop(step):
    assert world.browser.find_elements_by_css_selector(".shopItem").count > 0

@step(u'When I click on the item')
def when_i_click_on_the_item(step):
    theitem = world.browser.find_element_by_css_selector(".shopItem")
    step.scenario.context['itemurl'] = theitem.find_element_by_css_selector("a").get_attribute("href")
    theitem.find_element_by_css_selector("a").click()

@step(u'Then the item detail page is displayed')
def then_the_item_detail_page_is_displayed(step):
    assert world.browser.current_url == step.scenario.context['itemurl'] + "/", world.browser.current_url + " does not equal " + step.scenario.context['itemurl']

@step(u'Given I am on an item detail page')
def given_i_am_on_an_item_detail_page(step):
    step.behave_as("Given the demo shop")
    step.behave_as("Given I have an item in the demo shop")
    step.behave_as("When I click on the item")
    step.behave_as("Then the item detail page is displayed")

@step(u'Then I can see the following elements')
def then_i_can_see_the_following_elements(step):
    for itemdetailclass in step.hashes:
        theitemclass = str(itemdetailclass["Class"])
        myelements = world.browser.find_elements_by_class_name(theitemclass)
        elementexists = False
        for element in myelements:
            if element.is_displayed() == True:
                elementexists = True
                break
        assert elementexists, theitemclass + " is not displayed"

@step(u'Then the default values for an item are as follows')
def then_the_default_values_for_an_item_are_as_follows(step):
    for itemdetailvalues in step.hashes:
        theitemclass = str(itemdetailvalues["Class"])
        thedefaultvalue = str(itemdetailvalues["DefaultValue"]).replace('"', '')
        theselector = world.browser.find_element_by_id(theitemclass)

        if theselector.tag_name == 'select':
            theselectedvalue = str(Select(theselector).first_selected_option.text)
        elif theselector.tag_name == "input":
            theselectedvalue = str(theselector.get_attribute('value'))
        assert theselectedvalue == thedefaultvalue,  theselectedvalue + " does not equal" + thedefaultvalue

