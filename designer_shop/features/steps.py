# -*- coding: utf-8 -*-
from designer_shop.models import Shop
from django.test.client import Client
from lettuce import *
from lettuce.django import django_url
from lxml import html
from nose.tools import assert_equals

@before.all
def set_browser():
    world.browser = Client()

@step(u'Given a designer shop')
def given_a_designer_shop(step):
    world.shop = Shop.objects.create(
        name='foo',
        banner='foo',
    )

@step(u'When the shop is visited')
def when_the_shop_is_visited(step):
    response = world.browser.get(django_url(world.shop.get_absolute_url()))
    assert_equals(200, response.status_code)
    world.dom = html.fromstring(response.content)

@step(u'Then the banner for the shop is displayed')
def then_the_banner_for_the_shop_is_displayed(step):
    banner = world.dom.cssselect('img.banner')
