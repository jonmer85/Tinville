from django.test import TestCase
from user.models import TinvilleUser
from designer_shop.models import Shop
from common.factories import create_order
from custom_oscar.apps.checkout.mixins import SendOrderMixin

class SendOrderMixinTests(TestCase):
    fixtures = ['all.json']

    def setUp(self):
        self.user = TinvilleUser.objects.create(email="foo@123.com")
        self.shop = Shop.objects.create(name='SchmoeVille', user=self.user)
        self.order = create_order(number="2-10011",user=self.user, shop=self.shop)

    def Send_Valid_New_Order_Email_Test(self):
        SendOrderMixin.send_new_order_email(self.order)
        pass