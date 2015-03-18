from common.lettuce_utils import *
from django.conf import settings
import os


@step(u'the banner button is pressed')
def when_the_banner_button_is_selected(step):
    change_viewport_lg()
    wait_for_element_with_id_to_exist('xlBannerUploadButton').click()

@step(u'Then the banner file upload is displayed')
def then_the_banner_file_upload_is_displayed(step):
    wait_for_element_with_id_to_be_displayed('id_banner')

@step(u'And the submit Banner button is displayed')
def and_the_submit_banner_button_is_displayed(step):
    assert_id_exists('bannerModalFooterSubmit')

@step(u'And a banner is submitted')
def and_a_banner_is_submitted(step):
    bannerUploader = world.browser.find_element_by_id("id_banner")
    bannerUploader.send_keys(os.path.join(settings.PROJECT_DIR.child("static"), "img/banner-xl.jpg"))
    assert_selector_contains('#div_id_bannerCropping > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > '
                             'div:nth-child(1) > img:nth-child(1)', 'src', 'data:image/jpeg;base64')
    wait_for_element_with_id_to_be_clickable("bannerModalFooterSubmit").click()

@step(u'The selected banner file is saved')
def the_selected_banner_file_is_saved(step):
    assert_selector_contains('#div_id_bannerCropping > div:nth-child(1) > div:nth-child(3) > img:nth-child(3)',
                             'src', '/media/shops/demo/banner/banner-xl')
    assert_selector_contains('.banner>span>img', 'src', '/media/shops/demo/banner/banner-xl')