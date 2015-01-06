# -*- coding: utf-8 -*-
from common.lettuce_utils import *
import cssselect
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
from user.models import TinvilleUser
import lettuce.django
from selenium.common.exceptions import *

@step(u'When I click the flatpage of "([^"]*)"')
def when_i_click_flatpages(step, url):
    absoluteUrl = lettuce.django.get_server().url(url)
    world.browser.get(absoluteUrl)
    assert_page_exist(url)

@step(u'(?:Then|And) I check if that page is active of id "([^"]*)"')
def check_if_id_is_active(step, id):
    assert_id_exists(id)
    assert_selector_contains('#About', 'class', 'active')