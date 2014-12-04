
from oscar.apps.checkout.app import CheckoutApplication as CoreCheckoutApplication

from .views import PaymentDetailsView, IndexView, ShippingAddressView, ThankYouView

class CheckoutApplication(CoreCheckoutApplication):
    payment_details_view = PaymentDetailsView
    index_view = IndexView
    shipping_address_view = ShippingAddressView
    thankyou_view = ThankYouView

application = CheckoutApplication()