
from oscar.apps.customer.app import CustomerApplication as CoreCustomerApplication

from user.views import register # Jon M TODO migrate the user stuff to this Oscar overridden app

from .views import AddressUpdateView

class CustomerApplication(CoreCustomerApplication):
    
    register_view = register

    address_update_view = AddressUpdateView

application = CustomerApplication()
