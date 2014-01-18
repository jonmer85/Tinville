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

@step(u'I access the URL "(,*)"')
def access_url(step, url):
    response = world.browser.get(url)
    assert_equals(200, response.status_code)
    world.dom = html.fromstring(response.content)

@step(u'I see information to register as a designer')
def see_information_to_register_as_a_designer(step):
    designerInfo = world.dom.cssselect('#viewDesignerDetails')[0]
    assert designerInfo.text.length > 0



# @step(u'When the shop is visited')
# def when_the_shop_is_visited(step):
#     response = world.browser.get(django_url(world.shop.get_absolute_url()))
#     assert_equals(200, response.status_code)
#     world.dom = html.fromstring(response.content)
#
# @step(u'Then the banner for the shop is displayed')
# def then_the_banner_for_the_shop_is_displayed(step):
#     assert_selector_contains('img.shopBanner', 'src', 'bar')
#
# @step(u'And the items for the shop are displayed')
# def and_the_items_for_the_shop_are_displayed(step):
#     assert_selector_exists('.shopItems')
#
# @step(u'And the Tinville header is displayed')
# def and_the_tinville_header_is_displayed(step):
#     assert_selector_exists('.navbar')
#
# @step(u'Then there should be (\d+) items displayed')
# def then_there_should_be_n_items_displayed(step, n):
#     assert_number_of_selectors('.shopItems .shopItem', int(n))
#
# @step(u'And every item should have a name')
# def and_every_item_should_have_a_name(step):
#     assert_text_of_every_selector('.shopItems .shopItem .name', 'itemname')
#
# @step(u'And every item should have an image')
# def and_every_item_should_have_an_image(step):
#     assert_every_selector_contains('.shopItems .shopItem img', 'src', 'itemimage')
#
# @step(u'And every item should have a price')
# def and_every_item_should_have_a_price(step):
#     assert_text_of_every_selector('.shopItems .shopItem .price', '$3.42')


