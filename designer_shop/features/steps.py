# -*- coding: utf-8 -*-
from designer_shop.models import Shop
from user.models import TinvilleUser
from common.lettuce_utils import *
from lettuce import step
from django.core.management import call_command
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

@step(u'Given a shop editor')
def give_a_shop_editor(step):
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

@step(u'And selecting the double inward arrows should demcrease the size of the shop editor to 35% of window size again')
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
