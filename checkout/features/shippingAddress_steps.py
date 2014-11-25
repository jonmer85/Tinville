from common.lettuce_utils import *

@step(u'Given the shipping address page')
def given_the_shipping_address_page(step):
    world.browser.get(lettuce.django.get_server().url('/shipping-address'))