from designer_shop.models import Shop
from user.models import TinvilleUser
from designer_shop.views import *
from django.http import HttpRequest
from django.test import TestCase
from lxml import html
import re

class ModelTest(TestCase):
    def setUp(self):
        self.user = TinvilleUser.objects.create(email="foo@bar.com")
        self.shop = Shop.objects.create(user=self.user, name='foo bar')

    def test_get_absolute_url(self):
        self.assertEqual('/foo-bar/', self.shop.get_absolute_url())

    def test_shop_items(self):
        self.shop.item_set.create(name='foo', image='bar', price='2.34')
        self.assertEqual(1, self.shop.item_set.count())

    def test_slug(self):
        self.assertEqual(self.shop.slug, 'foo-bar')



class ViewTest(TestCase):
    def setUp(self):
        self.user = TinvilleUser.objects.create(email="foo@bar.com")
        self.shop = Shop.objects.create(user=self.user, name='foo', banner='bar', logo='baz')
        self.shop.item_set.create(name='foo', image='image_bar', price='1.23')
        self.httprequest = HttpRequest()
        self.httprequest.user = self.user
        self.content = html.fromstring(shopper(self.httprequest, 'foo').content)

    def test_banner(self):
        self.assertFirstSelectorContains('img.shopBanner', 'src', 'bar')

    def test_navbar(self):
        self.assertSelectorExists('.navbar')

    def test_items(self):
        self.assertSelectorExists('.shopItems')

    def test_item_name(self):
        self.assertFirstSelectorTextEquals(
            '.shopItems .shopItem .name',
            self.shop.item_set.all()[0].name,
        )

    def test_item_image(self):
        self.assertFirstSelectorContains('.shopItems .shopItem img', 'src', 'image_bar')

    def test_item_price(self):
        self.assertFirstSelectorTextEquals('.shopItems .shopItem .price', '$1.23')

    def test_slug_lookup(self):
        self.shop.name = 'foo bar'
        self.shop.save()
        shopper(self.httprequest, 'foo-bar')


    def assertSelectorExists(self, selector):
        self.assertGreater(len(self.content.cssselect(selector)), 0)

    def assertFirstSelectorTextEquals(self, selector, text):
        self.assertEqual(self.content.cssselect(selector)[0].text, text)

    def assertFirstSelectorContains(self, selector, attrib, string):
        self.assertRegexpMatches(
            self.content.cssselect(selector)[0].attrib[attrib],
            re.compile(".*" + string + ".*"),
        )
