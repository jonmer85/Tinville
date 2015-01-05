
from oscar.apps.customer.app import CustomerApplication as CoreCustomerApplication

from .views import AddressUpdateView, AddressCreateView, AddressListView, AddressChangeStatusView


class CustomerApplication(CoreCustomerApplication):

    address_update_view = AddressUpdateView

    address_create_view = AddressCreateView

    address_list_view = AddressListView

    address_change_status_view = AddressChangeStatusView

application = CustomerApplication()
