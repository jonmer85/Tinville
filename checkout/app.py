
from oscar.apps.checkout.app import CheckoutApplication as CoreCheckoutApplication

from .views import PaymentDetailsView, IndexView

class CheckoutApplication(CoreCheckoutApplication):
    payment_details_view  = PaymentDetailsView
    index_view = IndexView

application = CheckoutApplication()