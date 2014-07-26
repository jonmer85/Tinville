from common.lettuce_utils import *

@step(u'And the color picker textbox is displayed')
def and_the_color_picker_textbox_is_displayed(step):
    assert_class_exists('farbtasticcolorpicker')