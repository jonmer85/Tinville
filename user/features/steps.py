# -*- coding: utf-8 -*-
from common.lettuce_utils import *
import cssselect
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
from user.models import TinvilleUser
import lettuce.django
from selenium.common.exceptions import * 

@step(u'I access the registration page')
def access_registration_url(step):
    world.browser.get(lettuce.django.get_server().url('/register'))

@step(u'I access the home page')
def access_home_url(step):
    world.browser.get(lettuce.django.get_server().url('/'))

@step(u'(?:When|And) I register for a shopper account with email "([^"]*)" and password "([^"]*)"')
def when_i_register_for_a_shopper_account_with_email_and_password(step, email, password):
    form = fill_in_user_form(email=email, password=password)
    submit_form_and_activate_user(form)

@step(u'(?:When|And) I register for a shop named "([^"]*)"')
def when_i_register_for_a_shop(step, shop_name):
    register_basic_shop(shop_name, "joe@schmoe.com", "test")

@step(u'(?:When|And|Or) I try to register a shop named "([^"]*)"')
def when_i_register_for_a_shop(step, shop_name):
    form = fill_out_designer_registration_form("test", shop_name, "joe@schmoe.com")
    form.submit()

@step(u'When a shop named "([^"]*)" already exists')
def when_a_shop_already_exists(step, shop_name):
    register_basic_shop(shop_name, "cock@blocker.com", "test")


def fill_out_designer_registration_form(password, shop_name, user):
    form = fill_in_user_form(email=user, password=password)
    world.user_info['shop_name'] = shop_name
    form.find_element_by_id("designer").click()
    form.find_element_by_name("shop_name").send_keys(shop_name)
    return form


def register_basic_shop(shop_name, user, password):
    form = fill_out_designer_registration_form(password, shop_name, user)
    submit_form_and_activate_user(form)


def fill_in_user_form(email, password):
    access_registration_url(step)
    world.user_info = {
        "email": email,
        "password": password,
    }
    form = world.browser.find_element_by_id("registrationForm")
    form.find_element_by_name("email").send_keys(email)
    form.find_element_by_name("password").send_keys(password)
    return form

def submit_form_and_activate_user(form):
    form.submit()
    user = TinvilleUser.objects.get(email=world.user_info['email'].lower())
    user.is_active = True
    user.save()

@step(u'(?:When|And) I sign in')
def and_i_sign_in(step):
    sign_in_local()


@step(u'When I fill in the login screen with email "([^"]*)" and password "([^"]*)"')
def when_i_fill_in_login_screen_with_email_and_password(step, email, password):
    world.user_info = {
        "email": email,
        "password": password,
    }
    sign_in_local()



@step(u'Then I should see an error telling me that the email is required')
def then_i_should_see_an_error_telling_me_that_email_is_required(step):
    assert_selector_does_exist("#lg-menuLogin #div_id_username.has-error")

@step(u'I should get an error that the shop already exists')
def then_i_should_see_an_error_telling_me_that_shop_exists(step):
    assert_selector_does_exist("#div_id_shop_name.has-error")
    assert_selector_contains_text("#error_1_id_shop_name strong", "Shop name is already taken.")



@step(u'Then I should be redirected to the home page')
def then_i_should_be_redirected_to_the_home_page(step):
    assert_equals(world.browser.current_url, lettuce.django.get_server().url('/'))

@step(u'(?:Then|And) I can visit my shop at "([^"]*)"')
def then_i_can_visit_my_shop(step, url):
    absoluteUrl = lettuce.django.get_server().url(url)
    world.browser.get(absoluteUrl)
    assert_page_exist(url)

@step(u'I should see a confirmation notification prompting me to activate the account via email instructions to "([^"]*)"')
def i_should_see_a_confirmation_notification(step, email):
    assert_class_exists('alert-success')
    assert_selector_contains_text('div.alert-success', email)


@step(u"Then I can't fill in the shop name")
def then_i_can_t_fill_in_the_shop_name(step):
    assert_raises(
        ElementNotVisibleException,
        world.browser.find_element_by_name("shop_name").send_keys,
        "foo",
    )

@step(u'Then I should not see validation errors')
def then_i_should_not_see_validation_errors(step):
    assert_raises(
        NoSuchElementException,
        world.browser.find_element_by_class_name,
        "has-error",
    )

@step(u'Then I should get a validation error on email address')
def then_i_should_get_a_validation_error_on_email_address(step):
    assert_equals(world.browser.current_url, lettuce.django.get_server().url('/register'))
    assert_class_exists('has-error')


# Utilities

def sign_in_local():
    sign_in(world.user_info["email"], world.user_info["password"])


