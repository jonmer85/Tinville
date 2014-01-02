# -*- coding: utf-8 -*-
from lettuce import *
from django.test.client import Client
from designer_shop.models import Shop

@before.all
def set_browser():
    world.browser = Client()

@step(u'Given a designer shop')
def given_a_designer_shop(step):
    Shop.objects.create()

@step(u'When the shop is visited')
def when_the_shop_is_visited(step):
    assert False, 'This step must be implemented'

@step(u'Then the banner for the shop is displayed')
def then_the_banner_for_the_shop_is_displayed(step):
    assert False, 'This step must be implemented'
