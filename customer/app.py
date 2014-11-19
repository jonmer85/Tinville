
from oscar.apps.customer.app import CustomerApplication as CoreCustomerApplication

from user.views import register # Jon M TODO migrate the user stuff to this Oscar overridden app


class CustomerApplication(CoreCustomerApplication):
    register_view = register
    # payment_details_view  = PaymentDetailsView

application = CustomerApplication()