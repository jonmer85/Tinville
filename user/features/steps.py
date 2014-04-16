# -*- coding: utf-8 -*-
from common.lettuce_utils import *
import cssselect
from lettuce import step
from nose.tools import assert_equals
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

@step(u'When I register for a shop named "([^"]*)"')
def when_i_register_for_a_shop(step, shop_name):
    form = fill_in_user_form(email="joe@schmoe.com", password="test")
    world.user_info['shop_name'] = shop_name
    form.find_element_by_id("designer").click()
    form.find_element_by_name("shop_name").send_keys(shop_name)
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
    sign_in()


@step(u'When I fill in the login screen with email "([^"]*)" and password "([^"]*)"')
def when_i_fill_in_login_screen_with_email_and_password(step, email, password):
    world.user_info = {
        "email": email,
        "password": password,
    }
    sign_in()



@step(u'Then I should see an error telling me that the email is required')
def then_i_should_see_an_error_telling_me_that_email_is_required(step):
    assert_selector_does_exist("#lg-menuLogin #div_id_username.has-error")



@step(u'Then I should be redirected to the home page')
def then_i_should_be_redirected_to_the_home_page(step):
    assert_equals(world.browser.current_url, lettuce.django.get_server().url('/'))

@step(u'Then I can visit my shop at "([^"]*)"')
def then_i_can_visit_my_shop(step, url):
    world.browser.get(lettuce.django.get_server().url(url))
    assert_not_equals(world.browser.title, 'Server Error', world.browser.page_source)

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

def sign_in():
    login_menu = world.browser.find_element_by_id("lg-menuLogin")
    login_menu.find_element_by_link_text("SIGN IN").click()
    login_menu.find_element_by_name("username").send_keys(world.user_info["email"])
    login_menu.find_element_by_name("password").send_keys(world.user_info["password"])
    login_menu.find_element_by_name("submit").click()
    wait_for_ajax_to_complete()


