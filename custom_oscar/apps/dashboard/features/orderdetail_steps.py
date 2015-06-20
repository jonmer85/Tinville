from common.lettuce_utils import *
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
import lettuce.django

@step("I click on order '(.*)'")
def I_click_on_order_x(step, order):
    world.browser.find_elements_by_xpath("//tr/td/a[contains(@href,'/dashboard/orders/" + order + "/')]")[1].click()

@step("I see order '(.*)' details")
def I_see_order_x_details(step, order):
    pageXPath = "//h1[normalize-space(.)='Order #" + order + "']"
    wait_for_element_with_xpath_to_exist(pageXPath)
    onPage = world.browser.find_elements_by_xpath(pageXPath)
    assert_equals(1, len(onPage), order + " page not shown")

@step("I can see the following order details")
def I_can_see_the_following_order_details(step):
    for items in step.hashes:
        for item in items:
            assert_equals(1, len(world.browser.find_elements_by_xpath("//th[normalize-space(.)='" + item + "']")), item + " column does not exist")