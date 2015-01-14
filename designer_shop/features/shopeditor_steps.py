import time
import math

from common.lettuce_utils import *


@step(u'the shop editor is (\d+)% of the window size by default')
def and_the_shop_editor_is_percentage(step, percent):
    time.sleep(1)
    shopeditorheight = world.browser.find_element_by_css_selector('body').size['height']
    assert math.fabs(world.browser.find_element_by_css_selector('#shopEditorWindow').size['height'] - int(shopeditorheight*(float(percent)/100))) <= 1