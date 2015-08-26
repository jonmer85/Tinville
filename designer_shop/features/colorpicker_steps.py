from time import sleep
from common.lettuce_utils import *

@step(u'And the color picker textbox is displayed')
def and_the_color_picker_textbox_is_displayed(step):
    assert_class_exists('farbtasticcolorpicker')

@step(u'the color picker button is pressed')
def when_the_color_button_is_selected(step):
    wait_for_element_with_css_selector_to_be_displayed('.shopBackgroundColor')
    sleep(1)
    wait_for_element_with_css_selector_to_be_clickable('.hidden-xs .colorPickerEditButton').click()

@step(u'Then the color picker wheel is displayed')
def then_the_color_picker_wheel_is_displayed(step):
    wait_for_element_with_id_to_be_displayed('id_color-colorpicker')

@step(u'And the Create button is displayed')
def and_the_create_button_is_displayed(step):
    wait_for_element_with_id_to_be_clickable('colorModalFooterSubmit')

@step(u'And a color is submitted "([^"]*)"')
def and_a_color_is_submitted(step,color):
    color_picker = wait_for_element_with_id_to_be_displayed("color")
    wait_for_element_with_id_to_be_displayed("id_color").clear()
    color_picker.find_element_by_name("color").send_keys(color)
    wait_for_element_with_id_to_be_clickable("colorModalFooterSubmit").click()
    wait_for_ajax_to_complete()

@step(u'The selected color is applied to the components of the shop "([^"]*)"')
def the_selected_color_is_applied_to_the_components_of_the_shop(step, color):
    color_element = wait_for_element_with_css_selector_to_be_displayed('.shopBackgroundColor')
    style = color_element.get_attribute("style")
    bc = "background-color: " + str(color) + ";"
    assert style == bc

@step(u'And the text color of shop menu is applied "([^"]*)"')
def and_the_text_color_of_shop_menu(step, color):
    color_element = wait_for_element_with_css_selector_to_be_displayed('.shopTitleColor')
    style = color_element.get_attribute("style")
    assert style == "color: " + color + ";"

@step(u'And the tinville orange color f46430 is submitted')
def and_the_tinville_orange_color_f46430_is_submitted(step):
    color_picker = wait_for_element_with_id_to_be_displayed("color")
    wait_for_element_with_id_to_be_displayed("id_color").clear()
    color_picker.find_element_by_name("color").send_keys("#f46430")
    # world.browser.find_element_by_id("minMaxIcon").click()
    wait_for_element_with_id_to_be_displayed("colorModalFooterSubmit")
    wait_for_element_with_id_to_be_clickable("colorModalFooterSubmit").click()

@step(u'Then an exception Tinville Branding is not Allowed to be Used is thrown')
def then_an_exception_Tinville_Branding_is_not_Allowed_to_be_Used_is_thrown(step):
    wait_for_element_with_css_selector_to_exist("#div_id_color.has-error")
    assert_selector_contains_text("span strong", "Tinville Branding is not Allowed to be Used")