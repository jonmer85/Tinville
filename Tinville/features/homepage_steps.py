from common.lettuce_extensions import get_server
from common.lettuce_utils import *
import cssselect
from lettuce import step
from nose.tools import assert_equals, assert_not_equals, assert_raises
from user.models import TinvilleUser
import lettuce.django
from selenium.common.exceptions import *


@step(u'Goto Demo page first')
def goto_Demo_page_first(step):
    world.browser.get(get_server().url('/Demo'))

@step(u'When I click the Tinville Tag')
def When_I_click_the_Tinville_Tag(step):
    change_viewport_lg()
    wait_for_element_with_css_selector_to_be_clickable("#tinvilletagId").click()

@step(u'Then I should be redirected to the home page')
def then_i_should_be_redirected_to_the_home_page(step):
    go_home_page()
