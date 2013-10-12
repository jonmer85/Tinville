import httplib
import datetime
from django.test import TestCase
from django.core.urlresolvers import reverse
import pytz
from Tinville.user.models import TinvilleUser
from Tinville.settings.base import TIME_ZONE


class TestUserViews(TestCase):


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

        success_url = reverse('notifications')
        self.assertRedirects(resp, success_url, httplib.FOUND, httplib.OK)
        user = TinvilleUser.objects.get(email=email)
        self.assertEqual(user.first_name, first)
        self.assertEqual(user.last_name, last)
        self.assertEqual(user.email, email)
        self.assertEqual(user.last_login.astimezone(local_tz), local_tz.localize(last_login))
        self.failIfEqual(user.password, password)  # Should fail since it should be is a hashed password
        self.assertTrue(user.is_seller)
        self.assertFalse(user.is_active)
        self.assertEqual(list(user.styles.all().values_list('id', flat=True)), styles)

    def test_post_create_shopper_view_success(self):
        first, last, email, shop_name, last_login, password, styles, resp \
            = self.post_test_user_data(shop_name='', view_name='create-shopper')

        local_tz = pytz.timezone(TIME_ZONE)

        success_url = reverse('notifications')
        self.assertRedirects(resp, success_url, httplib.FOUND, httplib.OK)
        user = TinvilleUser.objects.get(email=email)
        self.assertEqual(user.first_name, first)
        self.assertEqual(user.last_name, last)
        self.assertEqual(user.email, email)
        self.assertEqual(user.shop_name, shop_name)
        self.assertEqual(user.last_login.astimezone(local_tz), local_tz.localize(last_login))
        self.failIfEqual(user.password, password)  # Should fail since it should be is a hashed password
        self.assertFalse(user.is_seller)
        self.assertFalse(user.is_active)
        self.assertEqual(list(user.styles.all().values_list('id', flat=True)), styles)

    def test_get_activation_view_designer(self):
        first, last, email, shop_name, last_login, password, styles, resp = self.post_test_user_data()

        user = TinvilleUser.objects.get(email=email)
        self.assertTrue(user.is_seller)
        self.assertFalse(user.is_active)

        resp = self.client.get(reverse('activate-user', kwargs={'activation_key': user.activation_key}))
        user = TinvilleUser.objects.get(email=email)
        self.assertTemplateUsed(resp, 'notification.html')
        self.assertTrue(user.is_active)  # User should now be activated
        self.assertTrue(user.is_seller)
        self.assertEqual(resp.cookies['messages'].value, '')  # Messages should be cleared when rendered by template
        self.assertContains(resp, 'alert-success')

    def test_get_activation_view_designer_already_authenticated(self):
        first, last, email, shop_name, last_login, password, styles, resp = self.post_test_user_data()

        user = TinvilleUser.objects.get(email=email)
        user.is_active = True
        user.save()
        success = self.client.login(username=email, password=password)
        self.assertTrue(success)

        self.assertTrue(user.is_seller)
        self.assertTrue(user.is_active)

        resp = self.client.get(reverse('activate-user', kwargs={'activation_key': user.activation_key}))
        self.assertTemplateUsed(resp, 'notification.html')
        self.assertEqual(resp.cookies['messages'].value, '')  # Messages should be cleared when rendered by template
        self.assertContains(resp, 'alert-warning')

    def test_get_activation_view_while_another_user_is_signed_in(self):
        # Create a designer, log them in
        first, last, email, shop_name, last_login, password, styles, resp = self.post_test_user_data()
        user = TinvilleUser.objects.get(email=email)
        user.is_active = True
        user.save()
        success = self.client.login(username=email, password=password)
        self.assertTrue(success)

        # Now create another user and activate them, it should still activate even if the other user has a logged in
        # session
        first2, last2, email2, shop_name2, last_login2, password2, styles2, resp2 = \
            self.post_test_user_data(email="joe2@schmoe.com", shop_name="SchmoeShop")
        user = TinvilleUser.objects.get(email=email2)
        self.assertTrue(user.is_seller)
        self.assertFalse(user.is_active)

        resp = self.client.get(reverse('activate-user', kwargs={'activation_key': user.activation_key}))
        self.assertTemplateUsed(resp, 'notification.html')
        user = TinvilleUser.objects.get(email=email2)
        self.assertTrue(user.is_active)  # User should now be activated
        self.assertTrue(user.is_seller)
        self.assertEqual(resp.cookies['messages'].value, '')  # Messages should be cleared when rendered by template
        self.assertContains(resp, 'alert-success')

    def test_get_login_success(self):
        first, last, email, shop_name, last_login, password, styles, resp = self.post_test_user_data()

        user = TinvilleUser.objects.get(email=email)
        user.is_active = True
        user.save()
        resp = self.client.get(reverse('home'))
        self.assertNotContains(resp, first)  # Home page contains user's first name when logged in

        resp = self.client.post(reverse('login'),
                                {'username': email,
                                 'password': password,
                                 'remember_me': False,
                                }
                        )
        # self.assertRedirects(resp, reverse('home'), status_code=httplib.OK)   Jon M TBD - For some reason this fails...
        self.assertEqual(resp['Location'], 'http://testserver' + reverse('home'))
        self.assertEqual(resp.status_code, httplib.FOUND)
        resp = self.client.get(reverse('home'))
        self.assertContains(resp, 'JOE')  # Home page contains user's first name when logged in


    ### Utilities
    def post_test_user_data(self, first=None, last=None, email=None, shop_name=None,
                            last_login=None, password=None, password2=None, styles=None,
                            view_name=None):

        view_name = view_name or 'create-designer'
        create_url = reverse(view_name)
        first = first or 'Joe'
        last = last or 'Schmoe'
        email = email or 'joe@schmoe.com'
        shop_name = shop_name or 'SchmoeVille'

        last_login = last_login or datetime.datetime.now()
        password = password or 'test'
        password2 = password2 or password
        styles = styles or [1, 3, 5]
        resp = self.client.post(create_url,
                                {'first_name': first,
                                 'last_name': last,
                                 'shop_name': shop_name,
                                 'email': email,
                                 'password': password,
                                 'password2': password2,
                                 'last_login': last_login,
                                 'styles': styles,
                                 }
                                )

        return first, last, email, shop_name, last_login, password, styles, resp


