from designer_shop.models import Shop
from user.models import TinvilleUser
from designer_shop.views import *
from django.http import HttpRequest
from django.test import TestCase
from lxml import html
import json
import re

class ModelTest(TestCase):
    def setUp(self):
        self.user = TinvilleUser.objects.create(email="foo@bar.com")
        self.shop = Shop.objects.create(user=self.user, name='foo bar')

    def test_get_absolute_url(self):
        self.assertEqual('/foo-bar/', self.shop.get_absolute_url())

    #deprecated
    '''
    def test_shop_items(self):
        self.shop.item_set.create(name='foo', image='bar', price='2.34')
        self.assertEqual(1, self.shop.item_set.count())
    '''

    def test_slug(self):
        self.assertEqual(self.shop.slug, 'foo-bar')



class ViewTest(TestCase):
    def setUp(self):
        self.user = TinvilleUser.objects.create(email="foo@bar.com")
        self.shop = Shop.objects.create(user=self.user, name='foo', banner='bar', logo='baz')
        # Create a single product via ProductCreationForm
       # self.product = Product.objects.create(name='foo', image='image_bar', price='1.23')
       # self.shop.item_set.create(name='foo', image='image_bar', price='1.23')
        self.httprequest = HttpRequest()
        self.httprequest.user = self.user
        self.content = html.fromstring(shopper(self.httprequest, 'foo').content)

    def test_banner(self):
        self.assertFirstSelectorContains('img.shopBanner', 'src', 'bar')

    def test_navbar(self):
        self.assertSelectorExists('.navbar')

    def test_items(self):
        self.assertSelectorExists('.shopItems')

    '''
    def test_item_name(self):
        self.assertFirstSelectorTextEquals(
            '.shopItems .shopItem .name',
            self.product.all()[0].name,
        )
    '''
    '''
    def test_item_image(self):
        self.assertFirstSelectorContains('.shopItems .shopItem img', 'src', 'image_bar')

    def test_item_price(self):
        self.assertFirstSelectorTextEquals('.shopItems .shopItem .price', '$1.23')
    '''
    def test_slug_lookup(self):
        self.shop.name = 'foo bar'
        self.shop.save()
        shopper(self.httprequest, 'foo-bar')

    '''
    def assertSelectorExists(self, selector):
        self.assertGreater(len(self.content.cssselect(selector)), 0)

    def assertFirstSelectorTextEquals(self, selector, text):
        self.assertEqual(self.content.cssselect(selector)[0].text, text)

    def assertFirstSelectorContains(self, selector, attrib, string):
        self.assertRegexpMatches(
            self.content.cssselect(selector)[0].attrib[attrib],
            re.compile(".*" + string + ".*"),
        )
    '''

class ItemVarientService(TestCase):
    fixtures = ['all.json',]

    def test_nofiltersizeset(self):
        thecorrectresponse =json.loads('''{"variants": [{"color": "Red", "currency": "$", "price": "12.99", "quantity": 10, "size": "Xxs"},
                                        {"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10, "size": "Xxs"},
                                        {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10, "size": "Xs"},
                                        {"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10, "size": "Xs"},
                                        {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10, "size": "Sm"},
                                        {"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10, "size": "Sm"}],
                                        "sizetype": "1", "minprice": "12.99"}''')
        self.checkfilter("TestSizeSetItem", None, thecorrectresponse)

    def test_pricefiltersizeset(self):
        thecorrectresponse = json.loads('''{"variants": {"12.99": [{"color": "Red", "currency": "$", "quantity": 10, "size": "Xxs"},
                                           {"color": "Blue", "currency": "$", "quantity": 10, "size": "Xxs"},
                                           {"color": "Red", "currency": "$", "quantity": 10, "size": "Xs"},
                                           {"color": "Blue", "currency": "$", "quantity": 10, "size": "Xs"},
                                           {"color": "Red", "currency": "$", "quantity": 10, "size": "Sm"},
                                           {"color": "Blue", "currency": "$", "quantity": 10, "size": "Sm"}]},
                                           "sizetype": "1", "minprice": "12.99"}''')
        self.checkfilter("TestSizeSetItem", "price", thecorrectresponse)

    def test_colorfiltersizeset(self):
        thecorrectresponse = json.loads('''{"variants": {"Blue": [{"currency": "$", "price": "12.99", "quantity": 10, "size": "Sm"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "Xs"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "Xxs"}],
                                           "Red": [{"currency": "$", "price": "12.99", "quantity": 10, "size": "Sm"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "Xs"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "Xxs"}]},
                                           "sizetype": "1", "minprice": "12.99"}''')
        self.checkfilter("TestSizeSetItem", "color", thecorrectresponse)

    def test_sizefiltersizeset(self):
        thecorrectresponse = json.loads('''{"variants": {"Xxs": [{"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10},
                                           {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10}],
                                           "Xs": [{"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10},
                                           {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10}],
                                           "Sm": [{"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10},
                                           {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10}]},
                                           "sizetype": "1", "minprice": "12.99"}''')
        self.checkfilter("TestSizeSetItem", "size", thecorrectresponse)

    def test_quantityfiltersizeset(self):
        thecorrectresponse = json.loads('''{"variants": {"10": [{"color": "Red", "currency": "$", "price": "12.99", "size": "Xxs"},
                                           {"color": "Blue", "currency": "$", "price": "12.99", "size": "Xxs"},
                                           {"color": "Red", "currency": "$", "price": "12.99", "size": "Xs"},
                                           {"color": "Blue", "currency": "$", "price": "12.99", "size": "Xs"},
                                           {"color": "Red", "currency": "$", "price": "12.99", "size": "Sm"},
                                           {"color": "Blue", "currency": "$", "price": "12.99", "size": "Sm"}]},
                                           "sizetype": "1", "minprice": "12.99"}''')
        self.checkfilter("TestSizeSetItem", "quantity", thecorrectresponse)

    def test_currencyfiltersizeset(self):
        thecorrectresponse = json.loads('''{"variants": {"$": [{"color": "Red", "price": "12.99", "quantity": 10, "size": "Xxs"},
                                           {"color": "Blue", "price": "12.99", "quantity": 10, "size": "Xxs"},
                                           {"color": "Red", "price": "12.99", "quantity": 10, "size": "Xs"},
                                           {"color": "Blue", "price": "12.99", "quantity": 10, "size": "Xs"},
                                           {"color": "Red", "price": "12.99", "quantity": 10, "size": "Sm"},
                                           {"color": "Blue", "price": "12.99", "quantity": 10, "size": "Sm"}]},
                                           "sizetype": "1", "minprice": "12.99"}''')
        self.checkfilter("TestSizeSetItem", "currency", thecorrectresponse)

    def test_nofiltersizenum(self):
        thecorrectresponse =json.loads('''{"variants": [{"color": "Red", "currency": "$", "price": "12.99", "quantity": 10, "size": "1.0"},
                                          {"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10, "size": "1.0"},
                                          {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10, "size": "2.0"},
                                          {"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10, "size": "2.0"},
                                          {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10, "size": "3.0"},
                                          {"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10, "size": "3.0"}],
                                          "sizetype": "3", "minprice": "12.99"}''')
        self.checkfilter("TestSizeNumberItem", None, thecorrectresponse)

    def test_pricefiltersizenum(self):
        thecorrectresponse = json.loads('''{"variants": {"12.99": [{"color": "Red", "currency": "$", "quantity": 10, "size": "1.0"},
                                           {"color": "Blue", "currency": "$", "quantity": 10, "size": "1.0"},
                                           {"color": "Red", "currency": "$", "quantity": 10, "size": "2.0"},
                                           {"color": "Blue", "currency": "$", "quantity": 10, "size": "2.0"},
                                           {"color": "Red", "currency": "$", "quantity": 10, "size": "3.0"},
                                           {"color": "Blue", "currency": "$", "quantity": 10, "size": "3.0"}]},
                                           "sizetype": "3", "minprice": "12.99"}''')
        self.checkfilter("TestSizeNumberItem", "price", thecorrectresponse)

    def test_colorfiltersizenum(self):
        thecorrectresponse = json.loads('''{"variants": {"Blue": [{"currency": "$", "price": "12.99", "quantity": 10, "size": "1.0"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "2.0"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "3.0"}],
                                           "Red": [{"currency": "$", "price": "12.99", "quantity": 10, "size": "1.0"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "2.0"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "3.0"}]},
                                           "sizetype": "3", "minprice": "12.99"}''')
        self.checkfilter("TestSizeNumberItem", "color", thecorrectresponse)

    def test_sizefiltersizenum(self):
        thecorrectresponse = json.loads('''{"variants": {"2.0": [{"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10},
                                           {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10}],
                                           "1.0": [{"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10},
                                           {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10}],
                                           "3.0": [{"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10},
                                           {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10}]},
                                           "sizetype": "3", "minprice": "12.99"}''')
        self.checkfilter("TestSizeNumberItem", "size", thecorrectresponse)

    def test_quantityfiltersizenum(self):
        thecorrectresponse = json.loads('''{"variants": {"10": [{"color": "Red", "currency": "$", "price": "12.99", "size": "1.0"},
                                           {"color": "Blue", "currency": "$", "price": "12.99", "size": "1.0"},
                                           {"color": "Red", "currency": "$", "price": "12.99", "size": "2.0"},
                                           {"color": "Blue", "currency": "$", "price": "12.99", "size": "2.0"},
                                           {"color": "Red", "currency": "$", "price": "12.99", "size": "3.0"},
                                           {"color": "Blue", "currency": "$", "price": "12.99", "size": "3.0"}]},
                                           "sizetype": "3", "minprice": "12.99"}''')
        self.checkfilter("TestSizeNumberItem", "quantity", thecorrectresponse)

    def test_currencyfiltersizenum(self):
        thecorrectresponse = json.loads('''{"variants": {"$": [{"color": "Red", "price": "12.99", "quantity": 10, "size": "1.0"},
                                           {"color": "Blue", "price": "12.99", "quantity": 10, "size": "1.0"},
                                           {"color": "Red", "price": "12.99", "quantity": 10, "size": "2.0"},
                                           {"color": "Blue", "price": "12.99", "quantity": 10, "size": "2.0"},
                                           {"color": "Red", "price": "12.99", "quantity": 10, "size": "3.0"},
                                           {"color": "Blue", "price": "12.99", "quantity": 10, "size": "3.0"}]},
                                           "sizetype": "3", "minprice": "12.99"}''')
        self.checkfilter("TestSizeNumberItem", "currency", thecorrectresponse)

    def test_nofiltersizedim(self):
        thecorrectresponse =json.loads('''{"variants": [{"color": "Red", "currency": "$", "price": "12.99", "quantity": 10, "size": "30.0 x 30.0"},
                                          {"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10, "size": "31.0 x 31.0"},
                                          {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10, "size": "32.0 x 32.0"},
                                          {"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10, "size": "30.0 x 30.0"},
                                          {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10, "size": "31.0 x 31.0"},
                                          {"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10, "size": "32.0 x 32.0"}],
                                          "sizetype": "2", "minprice": "12.99"}''')
        self.checkfilter("TestSizeDimensionItem", None, thecorrectresponse)

    def test_pricefiltersizedim(self):
        thecorrectresponse = json.loads('''{"variants": {"12.99": [{"color": "Red", "currency": "$", "quantity": 10, "size": "30.0 x 30.0"},
                                           {"color": "Blue", "currency": "$", "quantity": 10, "size": "31.0 x 31.0"},
                                           {"color": "Red", "currency": "$", "quantity": 10, "size": "32.0 x 32.0"},
                                           {"color": "Blue", "currency": "$", "quantity": 10, "size": "30.0 x 30.0"},
                                           {"color": "Red", "currency": "$", "quantity": 10, "size": "31.0 x 31.0"},
                                           {"color": "Blue", "currency": "$", "quantity": 10, "size": "32.0 x 32.0"}]},
                                           "sizetype": "2", "minprice": "12.99"}''')
        self.checkfilter("TestSizeDimensionItem", "price", thecorrectresponse)

    def test_colorfiltersizedim(self):
        thecorrectresponse = json.loads('''{"variants": {"Blue": [{"currency": "$", "price": "12.99", "quantity": 10, "size": "30.0 x 30.0"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "31.0 x 31.0"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "32.0 x 32.0"}],
                                           "Red": [{"currency": "$", "price": "12.99", "quantity": 10, "size": "30.0 x 30.0"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "31.0 x 31.0"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "32.0 x 32.0"}]},
                                           "sizetype": "2", "minprice": "12.99"}''')
        self.checkfilter("TestSizeDimensionItem", "color", thecorrectresponse)

    def test_sizefiltersizedim(self):
        thecorrectresponse = json.loads('''{"variants": {"32.0 x 32.0": [{"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10},
                                           {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10}],
                                           "31.0 x 31.0": [{"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10},
                                           {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10}],
                                           "30.0 x 30.0": [{"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10},
                                           {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10}]},
                                           "sizetype": "2", "minprice": "12.99"}''')
        self.checkfilter("TestSizeDimensionItem", "size", thecorrectresponse)

    def test_quantityfiltersizedim(self):
        thecorrectresponse = json.loads('''{"variants": {"10": [{"color": "Red", "currency": "$", "price": "12.99", "size": "30.0 x 30.0"},
                                           {"color": "Blue", "currency": "$", "price": "12.99", "size": "31.0 x 31.0"},
                                           {"color": "Red", "currency": "$", "price": "12.99", "size": "32.0 x 32.0"},
                                           {"color": "Blue", "currency": "$", "price": "12.99", "size": "30.0 x 30.0"},
                                           {"color": "Red", "currency": "$", "price": "12.99", "size": "31.0 x 31.0"},
                                           {"color": "Blue", "currency": "$", "price": "12.99", "size": "32.0 x 32.0"}]},
                                           "sizetype": "2", "minprice": "12.99"}''')
        self.checkfilter("TestSizeDimensionItem", "quantity", thecorrectresponse)

    def test_currencyfiltersizedim(self):
        thecorrectresponse = json.loads('''{"variants": {"$": [{"color": "Red", "price": "12.99", "quantity": 10, "size": "30.0 x 30.0"},
                                           {"color": "Blue", "price": "12.99", "quantity": 10, "size": "31.0 x 31.0"},
                                           {"color": "Red", "price": "12.99", "quantity": 10, "size": "32.0 x 32.0"},
                                           {"color": "Blue", "price": "12.99", "quantity": 10, "size": "30.0 x 30.0"},
                                           {"color": "Red", "price": "12.99", "quantity": 10, "size": "31.0 x 31.0"},
                                           {"color": "Blue", "price": "12.99", "quantity": 10, "size": "32.0 x 32.0"}]},
                                           "sizetype": "2", "minprice": "12.99"}''')
        self.checkfilter("TestSizeDimensionItem", "currency", thecorrectresponse)

    def checkfilter(self, itemname, filtergroup, correctresponse):
        item = get_object_or_404(Product, slug__iexact=itemname, shop_id=1, parent__isnull=True)
        mybaseresponse = json.loads(get_variants(item, filtergroup))
        self.assertEqual(mybaseresponse, correctresponse, "the response was not as expected" )