from oscar.apps.order.abstract_models import AbstractOrder
from decimal import Decimal as D, ROUND_FLOOR

class Order(AbstractOrder):
    @property
    def estimated_tinville_cut(self):
        return ((self.basket_total_excl_tax - self.shipping_excl_tax) * D('0.1')).quantize(D('0.01'), rounding=ROUND_FLOOR)

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

from oscar.apps.order.models import *