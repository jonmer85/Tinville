from common.lettuce_utils import *
import cssselect
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
from user.models import TinvilleUser
import lettuce.django
from selenium.common.exceptions import *

@step(u'Given the shop page')
def Given_the_shop_page(step):
    world.browser.get(lettuce.django.get_server().url('/shop'))