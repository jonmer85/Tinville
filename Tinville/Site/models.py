from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
    )

# Create your models here.


class TinvilleUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=TinvilleUserManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
                                password=password,
                                first_name=first_name,
                                last_name=last_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class TinvilleUser(AbstractBaseUser):

    email = models.EmailField(verbose_name='email address', unique=True, db_index=True, max_length=254)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # Seller/Designer fields
    is_seller = models.BooleanField(default=True)
    other_site_url = models.URLField(verbose_name='Other Site URL', max_length=2083)
    shop_name = models.CharField(verbose_name="Shop name", unique=True, db_index=True, max_length=100)


    objects = TinvilleUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

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

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin






