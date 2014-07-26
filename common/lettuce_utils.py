from lettuce import *
from django.test import Client
from nose.tools import *
import lettuce.django
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from lxml import html


def wait_for_ajax_to_complete():
    WebDriverWait(world.browser, 10).until(ajax_complete,  "Timeout waiting for page to load")


def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass


def dom():
    return html.fromstring(world.browser.page_source)


def assert_class_exists(klass):
    world.browser.find_element_by_class_name(klass)


def assert_id_exists(id):
    world.browser.find_element_by_id(id)


def assert_class_does_not_exist(klass):
    try:
        world.browser.find_element_by_class_name(klass)
        assert False, 'Did not expect ' + klass + ' to be an element'
    except NoSuchElementException:
        pass


def assert_selector_does_exist(selector):
    try:
        world.browser.find_element_by_css_selector(selector)
        pass
    except NoSuchElementException:
        assert False, 'Expect ' + selector + ' to exist'


def assert_selector_does_not_exist(selector):
    try:
        world.browser.find_element_by_css_selector(selector)
        assert False, 'Did not expect ' + selector + ' to exist'
    except NoSuchElementException:
        pass


def assert_number_of_selectors(selector, n):
    assert_equals(len(dom().cssselect(selector)), n)


def assert_text_of_every_selector(selector, text):
    selector_found = False
    for item in dom().cssselect(selector):
        assert_equals(item.text, text)
        selector_found = True
    assert_true(selector_found, 'No elements found for ' + selector)


def assert_selector_contains_text(selector, text):
    assert_regexp_matches(
        dom().cssselect(selector)[0].text_content(),
        re.compile(".*" + text + ".*"),
    )


def assert_every_selector_contains(selector, attrib, string):
    selector_found = False
    for item in dom().cssselect(selector):
        assert_regexp_matches(item.attrib[attrib], re.compile('.*' + string + '.*'))
        selector_found = True
    assert_true(selector_found, 'No elements found for ' + selector)


def assert_selector_contains(selector, attrib, string):
    assert_regexp_matches(
        dom().cssselect(selector)[0].attrib[attrib],
        re.compile(".*" + string + ".*"),
    )


def assert_text_exists_in_first_element(id, error_text):
    first_element = world.browser.find_element_by_id(id[1:])
    assert_true(len(first_element.text) > 0, error_text)


def change_viewport_xs():
    world.browser.set_window_size(640, 1080)


def change_viewport_sm():
    world.browser.set_window_size(800, 600)


def change_viewport_md():
    world.browser.set_window_size(1024, 768)


def change_viewport_lg():
    world.browser.set_window_size(1920, 1080)

def wait_for_element_with_id_to_be_displayed(id):
    WebDriverWait(world.browser, 10).until(lambda s: s.find_element_by_id(id).is_displayed())

def wait_for_element_with_css_selector_to_be_displayed(css_selector):
    WebDriverWait(world.browser, 10).until(lambda s: s.find_element_by_css_selector(css_selector).is_displayed())

def wait_for_element_with_class_to_be_displayed(class_name):
    WebDriverWait(world.browser, 10).until(lambda s: s.find_element_by_class_name(class_name).is_displayed())

def assert_page_exist(url):
    c = Client()
    response = c.get(url, follow=True)
    assert_not_equals(response.status_code, 404)

def sign_in(email, password):
    login_menu = world.browser.find_element_by_id("lg-menuLogin")
    login_menu.find_element_by_link_text("SIGN IN").click()
    login_menu.find_element_by_name("username").send_keys(email)
    login_menu.find_element_by_name("password").send_keys(password)
    login_menu.find_element_by_name("submit").click()
    wait_for_ajax_to_complete()

def scroll_to_element(element):
    world.browser.execute_script("arguments[0].scrollIntoView(true);", element)




