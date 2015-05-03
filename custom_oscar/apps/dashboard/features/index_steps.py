from common.factories import create_order, create_product, create_basket_with_products, create_basket
from common.lettuce_utils import *
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
import lettuce.django
from django.contrib.auth.models import Permission
from user.models import TinvilleUser as User
from selenium.webdriver import *

@step("I am on the dashboard index page")
def i_am_on_the_dashboard_index_page(step):
    # TODO Create two orders
    # TODO Create two baskets with order for Demo user
    # TODO Behave as until user it as dashboard Accessing the dashboard test...
        # Resetting user permissions for default user...
    user = User.objects.get(pk=2)
    dashboard_access_perm = Permission.objects.get(
                codename='dashboard_access', content_type__app_label='partner')
    user.user_permissions.add(dashboard_access_perm)
    user.save()

    world.browser.get(lettuce.django.get_server().url('/'))
    sign_in("demo@user.com", "tinville")
    world.browser.get(lettuce.django.get_server().url('/dashboard'))


@step("I should see the '(.*)' table")
def i_should_see_the_table(step, tabletitle):
    tableheaders = len(world.browser.find_elements_by_xpath("//table/caption[contains(text(), '" + tabletitle + "')]")) \
                    + len(world.browser.find_elements_by_xpath("//div[contains(@class, 'table-header') and normalize-space(.)='" + tabletitle + "']"))

    assert_equals(1, tableheaders, "Should be 1 " + tabletitle + " table but there was " + str(tableheaders))

    try:
        table = world.browser.find_element_by_xpath("//div[contains(@class, 'table-header') and normalize-space(.)='" + tabletitle + "']/following-sibling::div[1]")
        type = "label"
    except NoSuchElementException:
        pass

    try:
        table = world.browser.find_element_by_xpath("//table/caption[contains(text(), '" + tabletitle + "')]").find_element_by_xpath("..")
        type = "tr"
    except NoSuchElementException:
        pass

    step.scenario.context["table"] = table
    step.scenario.context["type"] = type

@step("I should see my '(.*)'")
def i_should_see_my_section(step, section):
    table = step.scenario.context["table"]
    assert_equals(1, len(filter(lambda e: e.text == section, table.find_elements_by_css_selector(step.scenario.context["type"]))),
                  "No element with the text " + section + " exists in the table")