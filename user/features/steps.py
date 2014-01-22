# -*- coding: utf-8 -*-
from common.lettuce_utils import *
from django.test.client import Client
from lettuce import *
from lxml import html
from nose.tools import *
from user.models import TinvilleUser
import lettuce.django
from selenium import webdriver
import time

@before.all
def set_browser():
    world.browser = Client()
    world.firefox = webdriver.Firefox()

@after.all
def foo(step):
    world.firefox.quit()

@step(u'I access the registration page')
def access_url(step):
    response = world.browser.get('/register')
    assert_equals(200, response.status_code)
    world.dom = html.fromstring(response.content)

@step(u'I see information to register as a designer')
def see_information_to_register_as_a_designer(step):
    assert_text_exists_in_first_element('#viewDesignerDetails', 'Designer info not found')

@step(u'Or to register as a shopper')
def see_information_to_register_as_a_designer(step):
    assert_text_exists_in_first_element('#viewShopperDetails', 'Shopper info not found')

@step(u'all registration forms are initially collapsed')
def all_registration_forms_are_initially_collapsed(step):
    assert_selector_does_not_exist('.in')

@step(u'When I register for a shopper account with email "([^"]*)" and password "([^"]*)"')
def when_i_register_for_a_shopper_account_with_email_and_password(step, email, password):
    world.user_info = {
        "email": email,
        "password": password,
    }
    world.firefox.get(lettuce.django.get_server().url('/register'))
    world.firefox.find_element_by_id("shopperInfoButton").click()
    form = world.firefox.find_element_by_id("shopperRegistrationForm")
    form.find_element_by_name("first_name").send_keys("John")
    form.find_element_by_name("last_name").send_keys("Doe")
    form.find_element_by_name("email").send_keys(email)
    form.find_element_by_name("password").send_keys(password)
    form.find_element_by_name("password2").send_keys(password)
    form.find_element_by_name("shopperForm").click()
    user = TinvilleUser.objects.get(email=email)
    user.is_active = True
    user.save()

@step(u'(?:When|And) I sign in')
def and_i_sign_in(step):
    login_menu = world.firefox.find_element_by_id("lg-menuLogin")
    login_menu.find_element_by_link_text("SIGN IN").click()
    login_menu.find_element_by_name("username").send_keys(world.user_info["email"])
    login_menu.find_element_by_name("password").send_keys(world.user_info["password"])
    login_menu.find_element_by_name("submit").click()
    time.sleep(0.25)# wait for the ajax call

@step(u'Then I should be redirected to the home page')
def then_i_should_be_redirected_to_the_home_page(step):
    assert_equals(world.firefox.current_url, lettuce.django.get_server().url('/'))



# Helper methods
def assert_text_exists_in_first_element(selector, error_text):
    first_element = world.dom.cssselect(selector)[0]
    assert_true(len(html.tostring(first_element)) > 0, error_text)


