import httplib
import datetime
from django.test import TestCase
from django.core.urlresolvers import reverse
import pytz
from Tinville.user.models import TinvilleUser
from Tinville.settings.base import TIME_ZONE

class TestUserViews(TestCase):



    def setUp(self):
        pass

    def test_get_register_view(self):
        create_url = reverse('register')
        resp = self.client.get(create_url)
        self.assertEqual(resp.status_code, httplib.OK)
        self.assertTemplateUsed(resp, 'register.html')

    def test_get_create_shopper_view(self):
        create_url = reverse('create-shopper')
        resp = self.client.get(create_url)
        self.assertEqual(resp.status_code, httplib.OK)
        self.assertTemplateUsed(resp, 'register_shopper.html')


    def test_get_create_designer_view(self):
        create_url = reverse('create-designer')
        resp = self.client.get(create_url)
        self.assertEqual(resp.status_code, httplib.OK)
        self.assertTemplateUsed(resp, 'register_designer.html')

    def test_post_create_designer_view_success(self):
        first, last, email, shop_name, last_login, password, styles, resp = self.post_test_user_data()

        local_tz = pytz.timezone(TIME_ZONE)

        success_url = reverse('create-designer')
        self.assertRedirects(resp, success_url, httplib.FOUND, httplib.OK)
        user = TinvilleUser.objects.get(email=email)
        self.assertEqual(user.first_name, first)
        self.assertEqual(user.last_name, last)
        self.assertEqual(user.email, email)
        self.assertEqual(user.shop_name, shop_name)
        self.assertEqual(user.last_login.astimezone(local_tz), local_tz.localize(last_login))
        self.failIfEqual(user.password, password)  # Should fail since it should be is a hashed password
        self.assertEqual(user.styles, styles)



    def test_post_create_designer_view_duplicate_email(self):
        duplicate_email = 'joe@schmoe.com'
        TinvilleUser.objects.create_user(duplicate_email, 'joe', 'schmoe', 'test_password')
        first, last, email, shop_name, last_login, password, styles, resp \
            = self.post_test_user_data('jon', 'smith', duplicate_email)

        self.assertEqual(resp.status_code, httplib.OK)  # Return the page again with form error

    ### Utilities
    def post_test_user_data(self, first=None, last=None, email=None, shop_name=None,
                            last_login=None, password=None, password2=None, styles=None):
        create_url = reverse('create-designer')
        first = first or 'Joe'
        last = last or 'Schmoe'
        email = email or 'joe@schmoe.com'
        shop_name = shop_name or 'SchmoeVille'

        last_login = last_login or datetime.datetime.now()
        password = password or 'test'
        password2 = password2 or password
        styles = styles or ('1', '3', '5')
        resp = self.client.post(create_url,
                                {'first_name': first,
                                 'last_name': last,
                                 'shop_name': shop_name,
                                 'email': email,
                                 'password': password,
                                 'password2': password2,
                                 'last_login': last_login,
                                 'styles': styles,
                                })

        return first, last, email, shop_name, last_login, password, styles, resp


