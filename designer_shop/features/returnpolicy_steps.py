# -*- coding: utf-8 -*-
from django.conf import settings
import os
import time

from django.core.management import call_command
from common.lettuce_utils import *


@step(u'the return policy edit button is pressed')
def when_the_return_policy_button_is_selected(step):
    wait_for_element_with_css_selector_to_be_clickable('#returnPolicyTabAnchor').click()
    wait_for_element_with_css_selector_to_be_clickable('button.returnPolicyEditButton').click()

@step(u'Then the return policy text field box is displayed')
def then_the_return_policy_text_field_box_is_displayed(step):
    assert world.browser.find_element_by_id('returnPolicy')
    assert_id_exists('returnPolicy')

@step(u'And the submit return policy button is displayed')
def and_the_submit_return_policy_button_is_displayed(step):
    assert_id_exists('id_SubmitReturnPolicy')

@step(u'And the return policy is submitted')
def and_the_about_content_is_submitted(step):
    wait_for_element_with_id_to_be_clickable('id_returnPolicy_ifr').click()
    world.browser.execute_script("tinyMCE.activeEditor.setContent('<p>Test Return Policy Content</p>')")
    wait_for_javascript_to_complete()

    wait_for_element_with_id_to_exist("returnPolicyModalFooterSubmit")
    wait_for_element_with_id_to_be_clickable("returnPolicyModalFooterSubmit").click()
    wait_for_ajax_to_complete()

@step(u'The return policy is saved')
def the_about_content_is_saved(step):
    world.browser.maximize_window()
    wait_for_element_with_css_selector_to_be_clickable('#returnPolicyTabAnchor')
    wait_for_element_with_css_selector_to_be_clickable('#returnPolicyTabAnchor').click()
    returnPolicyLocation = wait_for_element_with_css_selector_to_be_displayed('.returnPolicyContent>p')
    assert returnPolicyLocation.text == "Test Return Policy Content"