
from oscar.apps.checkout.app import CheckoutApplication as CoreCheckoutApplication

from .views import PaymentDetailsView

class CheckoutApplication(CoreCheckoutApplication):
    payment_details_view  = PaymentDetailsView

application = CheckoutApplication()