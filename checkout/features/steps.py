# -*- coding: utf-8 -*-
from django.core.management import call_command
import lettuce.django
import math
import time
import os

from Tinville.settings.base import MEDIA_ROOT
from designer_shop.models import Shop
from user.models import TinvilleUser
from selenium.webdriver.support.ui import Select
from common.lettuce_utils import *

@before.each_scenario
def load_all_fixtures(scenario):
    call_command('loaddata', 'all.json')

@step(u'Given the demo shop$')
def given_the_demo_shop(step):
    world.browser.get(lettuce.django.get_server().url('/Demo'))

@step(u'(?:When|And) The user is signed in')
def and_the_user_is_signed_in(step):
    sign_in('demo@user.com', 'tinville')

@step(u'Given the shipping address page')
def given_the_shipping_address_page(step):
    assert_id_exists('shopEditor')

@step(u'And a global submit button')
def and_a_global_submit_button(step):
    assert world.browser.find_element_by_css_selector('button.tinvilleButton.pull-right')
