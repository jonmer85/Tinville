# -*- coding: utf-8 -*-
from common.lettuce_utils import *
import cssselect
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
from user.models import TinvilleUser
import lettuce.django
from selenium.common.exceptions import *

@step(u'(?:Then|And) I can visit my shop at "([^"]*)"')
def then_i_can_visit_my_shop(step, url):
    absoluteUrl = get_server().url(url)
    world.browser.get(absoluteUrl)
    assert_page_exist(url)

@step(u'(?:Then|And) check if the new shop exist "([^"]*)"')
def check_if_new_shop_exist(step, id):
    assert_id_exists(id)