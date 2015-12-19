from oscar.apps.order.abstract_models import AbstractOrder
from django.db import models
from oscar.apps.order.abstract_models import AbstractShippingEvent, AbstractPaymentEvent
from common.utils import get_designer_payout_amount
from decimal import Decimal as D, ROUND_FLOOR

class Order(AbstractOrder):
    @property
    def estimated_tinville_cut(self):
        return self.total_excl_tax - self.estimated_designer_cut - self.shipping_excl_tax

    @property
    def estimated_credit_card_fees(self):
        return ((self.total_incl_tax * D('0.29')) + D('0.30')).quantize(D('0.01'), rounding=ROUND_FLOOR)

    @property
    def estimated_designer_cut(self):
        return get_designer_payout_amount(self.total_excl_tax - self.shipping_excl_tax)

    promoter = models.ForeignKey('user.TinvilleUser', verbose_name="Promoter", blank=True, null=True)


class ShippingEvent(AbstractShippingEvent):
    group = models.IntegerField(null=True)
    # The reference should refer to the transaction ID of the payment gateway
    # that was used for this event.
    reference = models.CharField("Reference", max_length=128, blank=True, default='')
    label_url = models.URLField("Label_Url", null=True)
    tracking_code = models.TextField("tracking_code", null=True)

class PaymentEvent(AbstractPaymentEvent):
    group = models.IntegerField(null=True)

from oscar.apps.order.models import *