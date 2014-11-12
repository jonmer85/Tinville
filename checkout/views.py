import logging
import six

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.db.models import get_model
from django.utils.translation import ugettext as _

from oscar.apps.checkout import signals
from oscar.core.loading import get_class, get_classes
from oscar.core import prices

from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView, IndexView as CoreIndexView,\
    ShippingAddressView as CoreShippingAddressView, ThankYouView as CoreThankYouView, GatewayForm, ShippingAddressForm
from oscar.apps.shipping.methods import NoShippingRequired, Free
from oscar_stripe import facade, PAYMENT_METHOD_STRIPE, PAYMENT_EVENT_PURCHASE

# Create your views here.
from oscar_stripe.facade import Facade

from checkout.forms import PaymentInfoFormWithTotal

RedirectRequired, UnableToTakePayment, PaymentError \
    = get_classes('payment.exceptions', ['RedirectRequired',
                                         'UnableToTakePayment',
                                         'PaymentError'])
UnableToPlaceOrder = get_class('order.exceptions', 'UnableToPlaceOrder')


SourceType = get_model('payment', 'SourceType')
Source = get_model('payment', 'Source')
Country = get_model('address', 'Country')
ShippingAddress = get_model('order', 'ShippingAddress')

# Standard logger for checkout events
logger = logging.getLogger('oscar.checkout')


class PaymentDetailsView(CorePaymentDetailsView):

    template_name = "payment_details.html"


    def get_context_data(self, **kwargs):
        # ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        #
        # if not hasattr(self, 'stripe_token'):
        #     return ctx

        # This context generation only runs when in preview mode
        ctx = ({
            'total': self.request.basket.total_incl_tax,
            'payment_currency': self.request.basket.currency,
            'form': PaymentInfoFormWithTotal(),
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY
        })

        return ctx

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

    def get_shipping_method(self, basket, shipping_address=None, **kwargs):
        """
        Return the shipping method used
        """
        if not basket.is_shipping_required():
            return NoShippingRequired()

        method = Free

        return method

    def submit(self, user, basket, shipping_address, shipping_method,  # noqa (too complex (10))
               order_total, payment_kwargs=None, order_kwargs=None):
        """
        Submit a basket for order placement.

        The process runs as follows:

         * Generate an order number
         * Freeze the basket so it cannot be modified any more (important when
           redirecting the user to another site for payment as it prevents the
           basket being manipulated during the payment process).
         * Attempt to take payment for the order
           - If payment is successful, place the order
           - If a redirect is required (eg PayPal, 3DSecure), redirect
           - If payment is unsuccessful, show an appropriate error message

        :basket: The basket to submit.
        :payment_kwargs: Additional kwargs to pass to the handle_payment method
        :order_kwargs: Additional kwargs to pass to the place_order method
        """
        if payment_kwargs is None:
            payment_kwargs = {}
        if order_kwargs is None:
            order_kwargs = {}

        # Taxes must be known at this point
        assert basket.is_tax_known, (
            "Basket tax must be set before a user can place an order")
        assert shipping_method.is_tax_known, (
            "Shipping method tax must be set before a user can place an order")

        # Freeze the basket so it cannot be manipulated while the customer is
        # completing payment on a 3rd party site.  Also, store a reference to
        # the basket in the session so that we know which basket to thaw if we
        # get an unsuccessful payment response when redirecting to a 3rd party
        # site.
        self.freeze_basket(basket)
        self.checkout_session.set_submitted_basket(basket)

        # We define a general error message for when an unanticipated payment
        # error occurs.
        error_msg = _("A problem occurred while processing payment for this "
                      "order - no payment has been taken.  Please "
                      "contact customer services if this problem persists")

        signals.pre_payment.send_robust(sender=self, view=self)

        # Generate an order number for the top level that includes orders from all the shops
        top_level_order_number = self.generate_order_number(basket)
        self.checkout_session.set_order_number(top_level_order_number)

        logger.info("Order #%s: beginning submission process for basket #%d",
                        top_level_order_number, basket.id)

        items_by_shop = {}

        try:
            self.handle_payment(top_level_order_number, order_total, **payment_kwargs)
        except RedirectRequired as e:
            # Redirect required (eg PayPal, 3DS)
            logger.info("Order #%s: redirecting to %s", top_level_order_number, e.url)
            return HttpResponseRedirect(e.url)
        except UnableToTakePayment as e:
            # Something went wrong with payment but in an anticipated way.  Eg
            # their bankcard has expired, wrong card number - that kind of
            # thing. This type of exception is supposed to set a friendly error
            # message that makes sense to the customer.
            msg = six.text_type(e)
            logger.warning(
                "Order #%s: unable to take payment (%s) - restoring basket",
                top_level_order_number, msg)
            self.restore_frozen_basket()

            # We assume that the details submitted on the payment details view
            # were invalid (eg expired bankcard).
            return self.render_payment_details(
                self.request, error=msg, **payment_kwargs)
        except PaymentError as e:
            # A general payment error - Something went wrong which wasn't
            # anticipated.  Eg, the payment gateway is down (it happens), your
            # credentials are wrong - that king of thing.
            # It makes sense to configure the checkout logger to
            # mail admins on an error as this issue warrants some further
            # investigation.
            msg = six.text_type(e)
            logger.error("Order #%s: payment error (%s)", top_level_order_number, msg,
                         exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=error_msg, **payment_kwargs)
        except Exception as e:
            # Unhandled exception - hopefully, you will only ever see this in
            # development...
            logger.error(
                "Order #%s: unhandled exception while taking payment (%s)",
                top_level_order_number, e, exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=error_msg, **payment_kwargs)

        top_level_order = None
        try:
            top_level_order = self.handle_order_placement(
                top_level_order_number, user, basket, shipping_address, shipping_method,
                prices.Price(currency=basket.currency, excl_tax=basket.total_excl_tax, incl_tax=basket.total_excl_tax), **order_kwargs)
        except UnableToPlaceOrder as e:
            # It's possible that something will go wrong while trying to
            # actually place an order.  Not a good situation to be in as a
            # payment transaction may already have taken place, but needs
            # to be handled gracefully.
            msg = six.text_type(e)
            logger.error("Order #%s: unable to place order - %s",
                         top_level_order_number, msg, exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=msg, **payment_kwargs)

        # Collect information to split into an order for each shop
        for line in basket.all_lines():
            if(line.product.shop not in items_by_shop):
                items_by_shop[line.product.shop] = {"products": [], "order_total": 0}
            items_by_shop[line.product.shop]["products"].append(line.product),
            items_by_shop[line.product.shop]["order_total"] += line.line_price_excl_tax

        for shop in items_by_shop.keys():

            # We generate the order number first as this will be used
            # in payment requests (ie before the order model has been
            # created).  We also save it in the session for multi-stage
            # checkouts (eg where we redirect to a 3rd party site and place
            # the order on a different request).
            order_number = self.generate_order_number(basket, shop.id)
            order = None
            # This is needed to clear the payment events as to not create the payment event on the sub orders
            self._payment_events = []
            try:
                order_kwargs['shop'] = shop
                order = self.handle_order_placement(
                    order_number, user, basket, shipping_address, shipping_method,
                    prices.Price(currency=basket.currency, excl_tax=items_by_shop[shop]["order_total"],
                                 incl_tax=items_by_shop[shop]["order_total"]),
                                 **order_kwargs)
            except UnableToPlaceOrder as e:
                # It's possible that something will go wrong while trying to
                # actually place an order.  Not a good situation to be in as a
                # payment transaction may already have taken place, but needs
                # to be handled gracefully.
                msg = six.text_type(e)
                logger.error("Order #%s: unable to place order - %s",
                             order_number, msg, exc_info=True)
                self.restore_frozen_basket()
                return self.render_preview(
                    self.request, error=msg, **payment_kwargs)




        signals.post_payment.send_robust(sender=self, view=self)

        # If all is ok with payment, try and place order
        logger.info("Order #%s: payment successful, placing order",
                    top_level_order_number)

        basket.submit()

        return self.handle_successful_order(top_level_order)

    def generate_order_number(self, basket, shop_id=None):
        order_num = 100000 + basket.id
        if shop_id is not None:
            order_num = str(shop_id) + '-' + str(order_num)
        return order_num



    def handle_order_placement(self, order_number, user, basket,
                               shipping_address, shipping_method,
                               total, **kwargs):
        """
        Write out the order models and return the appropriate HTTP response

        We deliberately pass the basket in here as the one tied to the request
        isn't necessarily the correct one to use in placing the order.  This
        can happen when a basket gets frozen.
        """
        order = self.place_order(
            order_number, user, basket, shipping_address, shipping_method,
            total, **kwargs)

        return order



class IndexView(CoreIndexView):
    template_name = 'gateway.html'
    form_class = GatewayForm

class ShippingAddressView(CoreShippingAddressView):
    template_name = 'shipping_address.html'
    form_class = ShippingAddressForm

class ThankYouView(CoreThankYouView):
    template_name = 'thank-you.html'
