# -*- coding: utf-8 -*-
from designer_shop.models import Shop
from user.models import TinvilleUser
from common.lettuce_utils import *
from lettuce import step
from django.core.management import call_command
from selenium import webdriver
import lettuce.django
import time
import math

@before.each_scenario
def load_all_fixtures(scenario):
    call_command('loaddata', 'all.json')

@step(u'Given a designer shop')
def given_a_designer_shop(step):
    world.user = TinvilleUser.objects.create(email="foo@bar.com")
    world.shop = Shop.objects.create(user=world.user, name='foo', banner='bar', logo='baz')

@step(u'And (\d+) shop items')
def and_n_shop_items(step, n):
    for i in range(int(n)):
        world.shop.item_set.create(name='itemname', image='itemimage', price='3.42')

@step(u'When the shop is visited')
def when_the_shop_is_visited(step):
    world.browser.get(lettuce.django.get_server().url(world.shop.get_absolute_url()))

@step(u'Then the banner for the shop is displayed')
def then_the_banner_for_the_shop_is_displayed(step):
    assert_selector_contains('img.shopBanner', 'src', 'bar')

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

@step(u'Given the demo shop')
def given_the_demo_shop(step):
    world.browser.get(lettuce.django.get_server().url('/Demo'))

@step(u'The designer can open a shop editor')
def the_designer_can_open_a_shop_editor(step):
    world.browser.get(lettuce.django.get_server().url('/Demo/edit'))
    assert_id_exists('shopEditor')

@step(u'There should be 2 icons displayed for control')
def there_should_be_2_icons_displays_for_control(step):
    assert_id_exists('shopEditorTitle')
    assert world.browser.find_element_by_css_selector('#minMaxIcon.glyphicon-chevron-down')
    assert world.browser.find_element_by_css_selector('#resizeIcon.glyphicon-resize-full')

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

@step(u'And the shop editor is 35% of the window size by default')
def and_the_shop_editor_is_35(step):
    time.sleep(1)
    shopeditorheight = world.browser.find_element_by_css_selector('body').size['height']
    assert math.fabs(world.browser.find_element_by_css_selector('#shopEditorWindow').size['height'] - int(shopeditorheight*.35)) <= 1

@step(u'Given the demo shop editor')
def give_demo_shop_editor(step):
    world.browser.get(lettuce.django.get_server().url('/Demo/edit'))
    assert_id_exists('shopEditor')

@step(u'There should be 2 icons displayed for size control')
def there_should_be_two_icons_for_size_control(step):
    assert_id_exists('shopEditorTitle')
    assert world.browser.find_element_by_css_selector('#minMaxIcon.glyphicon-chevron-down')
    assert world.browser.find_element_by_css_selector('#resizeIcon.glyphicon-resize-full')

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
    assert math.fabs(world.browser.find_element_by_css_selector('#shopEditorWindow').size['height'] - int(shopeditorheight*.35)) <= 1

@step(u'And selecting the double arrows should increase the size of the shop editor to 75% of window size')
def and_selecting_the_double_arrows_should_increase_the_size_of_the_shop_editor_to_seventyfive_of_window_size(step):
    assert world.browser.find_element_by_css_selector('#resizeIcon.glyphicon-resize-full')
    world.browser.find_element_by_css_selector("#resizeIcon.glyphicon-resize-full").click()
    time.sleep(0.4)
    shopeditorheight = world.browser.find_element_by_css_selector('body').size['height']
    assert math.fabs(world.browser.find_element_by_css_selector('#shopEditorWindow').size['height'] == int(shopeditorheight*.75)) <= 1

@step(u'And selecting the double inward arrows should decrease the size of the shop editor to 35% of window size again')
def and_selecting_the_double_inward_arrows_should_decrease_the_size_to_thirtyfive_of_window_size(step):
    assert world.browser.find_element_by_css_selector('#resizeIcon.glyphicon-resize-small')
    world.browser.find_element_by_css_selector("#resizeIcon.glyphicon-resize-small").click()
    time.sleep(0.4)
    shopeditorheight = world.browser.find_element_by_css_selector('body').size['height']
    assert math.fabs(world.browser.find_element_by_css_selector('#shopEditorWindow').size['height'] == int(shopeditorheight*.35)) <= 1


@step(u'When the color tab is selected')
def when_the_color_tab_is_selected(step):
    world.browser.find_element_by_css_selector('#optionContent>li>a[href="#color"]').click()
    time.sleep(0.4)
    assert world.browser.find_element_by_css_selector('#optionContent>.active>a[href="#color"]')

@step(u'Then the color picker wheel is displayed')
def then_the_color_picker_wheel_is_displayed(step):
    assert world.browser.find_element_by_css_selector('#color.tab-pane.active')
    assert_id_exists('id_color-colorpicker')

@step(u'And the color picker textbox is displayed')
def and_the_color_picker_textbox_is_displayed(step):
    assert_id_exists('id_color')

@step(u'And the Create button is displayed')
def and_the_create_button_is_displayed(step):
    assert_id_exists('shopColorPicker')

@step(u'And a color is submitted')
def and_a_color_is_submitted(step):
    color_picker = world.browser.find_element_by_id("color")
    world.browser.find_element_by_id("id_color").clear()
    color_picker.find_element_by_name("color").send_keys("#fb1c0e")
    world.browser.find_element_by_id("resizeIcon").click()
    wait_for_element_with_id_to_be_displayed("shopColorPicker")
    world.browser.find_element_by_id("shopColorPicker").click()
    wait_for_ajax_to_complete()

@step(u'The selected color is applied to the components of the shop')
def the_selected_color_is_applied_to_the_components_of_the_shop(step):
    color_element = world.browser.find_element_by_css_selector('.shopBackgroundColor')
    style = color_element.get_attribute("style")
    assert style == 'background-color: rgb(251, 28, 14);'

@step(u'When the logo tab is selected')
def when_the_logo_tab_is_selected(step):
    world.browser.find_element_by_css_selector('#optionContent>li>a[href="#logo"]').click()
    time.sleep(0.4)
    assert world.browser.find_element_by_css_selector('#optionContent>.active>a[href="#logo"]')

@step(u'Then the logo file upload is displayed')
def then_the_logo_file_upload_is_displayed(step):
    assert world.browser.find_element_by_css_selector('#logo.tab-pane.active')
    assert_id_exists('id_logo')

@step(u'And the submit Logo button is displayed')
def and_the_submit_logo_button_is_displayed(step):
    assert_id_exists('id_SubmitLogo')

@step(u'And a logo is submitted')
def and_a_logo_is_submitted(step):
    logo_uploader = world.browser.find_element_by_id("id_logo")
    logo_uploader.send_keys('/images/logo2.jpg')
    wait_for_element_with_id_to_be_displayed("id_SubmitLogo")
    world.browser.find_element_by_id("id_SubmitLogo").click()

@step(u'The selected logo file is saved')
def the_selected_logo_file_is_saved(step):
    assert_selector_contains('#id_LogoImage', 'src', '/media/shops/demo/banner/logo2.jpg')

@step(u'When the banner tab is selected')
def when_the_banner_tab_is_selected(step):
    world.browser.find_element_by_css_selector('#optionContent>li>a[href="#banner"]').click()
    time.sleep(0.4)
    assert world.browser.find_element_by_css_selector('#optionContent>.active>a[href="#banner"]')

@step(u'Then the banner file upload is displayed')
def then_the_banner_file_upload_is_displayed(step):
    assert world.browser.find_element_by_css_selector('#banner.tab-pane.active')
    assert_id_exists('id_banner')

@step(u'And the submit Banner button is displayed')
def and_the_submit_banner_button_is_displayed(step):
    assert_id_exists('id_SubmitBanner')

@step(u'And a banner is submitted')
def and_a_banner_is_submitted(step):
    bannerUploader = world.browser.find_element_by_id("id_banner")
    bannerUploader.send_keys('/images/banner2.jpg')
    wait_for_element_with_id_to_be_displayed("id_SubmitBanner")
    world.browser.find_element_by_id("id_SubmitBanner").click()

@step(u'The selected banner file is saved')
def the_selected_banner_file_is_saved(step):
    assert_selector_contains('#id_BannerImage', 'src', '/media/shops/demo/banner/banner2.jpg')

@step(u'When the about tab is selected')
def when_the_about_tab_is_selected(step):
    world.browser.find_element_by_css_selector('#optionContent>li>a[href="#about"]').click()
    time.sleep(0.4)
    assert world.browser.find_element_by_css_selector('#optionContent>.active>a[href="#about"]')

@step(u'Then the about text field box is displayed')
def then_the_about_text_field_box_is_displayed(step):
    assert world.browser.find_element_by_id('about')
    assert_id_exists('about')

@step(u'And the submit about content button is displayed')
def and_the_submit_about_content_button_is_displayed(step):
    assert_id_exists('id_SubmitAboutContent')

@step(u'And the about content is submitted')
def and_the_about_content_is_submitted(step):
    aboutContent = world.browser.find_element_by_id('id_aboutContent')
    aboutContent.send_keys("We are doing Lettuce Tests")
    world.browser.find_element_by_id("id_SubmitAboutContent").click()
    wait_for_ajax_to_complete()

@step(u'The about content is saved')
def the_about_content_is_saved(step):
    aboutLocation = world.browser.find_element_by_id("aboutLocation")
    aboutLocation.getAttribute("innerHTML")

@step(u'When the add item tab is selected')
def when_the_add_item_tab_is_selected(step):
    world.browser.find_element_by_css_selector('#optionContent>li>a[href="#addItems"]').click()
    wait_for_element_with_id_to_be_displayed("shopColorPicker")
    assert world.browser.find_element_by_css_selector('#optionContent>.active>a[href="#addItems"]')

@step(u'Then the add item form is displayed')
def then_the_add_item_form_is_displayed(step):
    assert world.browser.find_element_by_css_selector('#addItems.tab-pane.active')
    assert_id_exists('id_title')