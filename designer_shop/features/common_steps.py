from lettuce import step
from django.core.management import call_command
import lettuce.django
import os
import time
import math

from Tinville.settings.base import MEDIA_ROOT
from designer_shop.models import Shop
from user.models import TinvilleUser
from selenium.webdriver.support.ui import Select
from common.lettuce_utils import *


@step(u'Given I have an item in the demo shop')
def given_I_have_an_item_in_the_shop(step):
    assert len(world.browser.find_elements_by_css_selector(".shopItem")) > 0