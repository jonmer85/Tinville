from common.factories import create_order, create_product, create_basket_with_products, create_basket
from django.contrib.auth.models import Permission
from custom_oscar.apps.catalogue.models import Product
from user.models import TinvilleUser as User
from lettuce import step
from common.lettuce_utils import *

@step("My user has correct permissions")
def my_user_has_correct_permissions(step):
    user = User.objects.get(pk=2)
    dashboard_access_perm = Permission.objects.get(
                codename='dashboard_access', content_type__app_label='partner')
    user.user_permissions.add(dashboard_access_perm)
    user.save()
    world.browser.get(lettuce.django.get_server().url('/'))
    sign_in("demo@user.com", "tinville")

@step("I have some basic dashboard data")
def i_have_some_basic_dashboar_data(step):
    my_user_has_correct_permissions(step)
    product_list = []
    product_list.append(Product.objects.get(pk=2))
    product_list.append(Product.objects.get(pk=3))
    basket1 = create_basket_with_products(product_list)
    basket2 = create_basket_with_products(product_list)
    create_order(number="1-10002", basket=basket1, user=User.objects.get(pk=2), shop=Shop.objects.get(pk=1))
    create_order(number="1-10003", basket=basket2, user=User.objects.get(pk=2), shop=Shop.objects.get(pk=1))