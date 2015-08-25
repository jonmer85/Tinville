from common.lettuce_utils import *
import cssselect
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
from user.models import TinvilleUser
import lettuce.django
from selenium.common.exceptions import *
from common.lettuce_utils import *
from selenium.webdriver.support.ui import Select

# @step(u'Given the shop page')
# def Given_the_shop_page(step):
#     world.browser.get(lettuce.django.get_server().url('/shop'))
#
# @step('When I select a filter')
# def When_i_select_a_filter(step):
#     world.browser.find_element_by_css_selector('#filterGender').click()
#     world.browser.find_element_by_css_selector('.')
#     world.browser.find_element_by_css_selector('#filterType').click()
#     world.browser.find_element_by_css_selector('#filterSort').click()