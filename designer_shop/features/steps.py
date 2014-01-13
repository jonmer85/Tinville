# -*- coding: utf-8 -*-
from designer_shop.models import Shop
from django.test.client import Client
from lettuce import *
from lettuce.django import django_url
from lxml import html
from nose.tools import assert_true, assert_equals, assert_regexp_matches
import re

@before.all
def set_browser():
    world.browser = Client()

@step(u'Given a designer shop')
def given_a_designer_shop(step):
    world.shop = Shop.objects.create(name='foo', banner='bar', logo='baz')

@step(u'When the shop is visited')
def when_the_shop_is_visited(step):
    response = world.browser.get(django_url(world.shop.get_absolute_url()))
    assert_equals(200, response.status_code)
    world.dom = html.fromstring(response.content)

@step(u'Then the banner for the shop is displayed')
def then_the_banner_for_the_shop_is_displayed(step):
    assert_selector_contains('img.shopBanner', 'src', 'bar')

@step(u'And the logo for the shop is displayed')
def then_the_logo_for_the_shop_is_displayed(step):
    assert_selector_contains('img.shopLogo', 'src', 'baz')

@step(u'And the items for the shop are displayed')
def and_the_items_for_the_shop_are_displayed(step):
    assert_equals('shopItems', world.dom.cssselect('.shopItems')[0].attrib['class'])

@step(u'And the Tinville header is displayed')
def and_the_tinville_header_is_displayed(step):
    assert_equals(1, len(world.dom.cssselect('.navbar')))

def assert_selector_contains(selector, attrib, string):
    assert_regexp_matches(
        world.dom.cssselect(selector)[0].attrib[attrib],
        re.compile(".*" + string + ".*"),
    )

@step(u'And (\d+) shop items')
def and_n_shop_items(step, n):
    for i in range(int(n)):
        world.shop.item_set.create(name='itemname', image='itemimage', price='3.42')

@step(u'Then there should be (\d+) items displayed')
def then_there_should_be_n_items_displayed(step, n):
    assert_equals(int(n), len(world.dom.cssselect('.shopItems .shopItem')))

@step(u'And every item should have a name')
def and_every_item_should_have_a_name(step):
    for item in world.dom.cssselect('.shopItems .shopItem .name'):
        assert_equals('itemname', item.text)

@step(u'And every item should have an image')
def and_every_item_should_have_an_image(step):
    selector_found = False
    for item in world.dom.cssselect('.shopItems .shopItem img'):
        assert_regexp_matches(item.attrib['src'], re.compile('.*itemimage.*'))
        selector_found = True
    assert_true(selector_found, 'No elements found')

@step(u'And every item should have a price')
def and_every_item_should_have_a_price(step):
    selector_found = False
    for item in world.dom.cssselect('.shopItems .shopItem .price'):
        assert_equals('$3.42', item.text)
        selector_found = True
    assert_true(selector_found, 'No elements found')
