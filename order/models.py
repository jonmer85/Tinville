from django.db import models

from oscar.apps.order.abstract_models import AbstractShippingEvent, AbstractPaymentEvent


class ShippingEvent(AbstractShippingEvent):
    group = models.IntegerField(null=True)

    # The reference should refer to the transaction ID of the payment gateway
    # that was used for this event.
    reference = models.CharField("Reference", max_length=128, blank=True)
    label_url = models.URLField("Label_Url", null=True)
    tracking_code = models.TextField("tracking_code", null=True)

class PaymentEvent(AbstractPaymentEvent):
    group = models.IntegerField(null=True)




from oscar.apps.order.models import *