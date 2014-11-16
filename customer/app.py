
from oscar.apps.customer.app import CustomerApplication as CoreCustomerApplication

from .views import AddressUpdateView

class CustomerApplication(CoreCustomerApplication):
    
    register_view = register

    address_update_view = AddressUpdateView

application = CustomerApplication()
