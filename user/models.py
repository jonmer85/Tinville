import datetime
import random
import hashlib
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
    )
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils.timezone import utc
from django.core.exceptions import ObjectDoesNotExist
from autoslug import AutoSlugField

from oscar.apps.customer.abstract_models import UserManager, AbstractUser
from oscar.core.loading import get_model

from Tinville.settings.base import EMAIL_HOST_USER



class TinvilleUserManager(UserManager):

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = super(TinvilleUserManager, self).create_superuser(email, password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class TinvilleUser(AbstractUser):
    # email = _metamodels.EmailField(verbose_name='email address', unique=True, db_index=True, max_length=254)
    slug = AutoSlugField(populate_from='email', unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = False
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(auto_now_add=True)

    # Seller/Designer fields
    is_seller = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    account_token = models.CharField(max_length=255)
    full_legal_name = models.CharField(max_length=255)
    recipient_id = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=255)
    promoter_code = models.CharField(max_length=5)

    objects = TinvilleUserManager()

    def generate_activation_information(self):

         # Build the activation key for their account
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        self.activation_key = hashlib.sha1(salt+self.email).hexdigest()
        self.key_expires = datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(7)  # Give 7 days to confirm
        self.save()

    def generate_promoter_code(self):
         # Generates random promoter code for shop
        promoter_code_candidate = None
        while True:
            promoter_code_candidate = get_random_string(24, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            try:
                TinvilleUser.objects.get(promoter_code=promoter_code_candidate)
                pass
            except ObjectDoesNotExist:
                break
        self.promoter_code = promoter_code_candidate
        self.save()

    def delete(self, *args, **kwargs):
        Partner = get_model("partner", "Partner")
        if self.is_seller:
            partner = Partner.objects.get(name=self.email)
            if partner is not None:
                partner.delete()
        super(TinvilleUser, self).delete(*args, **kwargs)

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def send_confirmation_email(self, base_url, scheme):

        # Send an email with the confirmation link
        confirmation_url = reverse('activate-user', kwargs={'activation_key': self.activation_key})

        email_subject = 'Your new Tinville account confirmation'
        email_body = "Thanks for signing up for a Tinville account!\n\nTo activate your account, click" \
                     " this link within 7 days:\n\n%s" % (scheme+"://"+base_url+confirmation_url)

        send_mail(email_subject, email_body, EMAIL_HOST_USER, [self.email])


class DesignerPayout(models.Model):
    designer = models.ForeignKey('TinvilleUser')
    datetime = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    # The reference should refer to the transaction ID of the payment gateway
    # that was used for this event.
    reference = models.CharField("Reference", max_length=128, blank=True)

class PromoterPayout(models.Model):
    promoter = models.ForeignKey('TinvilleUser')
    datetime = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    # The reference should refer to the transaction ID of the payment gateway
    # that was used for this event.
    reference = models.CharField("Reference", max_length=128, blank=True)

class UserPaymentMethod(models.Model):
    user = models.ForeignKey('TinvilleUser')
    card_token = models.CharField(max_length=255)
    card_fingerprint = models.CharField(max_length=255)
    is_default_for_user = models.BooleanField(default=False)
