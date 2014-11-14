from django.test import TestCase
from order.tasks import pay_designers
from oscar.core.loading import get_model

from common.factories import create_order

PaymentEvent = get_model('order', 'PaymentEvent')
ShippingEvent = get_model('order', 'ShippingEvent')
Order = get_model('order', 'Order')

class PayDesignersTests(TestCase):

    def test_no_designers_to_pay(self):
        self.assertIs(len(PaymentEvent.objects.all()), 0, "No payments should exist")
        pay_designers()
        self.assertIs(len(PaymentEvent.objects.all()), 0, "No payments should exist since there were no shipping events from any designer")

    def test_payout_on_one_full_order(self):

        order = create_order()
        shipping_event = ShippingEvent.objects.create(
            order=order,
            lines=order.lines,
            event_type =


            order = models.ForeignKey(
        'order.Order', related_name='shipping_events', verbose_name=_("Order"))
    lines = models.ManyToManyField(
        'order.Line', related_name='shipping_events',
        through='ShippingEventQuantity', verbose_name=_("Lines"))
    event_type = models.ForeignKey(
        'order.ShippingEventType', verbose_name=_("Event Type"))
    notes = models.TextField(
        _("Event notes"), blank=True,
        help_text=_("This could be the dispatch reference, or a "
                    "tracking number"))
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
        )



