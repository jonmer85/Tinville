from decimal import Decimal as D

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.db.models import get_model

from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from oscar.apps.shipping.methods import NoShippingRequired, FixedPrice
from oscar_stripe import facade, PAYMENT_METHOD_STRIPE, PAYMENT_EVENT_PURCHASE

# Create your views here.
from oscar_stripe.facade import Facade


SourceType = get_model('payment', 'SourceType')
Source = get_model('payment', 'Source')
Country = get_model('address', 'Country')
ShippingAddress = get_model('order', 'ShippingAddress')


class PaymentDetailsView(CorePaymentDetailsView):

    template_name = "payment_details.html"


    pre_conditions = (
        'check_basket_is_not_empty',
        'check_basket_is_valid')
        #'check_user_email_is_captured',
        #'check_shipping_data_is_captured')

    def get_context_data(self, **kwargs):
        # ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        #
        # if not hasattr(self, 'stripe_token'):
        #     return ctx

        # This context generation only runs when in preview mode


        # ctx.update({
        #     'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY
        # })

        return {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY}

    def post(self, request, *args, **kwargs):

        error_msg = (
            "A problem occurred communicating with PayPal "
            "- please try again later"
        )
        try:
            self.token = request.POST['stripe_token']
        except KeyError:
            # Probably suspicious manipulation if we get here
            messages.error(self.request, error_msg)
            return HttpResponseRedirect(reverse('home'))

        submission = self.build_submission()
        return self.submit(**submission)

    def build_submission(self, **kwargs):
        submission = super(
            PaymentDetailsView, self).build_submission(**kwargs)
        # Pass the user email so it can be stored with the order
        # submission['order_kwargs']['guest_email'] = self.txn.value('EMAIL')
        # Pass Stripe params
        submission['payment_kwargs']['stripe_token'] = self.token
        return submission

    def handle_payment(self, order_number, total, **kwargs):
        stripe_ref = Facade().charge(
            order_number,
            total,
            card=self.request.POST['stripe_token'],
            description=self.payment_description(order_number, total, **kwargs),
            metadata=self.payment_metadata(order_number, total, **kwargs))

        source_type, __ = SourceType.objects.get_or_create(name=PAYMENT_METHOD_STRIPE)
        source = Source(
            source_type=source_type,
            currency=settings.STRIPE_CURRENCY,
            amount_allocated=total.incl_tax,
            amount_debited=total.incl_tax,
            reference=stripe_ref)
        self.add_payment_source(source)

        self.add_payment_event(PAYMENT_EVENT_PURCHASE, total.incl_tax)

    def payment_description(self, order_number, total, **kwargs):
        # Jon M TODO - Add case for anonymous user with email
        return self.request.user.email
        # return self.request.POST[STRIPE_EMAIL]


    def payment_metadata(self, order_number, total, **kwargs):
        return {'order_number': order_number}

    def get_shipping_address(self, basket):
        """
        Return a created shipping address instance, created using
        the data returned by PayPal.
        """
        # Determine names - PayPal uses a single field
        # Jon M TODO
        # ship_to_name = self.txn.value('PAYMENTREQUEST_0_SHIPTONAME')
        # if ship_to_name is None:
        #     return None
        # first_name = last_name = None
        # parts = ship_to_name.split()
        # if len(parts) == 1:
        #     last_name = ship_to_name
        # elif len(parts) > 1:
        #     first_name = parts[0]
        #     last_name = " ".join(parts[1:])

        # return ShippingAddress(
        #     first_name=first_name,
        #     last_name=last_name,
        #     line1=self.txn.value('PAYMENTREQUEST_0_SHIPTOSTREET'),
        #     line2=self.txn.value('PAYMENTREQUEST_0_SHIPTOSTREET2', default=""),
        #     line4=self.txn.value('PAYMENTREQUEST_0_SHIPTOCITY', default=""),
        #     state=self.txn.value('PAYMENTREQUEST_0_SHIPTOSTATE', default=""),
        #     postcode=self.txn.value('PAYMENTREQUEST_0_SHIPTOZIP'),
        #     country=Country.objects.get(iso_3166_1_a2=self.txn.value('PAYMENTREQUEST_0_SHIPTOCOUNTRYCODE'))
        return ShippingAddress(
            first_name="Joe",
            last_name="Shmoe",
            line1='123 Main St',
            line2="",
            line4="Londonderry",
            state="NH",
            postcode="03053",
            country=Country.objects.get(iso_3166_1_a2="US"))


    def get_shipping_method(self, basket, shipping_address=None, **kwargs):
        """
        Return the shipping method used
        """
        if not basket.is_shipping_required():
            return NoShippingRequired()

        # Instantiate a new FixedPrice shipping method instance
        # Jon M TODO
        charge_incl_tax = D(9.99) #D(self.txn.value('PAYMENTREQUEST_0_SHIPPINGAMT'))
        # Assume no tax for now
        charge_excl_tax = charge_incl_tax
        method = FixedPrice(charge_excl_tax, charge_incl_tax)
        name = "Test shipping option"#self.txn.value('SHIPPINGOPTIONNAME')

        if not name:
            session_method = super(PaymentDetailsView, self).get_shipping_method(
                basket, shipping_address, **kwargs)
            if session_method:
                method.name = session_method.name
        else:
            method.name = name
        return method




