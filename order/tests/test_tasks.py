from decimal import Decimal
from designer_shop.models import Shop
from django.conf import settings
from django.test import TestCase
from order.tasks import pay_designers
from oscar.core.loading import get_model

from common.factories import create_order
import stripe
from user.models import TinvilleUser, DesignerPayout

PaymentEvent = get_model('order', 'PaymentEvent')
ShippingEvent = get_model('order', 'ShippingEvent')
ShippingEventType = get_model('order', 'ShippingEventType')
PaymentEventType = get_model('order', 'PaymentEventType')
Order = get_model('order', 'Order')


class PayDesignersTests(TestCase):
    fixtures = ['all.json']

    def setUp(self):
        self.user = TinvilleUser.objects.create(email="joe@schmoe.com")
        # Create a Stripe recipient so we can pay the user
        self.stripe = stripe
        self.stripe.api_key = settings.STRIPE_SECRET_KEY

        result = self.stripe.Recipient.create(
            name="Joe Schmoe",
            type="individual",
            card= {
                'number': '4000056655665556',
                'exp_month': '12',
                'exp_year': '2030',
                'cvc': '123'
            }
        )

        self.user.recipient_id = result.id
        self.user.save()

        self.shop = Shop.objects.create(name='SchmoeVille', user=self.user)
        self.order = create_order(number="2-10001", user=self.user, shop=self.shop)

        self.assertEqual(len(PaymentEvent.objects.all()), 0, "No payments should exist")
        self.assertEqual(len(DesignerPayout.objects.all()), 0, "No designer payout should be recorded yet")

    def tearDown(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        rp = stripe.Recipient.retrieve(self.user.recipient_id)
        rp.delete()

    def test_no_designers_to_pay(self):
        pay_designers()
        self.assertEqual(len(PaymentEvent.objects.all()), 0,
                      "No payments should exist since there were no shipping events from any designer")

    def test_no_payout_if_shipped_but_not_in_transit(self):

        # Event marked as shipped, but not in transit, no payment made
        shipped_event = self.order.shipping_events.create(
            event_type=ShippingEventType.objects.get(code="shipped"), group=0)

        for line in self.order.lines.all():
            shipped_event.line_quantities.create(line=line, quantity=line.quantity)

        pay_designers()

        self.assertEqual(len(PaymentEvent.objects.all()), 0,
                      "No payments should exist since there were no 'in transit' events from any designer")


    def create_shipping_events(self):
        shipped_event = self.order.shipping_events.create(
            event_type=ShippingEventType.objects.get(code="shipped"), group=1)
        for line in self.order.lines.all():
            shipped_event.line_quantities.create(line=line, quantity=line.quantity)


        # Event marked as "in transit", payment should be made
        in_transit_event = self.order.shipping_events.create(
            event_type=ShippingEventType.objects.get(code="in transit"), group=1)
        for line in self.order.lines.all():
            in_transit_event.line_quantities.create(line=line, quantity=line.quantity)
        return shipped_event

    def create_shipping_paid_payment_event(self, shipped_event):
        shipping_paid_event = self.order.payment_events.create(
            event_type=PaymentEventType.objects.get(code="paid_shipping"),
            amount=3.00, shipping_event=shipped_event, group=1)
        for line in self.order.lines.all():
            shipping_paid_event.line_quantities.create(
                line=line, quantity=line.quantity)

    def test_payout_on_one_full_order(self):

        shipped_event = self.create_shipping_events()

        self.create_shipping_paid_payment_event(shipped_event)

        self.assertEqual(len(PaymentEvent.objects.all()), 1, "1 payment should exist for the payment of shipping")

        pay_designers()

        self.assertEqual(len(PaymentEvent.objects.all()), 2,
                      "Another payment event should exist showing that the 1 shipping event was paid out")

        # There should be 1 payment event since there was only 1 shipped package to payout
        designer_payment_event = PaymentEvent.objects.get(event_type=PaymentEventType.objects.get(code="paid_designer"))
        self.assertEqual(
            designer_payment_event.group, 1, "Designer payment event should be of the same group as the shipping paid event")

        self.assertAlmostEqual(
            designer_payment_event.amount,
            Decimal(6.29),
            places=2,
            msg="The amount paid should be the item amount minus shipping and tinville fees")

        designer_payout = DesignerPayout.objects.all()[0]
        self.assertEqual(len(DesignerPayout.objects.all()), 1, "Designer payout should be recorded for this period")
        self.assertAlmostEqual(
            designer_payout.amount,
            Decimal(6.29),
            places=2)


        # Make sure all designer payment events are linked to the designer payout record
        self.assertEqual(designer_payment_event.reference, str(designer_payout.id), "Designer payment event should reference aggegate designer payout record")

        # Confirm info in Stripe is as expected
        stripe_transfer = self.stripe.Transfer.retrieve(designer_payout.reference)
        self.assertEqual((designer_payout.amount * 100), stripe_transfer.amount)
        self.assertEqual(self.user.recipient_id, stripe_transfer.recipient)

    def test_no_payout_if_shipping_not_paid(self):
        self.create_shipping_events()
        self.assertEqual(len(PaymentEvent.objects.all()), 0, "0 payments should exist since shipping not paid")

        pay_designers()

        self.assertEqual(len(PaymentEvent.objects.all()), 0, "0 payments should exist since shipping not paid")
        self.assertEqual(len(DesignerPayout.objects.all()), 0, "Designer payout should not be recorded for this period")

    def test_no_payout_if_payment_already_made(self):
        self.test_payout_on_one_full_order()

        self.assertEqual(len(PaymentEvent.objects.all()), 2)
        self.assertEqual(len(DesignerPayout.objects.all()), 1, "1 payout should exist for first payout")

        pay_designers()

        self.assertEqual(len(PaymentEvent.objects.all()), 2, "No new payment events should exist")
        self.assertEqual(len(DesignerPayout.objects.all()), 1, "No new payouts should exist")


    def test_no_payout_due_to_no_stripe_recipient_id_for_designer(self):
        shipped_event = self.create_shipping_events()
        self.create_shipping_paid_payment_event(shipped_event)

        self.assertEqual(len(PaymentEvent.objects.all()), 1)

        self.user.recipient_id = ''
        self.user.save()

        pay_designers()

        self.assertEqual(len(PaymentEvent.objects.all()), 1, "No new payments should exist since the user has no stripe info")
        self.assertEqual(len(DesignerPayout.objects.all()), 0, "Designer payout should not be recorded for this period")

    # def test_partial_payout_of_order(self):
    #     pass
    #
    # def test_payout_then_another_pay_period_does_not_pay_again(self):
    #     pass
    #
    # def test_multiple_payouts_if_multiple_orders_between_pay_periods(self):
    #     pass

    # def test_transaction_is_rolled_back_on_exception(self):
    #     pass

