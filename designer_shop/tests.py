from designer_shop.models import Shop
from designer_shop.views import *
from django.test import TestCase
from lxml import html

class ModelTest(TestCase):
    def test_get_absolute_url(self):
        self.assertEqual('/foo/', Shop.objects.create(name='foo').get_absolute_url())
        self.assertEqual('/foo_bar/', Shop.objects.create(name='foo bar').get_absolute_url())

class ViewTest(TestCase):
    def test_shopper(self):
        Shop.objects.create(name='foo', banner="foo").save
        assert html.fromstring(self.client.get('/foo/').content).cssselect('img.shopBanner')[0].attrib['src']
