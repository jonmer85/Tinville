from common.lettuce_extensions import get_server
from common.lettuce_utils import *
import cssselect
from django.conf import settings
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
from user.models import TinvilleUser
import lettuce.django
from selenium.common.exceptions import *

@step(u'Then I should be redirected to the under construction page')
def then_I_should_be_redirected_to_the_under_construction_page(step):
    world.browser.get(get_server().url('/under_construction'))

@step(u'When the shop is approved')
def When_the_shop_is_approved(step):
    user = TinvilleUser.objects.get(email="demo@user.com")
    user.is_approved = True
    user.save()

@step(u'When the shop is not approved')
def When_the_shop_is_not_approved(step):
    user = TinvilleUser.objects.get(email="demo@user.com")
    user.is_approved = False
    user.save()

@step(u'And their shop is not approved')
def and_the_shop_is_not_approved(step):
    user = TinvilleUser.objects.get(email="joe@schmoe.com")
    user.is_approved = False
    user.save()

@step(u'Given the demo shop$')
def given_the_demo_shop(step):
    world.browser.get(get_server().url('/Demo/'))
    wait_for_browser_to_have_url(get_server().url('/access_code?shop=Demo'))
    user = TinvilleUser.objects.get(email="demo@user.com")
    form = fill_in_access_form(access_code=user.access_code)
    form.submit()

@step(u'(?:Then|And) I visit my new shop at "([^"]*)"')
def then_i_visit_my_new_shop(step, url):
    absoluteUrl = get_server().url(url)
    world.browser.get(absoluteUrl)

@step(u'(?:Then|And) I can visit my new shop at "([^"]*)"')
def then_i_can_visit_my_new_shop(step, url):
    absoluteUrl = get_server().url(url)
    world.browser.get(absoluteUrl)
    wait_for_browser_to_have_url(absoluteUrl+"/")
    assert_page_exist(absoluteUrl)

@step(u'Then I can visit the demo shop$')
def then_i_can_visit_the_demo_shop(step):
    world.browser.get(get_server().url('/Demo/'))
    if not settings.DISABLE_BETA_ACCESS_CHECK:
        wait_for_browser_to_have_url(get_server().url('/access_code?shop=Demo'))
        user = TinvilleUser.objects.get(email="demo@user.com")
        form = fill_in_access_form(access_code=user.access_code)
        form.submit()