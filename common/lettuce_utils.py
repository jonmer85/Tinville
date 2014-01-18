from lettuce import *

from nose.tools import *

import re


def assert_selector_exists(selector):
    assert_greater(world.dom.cssselect(selector), 0)


def assert_selector_does_not_exist(selector):
    assert_equals(world.dom.cssselect(selector), [])


def assert_number_of_selectors(selector, n):
    assert_equals(len(world.dom.cssselect(selector)), n)


def assert_text_of_every_selector(selector, text):
    selector_found = False
    for item in world.dom.cssselect(selector):
        assert_equals(item.text, text)
        selector_found = True
    assert_true(selector_found, 'No elements found')


def assert_every_selector_contains(selector, attrib, string):
    selector_found = False
    for item in world.dom.cssselect(selector):
        assert_regexp_matches(item.attrib[attrib], re.compile('.*' + string + '.*'))
        selector_found = True
    assert_true(selector_found, 'No elements found')


def assert_selector_contains(selector, attrib, string):
    assert_regexp_matches(
        world.dom.cssselect(selector)[0].attrib[attrib],
        re.compile(".*" + string + ".*"),
    )
