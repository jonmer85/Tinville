import os
import time

from common.lettuce_utils import *
from selenium.webdriver.support.ui import Select

from Tinville.settings.base import MEDIA_ROOT

@step(u'When the add item tab is selected')
def when_the_add_item_tab_is_selected(step):
    world.browser.find_element_by_css_selector('#optionContent>li>a[href="#addOrEditItem"]').click()
    assert world.browser.find_element_by_css_selector('#optionContent>.active>a[href="#addOrEditItem"]')

@step(u'Then the add item form is displayed')
def then_the_add_item_form_is_displayed(step):
    assert world.browser.find_element_by_css_selector('#addOrEditItem.tab-pane.active')
    assert world.browser.find_element_by_css_selector("#id_title").is_displayed()

@step(u'And I fill in the general add item fields')
def and_i_fill_in_the_general_add_item_fields(step):
    world.browser.maximize_window()  # Shop Editor features don't work well with automation unless maximized Jon M TBD
    for itemfields in step.hashes:
        world.browser.find_element_by_name("title").send_keys(itemfields["Title"])
        # TinyMCE uses iframes so need to use their javascript API to set the content
        world.browser.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(itemfields["Description"]))
        wait_for_element_with_name_to_be_displayed("price")
        world.browser.find_element_by_name("price").send_keys(itemfields["Price"])
        file = os.path.join(MEDIA_ROOT, itemfields["Image1"])
        world.browser.find_element_by_name("product_image").send_keys(file)


@step(u'I fill the following variants')
def with_quantity_color_and_sizeset(step, quantity, color, sizeset):
    for variation in step.hashes:


    sizeVariationElement = world.browser.find_element_by_name('sizeVariation')
    scroll_to_element(sizeVariationElement)
    variationSelection = Select(sizeVariationElement)
    time.sleep(2)
    variationSelection.select_by_value("1")  # Size Set
    sizeSetSelectionElement = world.browser.find_element_by_name('sizeSetSelectionTemplate0_sizeSetSelection')
    scroll_to_element(sizeSetSelectionElement)
    sizeSetSelection = Select(sizeSetSelectionElement)
    sizeSetSelection.select_by_visible_text(sizeset)
    time.sleep(1)
    colorSelection = Select(world.browser.find_element_by_name('sizeSetSelectionTemplate0_colorSelection0'))
    colorSelection.select_by_visible_text(color)
    world.browser.find_element_by_name('sizeSetSelectionTemplate0_quantityField0').send_keys(quantity)

@step(u'And I submit this item')
def and_i_submit_this_item(step):
    element = world.browser.find_element_by_name("productCreationForm")
    scroll_to_element(element)
    element.click()

@step(u'Then I should see (\d+) product(?s) total')
def i_should_see_n_products_total(step, total):
    products = world.browser.find_elements_by_css_selector(".shopItem")
    assert len(products) == int(total)
    
    
@step(u'When I click the delete button for the product')
def when_I_click_delete_button_product(step):
    world.browser.find_element_by_css_selector("#minMaxIcon").click()
    wait_for_element_with_link_text_to_be_displayed("Delete")
    world.browser.find_element_by_link_text("Delete").click()

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