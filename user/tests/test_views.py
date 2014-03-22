import httplib
import datetime
from django.utils import unittest
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

    ### Utilities
    def get_request(self):
        response = self.client.get(self.registration_url, {
            'email': 'joe@schmoe.com',
            'password': 'test',
        })
        self.assertEqual(response.status_code, httplib.OK)
        return response

    def post_request_user(self, email='joe@schmoe.com', last_login=datetime.datetime.now(),
                          password='test', is_seller=False, shop_name=None):
        self.client.post(self.registration_url, {
            'email': email,
            'password': password,
            'last_login': last_login,
            'is_seller': is_seller,
            'shop_name': shop_name,
        })
        return TinvilleUser.objects.get(email=email)

def ActivationTest(TestCase):
    def setUp(self):
        self.user = TinvilleUser.objects.create()

    def test_unconfirmed(self):
        self.assertFalse(self.user.is_active)

    def test_confirmed(self):
        self.client.get(reverse('activate-user', kwargs={'activation_key': self.user.activation_key}))
        self.assertTrue(TinvilleUser.objects.get(id=self.user.id).is_active)

    def test_already_registered_warning(self):
        self.user.is_active = True
        self.user.save()
        response = self.client.get(reverse('activate-user', kwargs={'activation_key': self.user.activation_key}))
        self.assertRegexpMatches(
            response.content,
            re.compile(".*Your account already exists and is activated.*"),
        )

    def test_other_user_logged_in(self):
        other_user = TinvilleUser.objects.create(
            is_active=True,
            email='joe@schmoe.com',
            password='test',
        )
        self.client.login(username=other_user.email, password='test')
        self.client.get(reverse('activate-user', kwargs={'activation_key': self.user.activation_key}))
        self.assertTrue(TinvilleUser.objects.get(id=self.user.id).is_active)
