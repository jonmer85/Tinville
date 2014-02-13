from django.core.urlresolvers import resolve
from django.test import TestCase

class URLTest(TestCase):
    def test_designer_shop(self):
        self.assertEqual('designer_shop.views.shopper', resolve('/foo/').view_name)
        self.assertEqual('designer_shop.views.shopper', resolve('/bar/').view_name)

    def test_register(self):
        self.assertEqual('user.views.register', resolve('/register').view_name)
