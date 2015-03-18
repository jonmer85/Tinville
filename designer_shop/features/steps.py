# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management import call_command
import lettuce.django
import math
import time
import os


from Tinville.settings.base import MEDIA_ROOT
from designer_shop.models import Shop
from user.models import TinvilleUser
from selenium.webdriver.support.ui import Select
from common.lettuce_utils import *

@before.each_scenario
def load_all_fixtures(scenario):
    call_command('loaddata', 'all.json')


@step(u'And (\d+) shop items')
def and_n_shop_items(step, n):
    for i in range(int(n)):
        world.shop.item_set.create(name='itemname', image='itemimage', price='3.42')

@step(u'Then the banner for the shop is displayed')
def then_the_banner_for_the_shop_is_displayed(step):
    assert_selector_contains('#id_BannerImage', 'src', 'bar')

@step(u'And the items for the shop are displayed')
def and_the_items_for_the_shop_are_displayed(step):
    assert_class_exists('shopItems')

@step(u'And the Tinville header is displayed')
def and_the_tinville_header_is_displayed(step):
    assert_class_exists('navbar')

@step(u'Then there should be (\d+) items displayed')
def then_there_should_be_n_items_displayed(step, n):
    assert_number_of_selectors('.shopItems .shopItem', int(n))

@step(u'And every item should have a name')
def and_every_item_should_have_a_name(step):
    assert_text_of_every_selector('.shopItems .shopItem .name', 'itemname')

@step(u'And every item should have an image')
def and_every_item_should_have_an_image(step):
    assert_every_selector_contains('.shopItems .shopItem img', 'src', 'itemimage')

@step(u'And every item should have a price')
def and_every_item_should_have_a_price(step):
    assert_text_of_every_selector('.shopItems .shopItem .price', '$3.42')

@step(u'Given the demo shop$')
def given_the_demo_shop(step):
    world.browser.get(lettuce.django.get_server().url('/Demo'))
    wait_for_browser_to_have_url(lettuce.django.get_server().url('/access_code?shop=Demo'))
    user = TinvilleUser.objects.get(email="demo@user.com")
    form = fill_in_access_form(access_code=user.access_code)
    form.submit()
    # wait_for_browser_to_have_url(world.browser.get(lettuce.django.get_server().url('/Demo')))

@step(u'Given a shop editor')
def given_a_shop_editor(step):
    assert_id_exists('shopEditor')

@step(u'Then the designer can open a shop editor')
def the_designer_can_open_a_shop_editor(step):
    sign_in('Demo@user.com', 'tinville')
    world.browser.get(lettuce.django.get_server().url('/Demo/edit'))
    assert_id_exists('shopEditor')

@step(u'Then there should be 1 icon displayed for control')
def there_should_be_1_icon_displays_for_control(step):
    assert_id_exists('shopEditorTitle')
    assert world.browser.find_element_by_css_selector('#minMaxIcon.glyphicon-chevron-down')

@step(u'And a panel for options')
def and_a_panel_for_options(step):
    assert_id_exists('optionPanel')
    assert_id_exists('optionContent')

@step(u'And a panel with the panel')
def and_a_panel_with_the_panel(step):
    assert_id_exists('formPanel')
    assert_id_exists('formContent')

@step(u'And a global submit button')
def and_a_global_submit_button(step):
    assert world.browser.find_element_by_css_selector('button.tinvilleButton.pull-right')

@step(u'And the shop editor is 85% of the window size by default')
def and_the_shop_editor_is_85(step):
    time.sleep(1)
    shopeditorheight = world.browser.find_element_by_css_selector('body').size['height']
    assert math.fabs(world.browser.find_element_by_css_selector('#shopEditorWindow').size['height'] - int(shopeditorheight*.85)) <= 1

@step(u'Given the demo shop editor')
def given_demo_shop_editor(step):
    # time.sleep(1)
    world.browser.get(lettuce.django.get_server().url('/'))
    sign_in("demo@user.com", "tinville")

    world.browser.get(lettuce.django.get_server().url('/Demo/edit'))
    wait_for_element_with_css_selector_to_exist('.bannerUploadEditButton')
    wait_for_element_with_class_to_be_displayed('colorPickerEditButton')
    wait_for_element_with_class_to_be_displayed('addItem')

@step(u'Then there should be 1 icon displayed for size control')
def there_should_be_one_icon_for_size_control(step):
    assert_id_exists('shopEditorTitle')
    assert world.browser.find_element_by_css_selector('#minMaxIcon.glyphicon-chevron-down')

@step(u'Then selecting the down arrow should minimize the shop editor')
def then_selecting_the_down_arrow_should_minimize_the_shop_editor(step):
    world.browser.find_element_by_css_selector('#minMaxIcon.glyphicon-chevron-down').click()
    time.sleep(0.4)
    assert world.browser.find_element_by_css_selector('#minMaxIcon.glyphicon-chevron-up')
    assert world.browser.find_element_by_css_selector('#formPanel').size['height'] == 0
    assert world.browser.find_element_by_css_selector('#optionPanel').size['height'] == 0

@step(u'And selecting the up arrow should expand the shop editor again')
def and_selecting_the_up_arrow_should_expand_the_shop_editor_again(step):
    assert world.browser.find_element_by_css_selector('#minMaxIcon.glyphicon-chevron-up')
    world.browser.find_element_by_css_selector('#minMaxIcon.glyphicon-chevron-up').click()
    time.sleep(0.4)
    shopeditorheight = world.browser.find_element_by_css_selector('body').size['height']
    assert math.fabs(world.browser.find_element_by_css_selector('#shopEditorWindow').size['height'] - int(shopeditorheight*.8)) <= 1



@step(u'When the logo tab is selected')
def when_the_logo_tab_is_selected(step):
    wait_for_element_with_css_selector_to_be_clickable('#optionContent>li>a[href="#logo"]').click()
    wait_for_element_with_css_selector_to_be_displayed('#optionContent>.active>a[href="#logo"]')

@step(u'Then the logo file upload is displayed')
def then_the_logo_file_upload_is_displayed(step):
    wait_for_element_with_css_selector_to_be_displayed('#logo.tab-pane.active')
    assert_id_exists('id_logo')

@step(u'And the submit Logo button is displayed')
def and_the_submit_logo_button_is_displayed(step):
    assert_id_exists('id_SubmitLogo')

@step(u'And a logo is submitted')
def and_a_logo_is_submitted(step):
    logo_uploader = world.browser.find_element_by_id("id_logo")
    logo_uploader.send_keys(os.path.join(MEDIA_ROOT, "images/logo.jpg"))
    wait_for_element_with_id_to_be_displayed("id_SubmitLogo")
    world.browser.find_element_by_id("id_SubmitLogo").click()

@step(u'The selected logo file is saved')
def the_selected_logo_file_is_saved(step):
    assert_selector_contains('#id_LogoImage', 'src', '/media/shops/demo/logo/logo.jpg')


@step(u'(?:When|And) I sign in')
def and_i_sign_in(step):
    sign_in('demo@user.com', 'tinville')


@step(u'When the home tab is selected')
def when_the_home_tab_is_selected(step):
    wait_for_element_with_css_selector_to_be_clickable('#shopTabButton').click()
    wait_for_element_with_css_selector_to_be_displayed('.active>#shopTabButton')

@step(u'Then the home content is displayed')
def then_the_home_content_is_displayed(step):
    assert world.browser.find_element_by_id('shopTab')
    assert_id_exists('shopTab')


@step(u'Then the about content is displayed')
def then_the_home_content_is_displayed(step):
    assert world.browser.find_element_by_id('aboutTab')
    assert_id_exists('aboutTab')

@step(u'When the landing tab is selected')
def when_the_landing_tab_is_selected(step):
    wait_for_element_with_css_selector_to_be_clickable('#landingTabButton').click()
    wait_for_element_with_css_selector_to_be_displayed('.active>#landingTabButton')

@step(u'Then the landing content is displayed')
def then_the_home_content_is_displayed(step):
    assert world.browser.find_element_by_id('landingTab')
    assert_id_exists('landingTab')
