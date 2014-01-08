from designer_shop.models import Shop
from designer_shop.views import *
from django.http import HttpRequest
from django.test import TestCase
from lxml import html
import re

class ModelTest(TestCase):
    def test_get_absolute_url(self):
        self.assertEqual('/foo/', Shop.objects.create(name='foo').get_absolute_url())
        self.assertEqual('/foo_bar/', Shop.objects.create(name='foo bar').get_absolute_url())

    def test_shop_items(self):
        shop = Shop.objects.create(name='foo')
        shop.item_set.create(name='foo', image='bar')
        self.assertEqual(1, shop.item_set.count())

class ViewTest(TestCase):
    def setUp(self):
        self.shop = Shop.objects.create(name='foo', banner='bar', logo='baz')
        self.shop.item_set.create(name='foo')
        self.content = html.fromstring(shopper(HttpRequest(), 'foo').content)

    def test_banner(self):
        self.assertSelectorContains('img.shopBanner', 'src', 'bar')

    def test_logo(self):
        self.assertSelectorContains('img.shopLogo', 'src', 'baz')

    def test_items(self):
        self.assertEquals('shopItems', self.content.cssselect('.shopItems')[0].attrib['class'])

    def test_item_name(self):
        self.assertEquals(
            self.content.cssselect('.shopItems .shopItem .name')[0].text,
            self.shop.item_set.all()[0].name,
        )

    def test_item_image(self):
        self.assertEqual(len(self.content.cssselect('.shopItems .shopItem img')), 1)

    def assertSelectorContains(self, selector, attrib, string):
        self.assertRegexpMatches(
            self.content.cssselect(selector)[0].attrib[attrib],
            re.compile(".*" + string + ".*"),
        )
