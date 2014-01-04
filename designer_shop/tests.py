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

class ViewTest(TestCase):
    def setUp(self):
        Shop.objects.create(name='foo', banner='bar', logo='baz').save
        self.content = html.fromstring(shopper(HttpRequest(), 'foo').content)

    def test_banner(self):
        self.assertSelectorContains('img.shopBanner', 'src', 'bar')

    def test_logo(self):
        self.assertSelectorContains('img.shopLogo', 'src', 'baz')

    def assertSelectorContains(self, selector, attrib, string):
        self.assertRegexpMatches(
            self.content.cssselect(selector)[0].attrib[attrib],
            re.compile(".*" + string + ".*"),
        )
