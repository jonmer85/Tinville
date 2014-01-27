# -*- coding: utf-8 -*-
from common.lettuce_utils import *
from lettuce import step
from nose.tools import assert_equals
from user.models import TinvilleUser
import lettuce.django

@step(u'I access the registration page')
def access_registration_url(step):
    world.browser.get(lettuce.django.get_server().url('/register'))

@step(u'When I register for a shopper account with email "([^"]*)" and password "([^"]*)"')
def when_i_register_for_a_shopper_account_with_email_and_password(step, email, password):
    access_registration_url(step)
    world.user_info = {
        "email": email,
        "password": password,
    }
    form = world.browser.find_element_by_id("registrationForm")
    form.find_element_by_name("email").send_keys(email)
    form.find_element_by_name("password").send_keys(password)
    form.find_element_by_name("password2").send_keys(password)
    form.submit()
    user = TinvilleUser.objects.get(email=email)
    user.is_active = True
    user.save()

@step(u'(?:When|And) I sign in')
def and_i_sign_in(step):
    login_menu = world.browser.find_element_by_id("lg-menuLogin")
    login_menu.find_element_by_link_text("SIGN IN").click()
    login_menu.find_element_by_name("username").send_keys(world.user_info["email"])
    login_menu.find_element_by_name("password").send_keys(world.user_info["password"])
    login_menu.find_element_by_name("submit").click()
    wait_for_ajax_to_complete()

@step(u'Then I should be redirected to the home page')
def then_i_should_be_redirected_to_the_home_page(step):
    assert_equals(world.browser.current_url, lettuce.django.get_server().url('/'))


