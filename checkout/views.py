from django.shortcuts import render
from django.conf import settings

from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView

# Create your views here.

class PaymentDetailsView(CorePaymentDetailsView):

    template_name = "payment_details.html"


    pre_conditions = (
        'check_basket_is_not_empty',
        'check_basket_is_valid')
        #'check_user_email_is_captured',
        #'check_shipping_data_is_captured')

    def get_context_data(self, **kwargs):
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)

        # if not hasattr(self, 'payer_id'):
        #     return ctx

        # This context generation only runs when in preview mode
        ctx.update({
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })

        return ctx