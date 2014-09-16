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


@step(u'Then I should see the following filters')
def then_i_should_see_the_following_filters(step):
    for filter in step.hashes:
        thefiltername = str(filter["FilterName"])
        thedefaultvalue = str(filter["DefaultValue"]).replace('"', '')
        theselector = world.browser.find_element_by_id(thefiltername)

        if theselector.tag_name == 'select':
            theselectedvalue = str(Select(theselector).first_selected_option.text)
        elif theselector.tag_name == "input":
            theselectedvalue = str(theselector.get_attribute('value'))
        assert theselectedvalue == thedefaultvalue,  theselectedvalue + " does not equal" + thedefaultvalue

@step(u'When I select the "(.*)" "(.*)"')
def when_i_select_a_option(step, filterId, selection):
    Select(world.browser.find_element_by_id(str(filterId))).select_by_value(selection)

@step(u'Then I should have "(\d+)" items in the demo shop')
def then_my_color_is(step, amount):
   # WebDriverWait(world.browser, 10).until(lambda s: s.find_elements_by_css_selector(".shopItem") == int(amount))
    hello = len(world.browser.find_elements_by_css_selector(".shopItem"))
    assert WebDriverWait(world.browser, 10).until(lambda s: len(s.find_elements_by_css_selector(".shopItem")) == int(amount)), "there are not " + amount + " items in the demo shop"

@step(u'Then I should not see coming soon message')
def then_no_coming_soon_message(step):
    assert_id_does_not_exist("emptyShopId")