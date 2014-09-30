from django.shortcuts import render

from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView

# Create your views here.

class PaymentDetailsView(CorePaymentDetailsView):


    pre_conditions = (
        'check_basket_is_not_empty',
        'check_basket_is_valid')
        #'check_user_email_is_captured',
        #'check_shipping_data_is_captured')