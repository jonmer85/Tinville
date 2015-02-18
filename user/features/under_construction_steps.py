from common.lettuce_utils import *
import cssselect
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
from user.models import TinvilleUser
import lettuce.django
from selenium.common.exceptions import *

@step(u'Then I should be redirected to the under construction page')
def then_I_should_be_redirected_to_the_under_construction_page(step):
    world.browser.get(lettuce.django.get_server().url('/under_contruction'))

@step(u'And the shop is approved')
def and_the_shop_is_approved(step):
    user = TinvilleUser.objects.get(email="joe@schmoe.com")
    user.is_approved = True
    user.save()

@step(u'And the shop is not approved')
def and_the_shop_is_not_approved(step):
    user = TinvilleUser.objects.get(email="joe@schmoe.com")
    user.is_approved = False
    user.save()

@step(u'Given the demo shop$')
def given_the_demo_shop(step):
    world.browser.get(lettuce.django.get_server().url('/Demo'))
    wait_for_browser_to_have_url(lettuce.django.get_server().url('/access_code?shop=Demo'))
    user = TinvilleUser.objects.get(email="demo@user.com")
    form = fill_in_access_form(access_code=user.access_code)
    form.submit()