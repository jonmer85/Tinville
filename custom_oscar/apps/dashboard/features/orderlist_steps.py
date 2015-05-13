from common.lettuce_utils import *
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
import lettuce.django

@step("I am on the dashboard index page")
def i_am_on_the_dashboard_index_page(step):
    world.browser.get(lettuce.django.get_server().url('/dashboard'))


@step("I click on the 'orders' link")
def i_click_on_the_link(step):
    clickme = step.scenario.context["LinkToClick"]
    clickme.click()


@step("I am on the dashboard order list page")
def i_am_on_the_dashboard_order_list_page(step):
    world.browser.get(lettuce.django.get_server().url('/dashboard/orders'))


@step("I click on the '(.*)' filter")
def i_click_on_the_filter(step, filter):
    assert_equals(1, len(world.browser.find_elements_by_xpath("//label[normalize-space(.)='" + filter + "']")), "Could not find the " + filter + " button")
    filterbtn = world.browser.find_element_by_xpath("//label[normalize-space(.)='" + filter + "']")
    filterbtn.click()


@step("I should see '(.*)' orders")
def i_should_see_x_orders(step, orders):
    ordercount = len(filter(lambda a: a.is_displayed(), world.browser.find_elements_by_css_selector("tr[id^='ordernumber_']")))
    assert_equals(int(orders), ordercount, "Should be " + orders + " visible orders, but was " + str(ordercount))


@step("I should see the following columns")
def i_should_see_the_following_columns(step):
    for column in step.hashes:
        thecolumn = str(column["Column"]).replace('"', '')
        assert_equals(1, len(world.browser.find_elements_by_xpath("//th/a[normalize-space(.)='" + thecolumn + "']")) +
                      len(world.browser.find_elements_by_xpath("//th[normalize-space(.)='" + thecolumn + "']")), thecolumn + " column does not exist")


@step("I should see '(.*)' order with a '(.*)' button")
def i_should_see_x_orders_with_a_x_button(step):
    """
    :type step lettuce.core.Step
    """
    pass


@step("I search for order '(.*)'")
def i_search_for_order_x(step):
    """
    :type step lettuce.core.Step
    """
    pass