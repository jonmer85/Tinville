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