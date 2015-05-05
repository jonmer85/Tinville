from common.lettuce_utils import *
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
import lettuce.django
from designer_shop.models import Shop


@step("I am on the dashboard index page")
def i_am_on_the_dashboard_index_page(step):
    world.browser.get(lettuce.django.get_server().url('/'))
    world.browser.get(lettuce.django.get_server().url('/dashboard'))


@step("I should see the '(.*)' table")
def i_should_see_the_table(step, tabletitle):
    tableheaders = len(world.browser.find_elements_by_xpath("//table/caption[normalize-space(.)='" + tabletitle + "']")) \
                    + len(world.browser.find_elements_by_xpath("//div[contains(@class, 'table-header') and normalize-space(.)='" + tabletitle + "']"))
    assert_equals(1, tableheaders, "Should be 1 " + tabletitle + " table but there was " + str(tableheaders))
    try:
        table = world.browser.find_element_by_xpath("//div[contains(@class, 'table-header') and normalize-space(.)='" + tabletitle + "']/following-sibling::div[1]")
        type = "label"
    except NoSuchElementException:
        pass

    try:
        table = world.browser.find_element_by_xpath("//table/caption[normalize-space(.)='" + tabletitle + "']").find_element_by_xpath("..")
        type = "tr"
    except NoSuchElementException:
        pass

    step.scenario.context["table"] = table
    step.scenario.context["type"] = type


@step("I should see my '(.*)'")
def i_should_see_my_section(step, section):
    table = step.scenario.context["table"]
    assert_equals(1, len(filter(lambda e: section in e.text, table.find_elements_by_css_selector(step.scenario.context["type"]))),
                  "No element with the text " + section + " exists in the table")