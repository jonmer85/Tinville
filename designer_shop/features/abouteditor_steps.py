# -*- coding: utf-8 -*-
from django.conf import settings
import os
import time

from django.core.management import call_command
from common.lettuce_utils import *

@before.each_scenario
def load_all_fixtures(scenario):
    call_command('loaddata', 'all.json')

@step(u'When the about tab is selected')
def when_the_about_tab_is_selected(step):
    maximize_shop_editor()
    wait_for_element_with_css_selector_to_be_clickable('#optionContent>li>a[href="#about"]').click()
    wait_for_element_with_css_selector_to_be_displayed('#optionContent>.active>a[href="#about"]')

@step(u'Then the about text field box is displayed')
def then_the_about_text_field_box_is_displayed(step):
    assert world.browser.find_element_by_id('about')
    assert_id_exists('about')

@step(u'And the submit about content button is displayed')
def and_the_submit_about_content_button_is_displayed(step):
    assert_id_exists('id_SubmitAboutContent')

@step(u'And the about content and image is submitted')
def and_the_about_content_is_submitted(step):
    wait_for_element_with_id_to_be_clickable('id_aboutContent_ifr').click()
    world.browser.execute_script("tinyMCE.activeEditor.setContent('<p>Test About Content</p>')")
    wait_for_javascript_to_complete()

    imgUploader = world.browser.find_element_by_id("id_aboutImg")
    imgUploader.send_keys(os.path.join(settings.MEDIA_ROOT, "images/aboutImage.png"))

    wait_for_element_with_id_to_exist("id_SubmitAboutContent")
    wait_for_element_with_id_to_be_clickable("id_SubmitAboutContent").click()
    wait_for_ajax_to_complete()

@step(u'The about content is saved')
def the_about_content_is_saved(step):
    world.browser.maximize_window()
    minimize_shop_editor()
    wait_for_element_with_css_selector_to_be_clickable('#aboutTabAnchor')
    wait_for_element_with_css_selector_to_be_clickable('#aboutTabAnchor').click()
    aboutLocation = wait_for_element_with_css_selector_to_be_displayed('.aboutContent>p')
    assert aboutLocation.text == "Test About Content"
    wait_for_element_with_id_to_be_displayed("displayedAboutImg")
    assert_every_selector_contains("#displayedAboutImg", "src", "about")