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
    assert True