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

# class SocialBoard(models.Model):
    # user (fk)
    # date_created
    # name
    # description
    # is_deleted
    # is_browsable

# class SocialBoardImage
    # date_created
    # user (fk)
    # url
    # cropping
    # location
    # is_deleted
    # date_deleted

# class SocialUsedImage
    # social_image (fk)
    # social_board (fk)
    # date_added (fk)

# class SocialVote(models.Model):
    # social_board (fk)
    # user (fk)
    # competition (fk)
    # date_created
    # is_stale

# class SocialFollow(models.Model):
    # following_user (fk)
    # followed_user (fk)
    # date_followed
    # is_stale

# class SocialCompetition
    # name
    # description
    # prize
    # date_created
    # date_competition_start
    # date_competition_end
    # is_active

# class SocialCompetitionsEntries
    # social_board (fk)
    # social_competition (fk)

# facebook sharing

