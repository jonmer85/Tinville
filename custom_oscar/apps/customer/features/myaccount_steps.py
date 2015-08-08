from common.lettuce_utils import *
from lettuce import step
import lettuce.django

@step("I have some basic order data")
def i_have_some_basic_dashboar_data(step):
    setup_basic_order_data()


@step("I click the user Icon")
def i_click_the_user_Icon(step):
    user_icon = wait_for_element_with_css_selector_to_be_clickable("i[id^='clickedLogin-lg']")
    user_icon.click()

@step("I should see the 'My Account' page")
def i_see_the_my_account_page(step):
    wait_for_browser_to_have_url(get_server().url('/accounts/orders/'))
    wait_for_element_with_css_selector_to_be_displayed('div.slidingContent2 > div:nth-child(1) > h1')
    assert_selector_contains_text('div.slidingContent2 > div:nth-child(1) > h1', 'My Account')

@step("the selected tab should be '(.*)'")
def should_be_on_selected_tab(step, tab):
    wait_for_element_with_css_selector_to_be_displayed('.active > a:nth-child(1)')
    assert_selector_contains_text('.active > a:nth-child(1)', tab)

@step("I should see 3 top level orders")
def should_be_on_selected_tab(step):
    wait_for_element_with_link_text_to_be_clickable('10002')
    wait_for_element_with_link_text_to_be_clickable('10003')
    wait_for_element_with_link_text_to_be_clickable('10004')
    assert_element_with_link_text_does_not_exist('1-10002')
    assert_element_with_link_text_does_not_exist('1-10003')
    assert_element_with_link_text_does_not_exist('1-10004')


@step("I should see the '(.*)' link")
def i_should_see_the_link(step, linktext):
    wait_for_element_with_partial_link_text_to_be_displayed(linktext)

@step("I click on 'My Account'")
def i_click_on_link(step):
    dashboardlink = wait_for_element_with_partial_link_text_to_be_displayed("My Account")
    dashboardlink.click()


@step("I should see the Dashboard '(.*)' page")
def i_should_see_the_dashboard_page(step, page):
    assert_selector_does_exist(".dashboard")
    assert_selector_contains_text("h1", page)