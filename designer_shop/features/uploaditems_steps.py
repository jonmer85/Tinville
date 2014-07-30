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

@step(u'When I click the delete button for the product')
def when_I_click_delete_button_product(step):
    world.browser.find_element_by_css_selector("#minMaxIcon").click()
    wait_for_element_with_link_text_to_be_displayed("Delete")
    world.browser.find_element_by_link_text("Delete").click()

@step(u'Then the product is removed')
def then_product_is_removed(step):
    try:
        world.browser.find_element_by_css_selector("a[href='/Demo/edit/delete_product/TestSizeSetItem']")
    except NoSuchElementException:
        return True
    return False

@step(u'And the shop editor refreshes in a minimized state')
def and_shopEditor_refreshes_minimized(step):
    assert world.browser.find_element_by_css_selector("#minMaxIcon.glyphicon-chevron-up").is_displayed() == True, "Because chevron should be facing up"
    assert len(world.browser.find_elements_by_css_selector("#editorPanels.collapse")) == 1, "Because the editor panel should be collapsed"