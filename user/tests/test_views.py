import httplib
import datetime
from designer_shop.models import Shop
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.forms import ValidationError
import pytz
from user.models import TinvilleUser
from Tinville.settings.base import TIME_ZONE
import re

class RegistrationTest(TestCase):
    def setUp(self):
        self.registration_url = reverse('user.views.register')

    def test_get_register_view(self):
        self.assertTemplateUsed(self.get_request(), 'register.html')

    def test_email(self):
        self.assertEqual(self.post_request_user(email='john@schmoe.com').email, 'john@schmoe.com')

    def test_password_hashed(self):
        self.failIfEqual(self.post_request_user(password='foo'), 'foo')

    def test_is_shopper(self):
        self.assertFalse(self.post_request_user(is_seller=False).is_seller)

    def test_is_seller(self):
        self.assertTrue(self.post_request_user(is_seller=True, shop_name="SchmoeShop").is_seller)

    def test_is_seller_shop_name_with_spaces(self):
        user = self.post_request_user(is_seller=True, shop_name='Casa de Schmoe')
        shop = Shop.objects.get(user=user)
        self.assertEquals(shop.name, 'Casa de Schmoe')
        self.assertEquals(shop.slug, 'casa-de-schmoe')

    ### Utilities
    def get_request(self):
        response = self.client.get(self.registration_url, {
            'email': 'joe@schmoe.com',
            'password': 'test',
        })
        self.assertEqual(response.status_code, httplib.OK)
        return response

    def post_request_user(self, email='joe@schmoe.com', last_login=datetime.datetime.now(),
                          password='test', is_seller=False, shop_name=''):
        self.client.post(self.registration_url, {
            'email': email,
            'password': password,
            'last_login': last_login,
            'is_seller': is_seller,
            'shop_name': shop_name,
        })
        return TinvilleUser.objects.get(email=email)
