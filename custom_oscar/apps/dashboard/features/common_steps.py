from common.factories import create_order, create_product, create_basket_with_products, create_basket
from django.contrib.auth.models import Permission
from custom_oscar.apps.catalogue.models import Product
from custom_oscar.apps.order.models import Order
from lettuce import step
from common.lettuce_utils import *

@step("I have some basic dashboard data")
def i_have_some_basic_dashboar_data(step):
    setup_basic_order_data()

