from django.test import TestCase
from django.db.utils import IntegrityError
from Tinville.Site.models import MailingListItem

class MailingListItemTest(TestCase):
    def test_duplicate(self):
        MailingListItem.objects.create(email="foo@bar.com")
        self.assertRaises(IntegrityError, MailingListItem.objects.create, email="foo@bar.com")
