from django.test import TestCase
from order.tasks import pay_designers
from oscar.core.loading import get_model

from common.factories import create_order

PaymentEvent = get_model('order', 'PaymentEvent')
ShippingEvent = get_model('order', 'ShippingEvent')
ShippingEventType = get_model('order', 'ShippingEventType')
PaymentEventType = get_model('order', 'PaymentEventType')
Order = get_model('order', 'Order')

class PayDesignersTests(TestCase):
    fixtures = ['all.json']

    def test_no_designers_to_pay(self):
        self.assertIs(len(PaymentEvent.objects.all()), 0, "No payments should exist")
        pay_designers()
        self.assertIs(len(PaymentEvent.objects.all()), 0, "No payments should exist since there were no shipping events from any designer")

    def test_no_payout_if_shipped_but_not_in_transit(self):
        order = create_order(number="1-10001")

        # Event marked as shipped, but not in transit, no payment made
        shipped_event = order.shipping_events.create(
            event_type=ShippingEventType.objects.get(code="shipped"))

        for line in order.lines.all():
            shipped_event.line_quantities.create(
                line=line, quantity=line.quantity)

        pay_designers()

        self.assertIs(len(PaymentEvent.objects.all()), 0, "No payments should exist since there were no 'in transit' events from any designer")


    def test_payout_on_one_full_order(self):
        self.assertIs(len(PaymentEvent.objects.all()), 0, "No payments should exist")

        order = create_order(number="1-10001")

        shipped_event = order.shipping_events.create(
            event_type=ShippingEventType.objects.get(code="shipped"))
        for line in order.lines.all():
            shipped_event.line_quantities.create(
                line=line, quantity=line.quantity)


        # Event marked as "in transit", payment should be made
        in_transit_event = order.shipping_events.create(
            event_type=ShippingEventType.objects.get(code="in transit"))
        for line in order.lines.all():
            in_transit_event.line_quantities.create(
                line=line, quantity=line.quantity)

        shipping_paid_event = order.payment_events.create(
            event_type=PaymentEventType.objects.get(code="shipping_paid"))
        for line in order.lines.all():
            shipping_paid_event.line_quantities.create(
                line=line, quantity=line.quantity)

        self.assertIs(len(PaymentEvent.objects.all()), 1, "1 payment should exist for the payment of shipping")

        pay_designers()

        self.assertIs(len(PaymentEvent.objects.all()), 2, "Another payment to designer should have been made since it is in transit")

    def test_no_payout_if_shipping_not_paid(self):
        pass


