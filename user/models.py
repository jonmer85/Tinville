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


class TinvilleUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=TinvilleUserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
                                password=password,
                                )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class TinvilleUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', unique=True, db_index=True, max_length=254)
    slug = AutoSlugField(populate_from='email', unique=True)

    is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(auto_now_add=True)

    # Seller/Designer fields
    is_seller = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    objects = TinvilleUserManager()

    USERNAME_FIELD = "email"

    def generate_activation_information(self):

         # Build the activation key for their account
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        self.activation_key = hashlib.sha1(salt+self.email).hexdigest()
        self.key_expires = datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(7)  # Give 7 days to confirm
        self.save()

    def save(self, *args, **kwargs):

        super(TinvilleUser, self).save(*args, **kwargs)

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

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
        email_body = "Thanks for signing up for a Tinville account!\n\nTo activate your account, click" \
                     " this link within 7 days:\n\n%s" % (base_url+confirmation_url)

        send_mail(email_subject, email_body, EMAIL_HOST_USER, [self.email])

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
