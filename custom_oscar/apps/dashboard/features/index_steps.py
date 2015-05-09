from common.lettuce_utils import *
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
import lettuce.django


@step("I am on the dashboard index page")
def i_am_on_the_dashboard_index_page(step):
    world.browser.get(lettuce.django.get_server().url('/dashboard'))


@step("I should see the '(.*)' table")
def i_should_see_the_table(step, tabletitle):
    tableheaders = len(world.browser.find_elements_by_xpath("//table/caption[normalize-space(.)='" + tabletitle + "']")) \
                   + len(world.browser.find_elements_by_xpath(
        "//div[contains(@class, 'table-header') and normalize-space(.)='" + tabletitle + "']"))
    assert_equals(1, tableheaders, "Should be 1 " + tabletitle + " table but there was " + str(tableheaders))
    try:
        table = world.browser.find_element_by_xpath(
            "//div[contains(@class, 'table-header') and normalize-space(.)='" + tabletitle + "']/following-sibling::div[1]")
        type = "label"
    except NoSuchElementException:
        pass

    try:
        table = world.browser.find_element_by_xpath(
            "//table/caption[normalize-space(.)='" + tabletitle + "']").find_element_by_xpath("..")
        type = "tr"
    except NoSuchElementException:
        pass

    step.scenario.context["table"] = table
    step.scenario.context["type"] = type


@step("I should see my '(.*)'")
def i_should_see_my_section(step, section):
    table = step.scenario.context["table"]
    assert_equals(1, len(
        filter(lambda e: section in e.text, table.find_elements_by_css_selector(step.scenario.context["type"]))),
                  "No element with the text " + section + " exists in the table")


@step("I click the user Icon")
def i_click_the_user_Icon(step):
    user_icon = wait_for_element_with_css_selector_to_be_clickable("i[id^='clickedLogin-lg']")
    user_icon.click()


@step("I should see the '(.*)' link")
def i_should_see_the_link(step, linktext):
    wait_for_element_with_partial_link_text_to_be_displayed(linktext)


@step("I click on 'Dashboard'")
def i_click_on_link(step):
    dashboardlink = wait_for_element_with_partial_link_text_to_be_displayed("Dashboard")
    dashboardlink.click()


@step("I should see the Dashboard page")
def i_should_see_the_dashboard_page(step):
    assert_selector_does_exist(".dashboard")
    assert_selector_contains_text("h1", "Dashboard")


@step("I should not see the Dashboard page")
def I_should_not_see_the_dashboard_page(step):
    assert_selector_does_not_exist(".dashboard")


@step("I go to the url '(.*)'")
def i_go_to_url(step, url):
    world.browser.get(lettuce.django.get_server().url(url))


@step("I am logged in as a non-designer customer")
def i_am_logged_in_as_a_non_designer_customer(step):
    world.browser.get(lettuce.django.get_server().url('/'))
    sign_in("democust@user.com", "tinville")


@step("I should see the Dashboard Menu")
def i_should_see_the_dashboard_menu(step):
    assert_id_exists("dashboardNav")


@step("I should see a '(.*)' dropdown with the following options")
def i_should_see_a_dropdown_with_options(step, linktext):
    link = wait_for_element_with_partial_link_text_to_be_displayed(linktext)
    link.click()
    for option in step.hashes:
        wait_for_element_with_partial_link_text_to_be_displayed(option["Options"])
