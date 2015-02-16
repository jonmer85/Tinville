from django.conf import settings
import os
import time

from common.lettuce_utils import *
from selenium.webdriver.support.ui import Select

from Tinville.settings.base import MEDIA_ROOT


@step(u'the (?:add|edit) item tab is selected')
def when_the_add_item_tab_is_selected(step):
    maximize_shop_editor()
    world.browser.find_element_by_css_selector('#optionContent>li>a[href="#addOrEditItem"]').click()
    wait_for_element_with_css_selector_to_be_displayed('#optionContent>.active>a[href="#addOrEditItem"]')



@step(u'And I fill in the general add item fields')
def and_i_fill_in_the_general_add_item_fields(step):

    change_viewport_lg()  # Shop Editor features don't work well with automation unless maximized Jon M TBD
    for itemfields in step.hashes:
        clear_and_send_keys(world.browser.find_element_by_name("title"), itemfields["Title"])
        wait_for_element_with_css_selector_to_be_clickable("a[href='#description']").click()
        # TinyMCE uses iframes so need to use their javascript API to set the content
        world.browser.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(itemfields["Description"]))
        clear_and_send_keys(wait_for_element_with_name_to_be_displayed("price"), itemfields["Price"])
        wait_for_element_with_name_to_exist("category")
        wait_for_element_with_name_to_be_displayed("category").send_keys(itemfields["Category"])
        file = os.path.join(settings.MEDIA_ROOT, itemfields["Image1"])
        wait_for_element_with_css_selector_to_be_clickable("a[href='#images']").click()
        wait_for_element_with_name_to_be_displayed("images-0-original").send_keys(file)
        wait_for_element_with_css_selector_to_exist("a[href='#accordion2']")
        wait_for_element_with_css_selector_to_be_clickable("a[href='#accordion2']").click()
        wait_for_element_with_name_to_exist('sizeVariation')
        Select(wait_for_element_with_name_to_be_displayed('sizeVariation')).select_by_value(itemfields['SizeVariation'])


def select_colors_and_quantities(sizePrefix, step):
    for (counter, colorQuantity) in enumerate(step.hashes):
        Select(wait_for_element_with_id_to_be_clickable(
            sizePrefix + "colorSelection" + unicode(counter))).select_by_visible_text(colorQuantity["Color"])
        clear_and_send_keys(wait_for_element_with_id_to_be_clickable(sizePrefix + "quantityField" + unicode(counter)), colorQuantity["Quantity"])


@step(u'I choose the size (.*) with row number (\d+) and I fill the following quantities and colors')
def i_choose_the_size_and_fill_colors_and_quantities(step, size_set, row_number):
    row_number = unicode(int(row_number) - 1)  # 0-bias it for indexing
    sizeSetPrefix = "sizeSetSelectionTemplate{0}_id_".format(row_number)
    Select(world.browser.find_element_by_id(sizeSetPrefix + "sizeSetSelection")).select_by_visible_text(size_set)
    select_colors_and_quantities(sizeSetPrefix, step)

@step(u'I choose the sizeX (\d*\.?\d*) and the sizeY (\d*\.?\d*) with row number (\d+) and I fill the following quantities and colors')
def i_choose_the_size_dims_and_fill_colors_and_quantities(step, dimX, dimY, row_number):
    row_number = unicode(int(row_number) - 1)  # 0-bias it for indexing
    sizeDimPrefix = "sizeDimensionSelectionTemplate{0}_id_".format(row_number)
    wait_for_element_with_id_to_be_displayed(sizeDimPrefix + "sizeDimensionSelectionWidth").send_keys(dimX)
    wait_for_element_with_id_to_be_displayed(sizeDimPrefix + "sizeDimensionSelectionLength").send_keys(dimY)
    select_colors_and_quantities(sizeDimPrefix, step)

@step(u'I choose the sizenumber (\d*\.?\d*) with row number (\d+) and I fill the following quantities and colors')
def i_choose_the_size_num_and_fill_colors_and_quantities(step, size_number, row_number):
    row_number = unicode(int(row_number) - 1)  # 0-bias it for indexing
    sizeNumPrefix = "sizeNumberSelectionTemplate{0}_id_".format(row_number)
    wait_for_element_with_id_to_be_displayed(sizeNumPrefix + "sizeNumberSelection").send_keys(size_number)
    select_colors_and_quantities(sizeNumPrefix, step)

@step(u'I add a new color to the size set product')
def i_add_a_new_color_to_the_size_set_product(step):
    world.browser.find_element_by_id('sizeSetSelectionTemplate2_id_colorSelection2')
    Select(wait_for_element_with_id_to_be_displayed('sizeSetSelectionTemplate2_id_colorSelection2')).select_by_visible_text("White")

@step(u'I expand the sizes group')
def i_expand_the_sizes_group(step):
    wait_for_element_with_css_selector_to_exist("a[href='#accordion2']")
    wait_for_element_with_css_selector_to_be_clickable("a[href='#accordion2']").click()

@step(u'I delete an existing size')
def i_delete_an_existing_size(step):
    change_viewport_lg()
    world.browser.find_element_by_id('sizeSetSelectionTemplate2_id_clearSizes')
    wait_for_element_with_id_to_be_clickable('sizeSetSelectionTemplate2_id_clearSizes').click()

@step(u'I delete an existing color')
def i_delete_an_existing_color(step):
    world.browser.find_element_by_id('sizeSetSelectionTemplate2_id_clearColorQuantity1')
    wait_for_element_with_id_to_be_clickable('sizeSetSelectionTemplate2_id_clearColorQuantity1').click()


@step(u'I change the quantity of one of the colors of the size set product')
def i_change_the_quantity_of_one_of_the_colors_of_the_size_set_product(self):
    world.browser.find_element_by_id('sizeSetSelectionTemplate2_id_quantityField1')
    quantityField = wait_for_element_with_id_to_be_displayed('sizeSetSelectionTemplate2_id_quantityField1')
    quantityField.clear()
    quantityField.send_keys("4")

@step(u'I add a new size to the size set product')
def i_add_a_new_size_to_the_size_set_product(step):
    change_viewport_lg()
    world.browser.find_element_by_id('sizeSetSelectionTemplate3_id_sizeSetSelection')
    Select(wait_for_element_with_id_to_be_displayed('sizeSetSelectionTemplate3_id_sizeSetSelection')).select_by_visible_text("XL")
    Select(wait_for_element_with_id_to_be_displayed('sizeSetSelectionTemplate3_id_colorSelection0')).select_by_visible_text("Black")
    quantityField = wait_for_element_with_id_to_be_displayed('sizeSetSelectionTemplate3_id_quantityField0')
    quantityField.clear()
    quantityField.send_keys("8")

@step(u'I should see a confirmation message stating that the item was (.*)')
def i_should_see_a_confirmation_message_stating_that_the_item_was_created_or_updated(step, createdOrUpdated):
    wait_for_element_with_id_to_exist("messagesModal")
    assert_selector_contains_text("#messagesModal .alert-success", "Item has been successfully {0}!".format(createdOrUpdated))
    wait_for_element_with_css_selector_to_be_clickable("#messagesModal .close").click()
    wait_for_element_with_id_to_not_be_displayed("messagesModal")

@step(u'And I submit this item')
def and_i_submit_this_item(step):
    element = world.browser.find_element_by_name("productCreationForm")
    element.click()

@step(u'Then I should see (\d+) product(?s) total')
def i_should_see_n_products_total(step, total):
    minimize_shop_editor()
    products = world.browser.find_elements_by_css_selector(".shopItem")
    assert len(products) == int(total)

@step(u'my color, quantity, and size selections are')
def my_color_quantity_and_size_selections_are(step):
    colors_to_sizes_and_quantities = {}

    for variant in step.hashes:
        color = variant["Color"]
        if color not in colors_to_sizes_and_quantities:
            colors_to_sizes_and_quantities[color] = []
        colors_to_sizes_and_quantities[color].append({"Size": variant["Size"], "Quantity": variant["Quantity"]})

    color_select = Select(wait_for_element_with_id_to_be_displayed("itemColorSelection"))
    wait_for_ajax_to_complete()
    assert len(colors_to_sizes_and_quantities.keys()) == (len(color_select.options) - 1), "Because the number of colors expected were incorrect"

    size_select = Select(wait_for_element_with_id_to_be_displayed("itemSizeSelection"))
    for color, sizes_and_quantities in colors_to_sizes_and_quantities.iteritems():
        color_select.select_by_visible_text(color)
        assert len(sizes_and_quantities) == len(size_select.options) - 1, "Because the expected sizes for color {0} is not correct".format(color)
        for size_and_quantity in sizes_and_quantities:
            size = size_and_quantity["Size"]
            quantity = size_and_quantity["Quantity"]
            assert size in map(lambda x: x.text, size_select.options), "Because an expected size was not found for color {0}".format(color)
            size_select.select_by_visible_text(size)
            assert_selector_contains_text('.itemStockQuantity', quantity+' ')

@step(u'my primary image is visible')
def my_primary_image_is_visible(step):
    assert_every_selector_contains("#itemSelectedImage", "src", ".jpg")


@step(u'I click the edit button on the basic size set product')
def i_click_the_edit_button_on_the_basic_size_set_product(self):
    minimize_shop_editor()
    wait_for_element_with_css_selector_to_be_clickable("a[href='/demo/edit/testsizesetitem'].overlayEdit").click()

@step(u'I plan to change the default image of the size set product')
def i_change_the_default_image_of_the_size_set_product(step):
    world.browser.find_element_by_css_selector("a[href='/demo/testsizesetitem']").click()
    world.browser.originalImageURL = wait_for_element_with_css_selector_to_exist("#itemSelectedImageLink").get_attribute("href")
    world.browser.get(lettuce.django.get_server().url('/Demo/edit'))
    wait_for_element_with_id_to_be_displayed('shopEditor')

@step(u'my primary image is different from the original')
def my_primary_image_is_visible_and_different_from_original(step):
    assert_every_selector_contains("#itemSelectedImage", "src", ".jpg")
    assert wait_for_element_with_css_selector_to_exist("#itemSelectedImageLink").get_attribute("href") != world.browser.originalImageURL, \
        "Because the image should be different"












    
    
@step(u'When I click the delete button for the product')
def when_I_click_delete_button_product(step):
    minimize_shop_editor()
    wait_for_element_with_id_to_be_clickable("testsizesetitem").click()

@step(u'And I click ok on the confirmation')
def and_I_click_ok_confirmation(step):
    wait_for_element_with_css_selector_to_be_clickable("#okDeleteBtn").click()

@step(u'Then the product is removed')
def then_product_is_removed(step):
    try:
        world.browser.find_element_by_css_selector("a[href='/demo/testsizesetitem']")
    except NoSuchElementException:
        return True
    return False

@step(u'And the shop editor refreshes in a minimized state')
def and_shopEditor_refreshes_minimized(step):
    wait_for_element_with_css_selector_to_be_displayed("#minMaxIcon.glyphicon-chevron-up")
    wait_for_element_with_css_selector_to_exist("#editorPanels.collapse")



