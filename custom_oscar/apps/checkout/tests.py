from django.test import TestCase
from user.models import TinvilleUser
from designer_shop.models import Shop
from common.factories import create_order
from custom_oscar.apps.checkout.mixins import SendOrderMixin
from django.db.models import get_model

Email = get_model('customer','Email')

class SendOrderMixinTests(TestCase):
    fixtures = ['all.json']

    def setUp(self):
        self.user = TinvilleUser.objects.create(email="andrewfdabrowski@gmail.com")
        self.shop = Shop.objects.create(name='SchmoeVille', user=self.user)
        self.order = create_order(number="2-10011",user=self.user, shop=self.shop)
        self.top_level_order = create_order(number=10011,user=self.user, shop=self.shop)
        self.sendOrderMixin = SendOrderMixin()

    def Send_Valid_New_Order_Email_Test(self):
        self.sendOrderMixin.send_new_order_email(self.top_level_order)
        email = Email.objects.get(user_id=self.user.id)
        self.assertEqual(email.user.email, self.user.email)
        self.assertEqual(email.subject, "New Customer Order Placed", "Because the subject should be equal")
        self.assertEqual(email.body_text, "Hello, /n You have a new order available.", "Because the text body should be equal")
        self.assertEqual(email.body_html, "<html><div>Hello,</div><div> You have a new order available.</div></html>", "Because the html body should be equal")