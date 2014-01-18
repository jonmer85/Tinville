# -*- coding: utf-8 -*-
from common.lettuce_utils import *
from django.test.client import Client
from lettuce import *
from lettuce.django import django_url
from lxml import html
from nose.tools import *

@before.all
def set_browser():
    world.browser = Client()

@step(u'I access the registration page')
def access_url(step):
    response = world.browser.get('/register')
    assert_equals(200, response.status_code)
    world.dom = html.fromstring(response.content)

@step(u'I see information to register as a designer')
def see_information_to_register_as_a_designer(step):
    assert_text_exists_in_first_element('#viewDesignerDetails', 'Designer info not found')

@step(u'Or to register as a shopper')
def see_information_to_register_as_a_designer(step):
    assert_text_exists_in_first_element('#viewShopperDetails', 'Shopper info not found')

@step(u'all registration forms are initially collapsed')
def all_registration_forms_are_initially_collapsed(step):
    assert_selector_does_not_exist('.in')




# Helper methods
def assert_text_exists_in_first_element(selector, error_text):
    first_element = world.dom.cssselect(selector)[0]
    assert_true(len(html.tostring(first_element)) > 0, error_text)


