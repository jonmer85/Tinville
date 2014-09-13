from designer_shop.views import *
from django.test import TestCase
import json

class ItemVarientService(TestCase):
    fixtures = ['all.json',]

    def test_nofiltersizeset(self):
        thecorrectresponse =json.loads('''{"variants": [{"color": "Red", "currency": "$", "price": "12.99", "quantity": 10, "size": "XXS"},
                                        {"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10, "size": "XXS"},
                                        {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10, "size": "XS"},
                                        {"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10, "size": "XS"},
                                        {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10, "size": "SM"},
                                        {"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10, "size": "SM"}],
                                        "sizetype": "1", "minprice": "12.99"}''')
        self.checkfilter("TestSizeSetItem", None, thecorrectresponse)

    def test_pricefiltersizeset(self):
        thecorrectresponse = json.loads('''{"variants": {"12.99": [{"color": "Red", "currency": "$", "quantity": 10, "size": "XXS"},
                                           {"color": "Blue", "currency": "$", "quantity": 10, "size": "XXS"},
                                           {"color": "Red", "currency": "$", "quantity": 10, "size": "XS"},
                                           {"color": "Blue", "currency": "$", "quantity": 10, "size": "XS"},
                                           {"color": "Red", "currency": "$", "quantity": 10, "size": "SM"},
                                           {"color": "Blue", "currency": "$", "quantity": 10, "size": "SM"}]},
                                           "sizetype": "1", "minprice": "12.99"}''')
        self.checkfilter("TestSizeSetItem", "price", thecorrectresponse)

    def test_colorfiltersizeset(self):
        thecorrectresponse = json.loads('''{"variants": {"Blue": [{"currency": "$", "price": "12.99", "quantity": 10, "size": "SM"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "XS"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "XXS"}],
                                           "Red": [{"currency": "$", "price": "12.99", "quantity": 10, "size": "SM"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "XS"},
                                           {"currency": "$", "price": "12.99", "quantity": 10, "size": "XXS"}]},
                                           "sizetype": "1", "minprice": "12.99"}''')
        self.checkfilter("TestSizeSetItem", "color", thecorrectresponse)

    def test_sizefiltersizeset(self):
        thecorrectresponse = json.loads('''{"variants": {"XXS": [{"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10},
                                           {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10}],
                                           "XS": [{"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10},
                                           {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10}],
                                           "SM": [{"color": "Blue", "currency": "$", "price": "12.99", "quantity": 10},
                                           {"color": "Red", "currency": "$", "price": "12.99", "quantity": 10}]},
                                           "sizetype": "1", "minprice": "12.99"}''')
        self.checkfilter("TestSizeSetItem", "size", thecorrectresponse)

    def test_quantityfiltersizeset(self):
        thecorrectresponse = json.loads('''{"variants": {"10": [{"color": "Red", "currency": "$", "price": "12.99", "size": "XXS"},
                                           {"color": "Blue", "currency": "$", "price": "12.99", "size": "XXS"},
                                           {"color": "Red", "currency": "$", "price": "12.99", "size": "XS"},
                                           {"color": "Blue", "currency": "$", "price": "12.99", "size": "XS"},
                                           {"color": "Red", "currency": "$", "price": "12.99", "size": "SM"},
                                           {"color": "Blue", "currency": "$", "price": "12.99", "size": "SM"}]},
                                           "sizetype": "1", "minprice": "12.99"}''')
        self.checkfilter("TestSizeSetItem", "quantity", thecorrectresponse)

    def test_currencyfiltersizeset(self):
        thecorrectresponse = json.loads('''{"variants": {"$": [{"color": "Red", "price": "12.99", "quantity": 10, "size": "XXS"},
                                           {"color": "Blue", "price": "12.99", "quantity": 10, "size": "XXS"},
                                           {"color": "Red", "price": "12.99", "quantity": 10, "size": "XS"},
                                           {"color": "Blue", "price": "12.99", "quantity": 10, "size": "XS"},
                                           {"color": "Red", "price": "12.99", "quantity": 10, "size": "SM"},
                                           {"color": "Blue", "price": "12.99", "quantity": 10, "size": "SM"}]},
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