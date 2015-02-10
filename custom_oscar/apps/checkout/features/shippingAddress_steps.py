# from common.lettuce_utils import *
#
# @step(u'Given the shipping address page')
# def given_the_shipping_address_page(step):
#     world.browser.get(lettuce.django.get_server().url('/shipping-address'))
#     assert world.browser.find_element_by_class_name('form-stacked well')
#
# @step(u'When the form is displayed')
# def when_the_form_is_displayed(step):
#     assert world.browser.find_element_by_class_name('form-stacked well')
#
# @step(u'Then the first name field is displayed')
# def then_the_first_name_field_is_displayed(step):
#     assert world.browser.find_element_by_id('id_first_name')
#
# @step(u'And the last name field is displayed')
# def and_the_last_name_field_is_displayed(step):
#     assert world.browser.find_element_by_id('id_last_name')
#
# @step(u'And the first address line field is displayed')
# def and_the_first_address_line_field_is_displayed(step):
#     assert world.browser.find_element_by_id('id_line1')
#
# @step(u'And the second address line field is displayed')
# def and_the_second_address_line_field_is_displayed(step):
#     assert world.browser.find_element_by_id('id_line2')
#
# @step(u'And the third address line field is displayed')
# def and_the_third_address_line_field_is_displayed(step):
#     assert world.browser.find_element_by_id('id_line3')
#
# @step(u'And the city field is displayed')
# def and_the_city_field_is_displayed(step):
#     assert world.browser.find_element_by_id('id_line4')
#
# @step(u'And the state field is displayed')
# def and_the_state_field_is_displayed(step):
#     assert world.browser.find_element_by_id('id_state')
#
# @step(u'And the zip field is displayed')
# def and_the_zip_field_is_displayed(step):
#     assert world.browser.find_element_by_id('id_postcode')
#
# @step(u'And the phone number field is displayed')
# def and_the_phone_number_field_is_displayed(step):
#     assert world.browser.find_element_by_id('id_phone_number')
#
# @step(u'Then I add an invalid address')
# def then_I_add_an_invalid_address(step):
#     wait_for_element_with_css_selector_to_be_clickable("a[href='/accounts/addresses/add/']").click()
#     wait_for_element_with_name_to_be_displayed('first_name').send_keys('Joe')
#     wait_for_element_with_name_to_be_displayed('last_name').send_keys('Schmoe')
#     wait_for_element_with_name_to_be_displayed('line1').send_keys('10 Schmoe St')
#     wait_for_element_with_name_to_be_displayed('line4').send_keys('SchmoeVille')
#     wait_for_element_with_name_to_be_displayed('state').send_keys('SchmoeLand')
#     wait_for_element_with_name_to_be_displayed('postcode').send_keys('12345')
#     wait_for_element_with_css_selector_to_be_clickable("button[type='submit']").click()
#     wait_for_element_with_css_selector_to_be_clickable("#messagesModal .close").click()
#
# @step(u'and the invalid address is submitted')
# def and_the_invalid_address_is_submitted(step):
#     world.browser.find_element_by_class_name("id_SubmitAboutContent").click()
#     wait_for_ajax_to_complete()
#     assert world.browser.find_element_by_class_name('alert alert-block alert-danger')
#
# @step(u'Then I add a valid address')
# def then_I_add_a_address(step):
#     wait_for_element_with_css_selector_to_be_clickable("a[href='/accounts/addresses/add/']").click()
#     wait_for_element_with_name_to_be_displayed('first_name').send_keys('Joe')
#     wait_for_element_with_name_to_be_displayed('last_name').send_keys('Schmoe')
#     wait_for_element_with_name_to_be_displayed('line1').send_keys('14 Minnesota Ave.')
#     wait_for_element_with_name_to_be_displayed('line4').send_keys('Somerville')
#     wait_for_element_with_name_to_be_displayed('state').send_keys('Ma')
#     wait_for_element_with_name_to_be_displayed('postcode').send_keys('02145')
#     wait_for_element_with_css_selector_to_be_clickable("button[type='submit']").click()
#     wait_for_element_with_css_selector_to_be_clickable("#messagesModal .close").click()
#
# @step(u'and the invalid address is submitted')
# def and_the_invalid_address_is_submitted(step):
#     world.browser.find_element_by_class_name("id_SubmitAboutContent").click()
#     wait_for_ajax_to_complete()
#     assert world.browser.get(lettuce.django.get_server().url('/payment-details'))
#
#
#
#
#
#
#
#
