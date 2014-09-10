import os
import time

from common.lettuce_utils import *
from selenium.webdriver.support.ui import Select

from Tinville.settings.base import MEDIA_ROOT


@step(u'When the add item tab is selected')
def when_the_add_item_tab_is_selected(step):
    maximize_shop_editor()
    world.browser.find_element_by_css_selector('#optionContent>li>a[href="#addOrEditItem"]').click()
    assert world.browser.find_element_by_css_selector('#optionContent>.active>a[href="#addOrEditItem"]')

@step(u'Then the add item form is displayed')
def then_the_add_item_form_is_displayed(step):
    maximize_shop_editor()
    wait_for_element_with_css_selector_to_be_displayed('#addOrEditItem.tab-pane.active')
    wait_for_element_with_css_selector_to_be_displayed("#id_title")

@step(u'And I fill in the general add item fields')
def and_i_fill_in_the_general_add_item_fields(step):
    world.browser.maximize_window()  # Shop Editor features don't work well with automation unless maximized Jon M TBD
    for itemfields in step.hashes:
        world.browser.find_element_by_name("title").send_keys(itemfields["Title"])
        # TinyMCE uses iframes so need to use their javascript API to set the content
        world.browser.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(itemfields["Description"]))
        wait_for_element_with_name_to_be_displayed("price")
        world.browser.find_element_by_name("price").send_keys(itemfields["Price"])
        world.browser.find_element_by_name("category").send_keys(itemfields["Category"])
        file = os.path.join(MEDIA_ROOT, itemfields["Image1"])
        world.browser.find_element_by_name("product_image").send_keys(file)
        sizeVariationElement = world.browser.find_element_by_name('sizeVariation')
        scroll_to_element(sizeVariationElement)
        Select(sizeVariationElement).select_by_value(itemfields['SizeVariation'])

@step(u'I choose the size (.*) with row number (\d+) and I fill the following quantities and colors')
def i_choose_the_size_and_fill_colors_and_quantities(step, size_set, row_number):
    row_number = unicode(int(row_number) - 1)  # 0-bias it for indexing
    sizeSetPrefix = "sizeSetSelectionTemplate{0}_id_".format(row_number)
    Select(world.browser.find_element_by_id(sizeSetPrefix + "sizeSetSelection")).select_by_visible_text(size_set)
    for (counter, colorQuantity) in enumerate(step.hashes):
        Select(wait_for_element_with_id_to_be_clickable(sizeSetPrefix + "colorSelection" + unicode(counter))).select_by_visible_text(colorQuantity["Color"])
        wait_for_element_with_id_to_be_clickable(sizeSetPrefix + "quantityField" + unicode(counter)).send_keys(colorQuantity["Quantity"])

@step(u'I should see a confirmation message stating that the item was (.*)')
def i_should_see_a_confirmation_message_stating_that_the_item_was_created_or_updated(step, createdOrUpdated):
    assert_id_exists("messagesModal")
    assert_selector_contains_text("#messagesModal .alert-success", "Item has been successfully {0}!".format(createdOrUpdated))
    wait_for_element_with_css_selector_to_be_clickable("#messagesModal .close").click()
    wait_for_element_with_id_to_not_be_displayed("messagesModal")

@step(u'And I submit this item')
def and_i_submit_this_item(step):
    element = world.browser.find_element_by_name("productCreationForm")
    scroll_to_element(element)
    element.click()

@step(u'Then I should see (\d+) product(?s) total')
def i_should_see_n_products_total(step, total):
    minimize_shop_editor()
    products = world.browser.find_elements_by_css_selector(".shopItem")
    assert len(products) == int(total)
    
    
@step(u'When I click the delete button for the product')
def when_I_click_delete_button_product(step):
    world.browser.find_element_by_css_selector("#minMaxIcon").click()
    wait_for_element_with_link_text_to_be_displayed("Delete")
    world.browser.find_element_by_link_text("Delete").click()

@step(u'And I click ok on the confirmation')
def and_I_click_ok_confirmation(step):
    world.browser.find_element_by_css_selector("#okDeleteBtn").click()

@step(u'Then the product is removed')
def then_product_is_removed(step):
    try:
        world.browser.find_element_by_css_selector("a[href='/Demo/edit/delete_product/TestSizeSetItem']")
    except NoSuchElementException:
        return True
    return False

@step(u'And the shop editor refreshes in a minimized state')
def and_shopEditor_refreshes_minimized(step):
    assert world.browser.find_element_by_css_selector("#minMaxIcon.glyphicon-chevron-up").is_displayed() == True, "Because chevron should be facing up"
    assert len(world.browser.find_elements_by_css_selector("#editorPanels.collapse")) == 1, "Because the editor panel should be collapsed"


# Utilities
def minimize_shop_editor():
    if css_selector_exists("#minMaxIcon.glyphicon-chevron-down"):
        wait_for_element_with_id_to_be_clickable("minMaxIcon").click()
        time.sleep(1)
        wait_for_element_with_css_selector_to_be_displayed("#minMaxIcon.glyphicon-chevron-up")

def maximize_shop_editor():
    if css_selector_exists("#minMaxIcon.glyphicon-chevron-up"):
        wait_for_element_with_id_to_be_clickable("minMaxIcon").click()
        time.sleep(1)
        wait_for_element_with_css_selector_to_be_displayed("#minMaxIcon.glyphicon-chevron-down")
