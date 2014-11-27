from django.conf import settings
# from oscar.apps.checkout.mixins import OrderNumberGenerator Jon M WARNING!! For some reason importing this makes this module not be loadable!
from oscar.apps.order.utils import OrderCreator as CoreOrderCreator
from oscar.apps.shipping.methods import Free
from oscar.core.loading import get_model, get_class
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal as D, ROUND_FLOOR

Order = get_model('order', 'Order')
Line = get_model('order', 'Line')
order_placed = get_class('order.signals', 'order_placed')

class OrderCreator(CoreOrderCreator):
    def place_order(self, basket, total,
                    user=None, shipping_method=None, shipping_address=None,
                    billing_address=None, order_number=None, status=None,
                    **kwargs):
        """
        Placing an order involves creating all the relevant models based on the
        basket and session data.
        """
        if basket.is_empty:
            raise ValueError(_("Empty baskets cannot be submitted"))
        if not shipping_method:
            shipping_method = Free()
        if not status and hasattr(settings, 'OSCAR_INITIAL_ORDER_STATUS'):
            status = getattr(settings, 'OSCAR_INITIAL_ORDER_STATUS')
        try:
            Order._default_manager.get(number=order_number)
        except Order.DoesNotExist:
            pass
        else:
            raise ValueError(_("There is already an order with number %s")
                             % order_number)
        shop = kwargs.pop('shop', None)

        # Ok - everything seems to be in order, let's place the order
        order = self.create_order_model(
            user, basket, shipping_address, shipping_method, billing_address,
            total, order_number, status, **kwargs)
        for line in basket.all_lines():
            if shop is None or line.product.shop.id == shop.id:
                # Top level order and Shop orders track product lines
                self.create_line_models(order, line)
            if shop and line.product.shop.id == shop.id:
                # Stock is updated only for the Shop orders, not the top level order
                self.update_stock_records(line)

        for application in basket.offer_applications:
            # Trigger any deferred benefits from offers and capture the
            # resulting message
            application['message'] \
                = application['offer'].apply_deferred_benefit(basket)
            # Record offer application results
            if application['result'].affects_shipping:
                # Skip zero shipping discounts
                if shipping_method.discount <= D('0.00'):
                    continue
                # If a shipping offer, we need to grab the actual discount off
                # the shipping method instance, which should be wrapped in an
                # OfferDiscount instance.
                application['discount'] = shipping_method.discount
            self.create_discount_model(order, application)
            self.record_discount(application)

        for voucher in basket.vouchers.all():
            self.record_voucher_usage(order, voucher, user)

        # Send signal for analytics to pick up
        order_placed.send(sender=self, order=order, user=user)

        return order

def get_designer_payout_amount(original_amount):
    # We take 10% of sales. Jon M TODO abstract the sales percentage to settings
    return (original_amount -
            ((original_amount * settings.TINVILLE_ORDER_SALES_CUT).quantize(D('0.01'), rounding=ROUND_FLOOR))
            .quantize(D('0.01'), rounding=ROUND_FLOOR))


