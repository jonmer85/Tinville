from oscar.apps.order.abstract_models import AbstractOrder
from django.db import models
from oscar.apps.order.abstract_models import AbstractShippingEvent, AbstractPaymentEvent
from common.utils import get_designer_payout_amount
from decimal import Decimal as D, ROUND_FLOOR

class Order(AbstractOrder):
    @property
    def estimated_tinville_cut(self):
        return get_designer_payout_amount(self.basket_total_excl_tax - self.shipping_excl_tax)

    @property
    def estimated_tinville_credit_card_fees(self):
        return (self.estimated_tinville_cut * D('0.029')).quantize(D('0.01'), rounding=ROUND_FLOOR)

    @property
    def estimated_designer_credit_card_fees(self):
        return  (((self.basket_total_excl_tax - self.estimated_tinville_cut) * D('0.029')) + D('0.30')).quantize(D('0.01'), rounding=ROUND_FLOOR)

    @property
    def estimated_designer_cut(self):
        return self.basket_total_excl_tax - self.estimated_tinville_cut - self.estimated_designer_credit_card_fees - self.shipping_excl_tax

    @property
    def estimated_total_transaction_fees(self):
        return self.estimated_tinville_cut + self.estimated_designer_credit_card_fees

class ShippingEvent(AbstractShippingEvent):
    group = models.IntegerField(null=True)
    # The reference should refer to the transaction ID of the payment gateway
    # that was used for this event.
    reference = models.CharField("Reference", max_length=128, blank=True)

class PaymentEvent(AbstractPaymentEvent):
    group = models.IntegerField(null=True)

from oscar.apps.order.models import *