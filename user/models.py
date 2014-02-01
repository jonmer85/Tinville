import datetime
import random
import hashlib
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
    )
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.utils.timezone import utc
from autoslug import AutoSlugField

import designer_shop.models

from Tinville.settings.base import EMAIL_HOST_USER


# Create your models here.

class FashionStyles(models.Model):
    style = models.CharField(max_length=100)

    def __unicode__(self):
        return self.style

class TinvilleUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', unique=True, db_index=True, max_length=254)
    slug = AutoSlugField(populate_from='email', unique=True)

    is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(auto_now_add=True)

    # Seller/Designer fields
    is_seller = models.BooleanField(default=False)
    other_site_url = models.URLField(verbose_name='Other Site URL', max_length=2083, blank=True)
    shop_name = models.CharField(verbose_name="Shop name", unique=True, blank=True, null=True, db_index=True,
                                 default=None, max_length=100)
    is_approved = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    def generate_activation_information(self):

         # Build the activation key for their account
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        self.activation_key = hashlib.sha1(salt+self.email).hexdigest()
        self.key_expires = datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(7)  # Give 7 days to confirm
        self.save()


    def save(self, *args, **kwargs):

        if not self.shop_name:
            self.shop_name = None

        super(TinvilleUser, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        #TODO Add permission system for designer pages
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        #TODO Add permission system for designer pages
        return True

    def send_confirmation_email(self, base_url):

        # Send an email with the confirmation link
        confirmation_url = reverse('activate-user', kwargs={'activation_key': self.activation_key})

        email_subject = 'Your new Tinville account confirmation'
        email_body = "Hello %s! Thanks for signing up for a Tinville account!\n\nTo activate your account, click" \
                     " this link within 7 days:\n\n%s" % (self.email, base_url+confirmation_url)

        send_mail(email_subject, email_body, EMAIL_HOST_USER, [self.email])

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
