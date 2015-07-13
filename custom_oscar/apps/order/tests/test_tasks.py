from decimal import Decimal

from django.conf import settings
from django.db.models import Max
from django.db.models.query_utils import Q
from django.test import TestCase
from oscar.core.loading import get_model
import stripe

from designer_shop.models import Shop
from custom_oscar.apps.order.tasks import pay_designers
from common.factories import create_order, create_product, create_basket_with_products, create_basket
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

        # token = self.stripe.Token.create(
        #     {
        #         'number': '4000056655665556',
        #         'exp_month': '12',
        #         'exp_year': '2030',
        #         'cvc': '123'
        #     }
        # )
        result = self.stripe.Recipient.create(
                name="Joe Schmoe",
                type="individual",
                card = {
                    'number': '4000056655665556',
                    'exp_month': '12',
                    'exp_year': '2030',
                    'cvc': '123'
                }
        )

        self.user.recipient_id = result.id
        self.user.account_token = result.default_card
        self.user.save()

        self.shop = Shop.objects.create(name='SchmoeVille', user=self.user)

        self.assertEqual(len(PaymentEvent.objects.all()), 0, "No payments should exist")
        self.assertEqual(len(DesignerPayout.objects.all()), 0, "No designer payout should be recorded yet")

    def tearDown(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if self.user.recipient_id:
            rp = stripe.Recipient.retrieve(self.user.recipient_id)
            rp.delete()

    def test_no_designers_to_pay(self):
        self.order = create_order(number="2-10001", user=self.user, shop=self.shop)

        pay_designers()
        self.assertEqual(len(PaymentEvent.objects.all()), 0,
                      "No payments should exist since there were no shipping events from any designer")

    def test_no_payout_if_shipped_but_not_in_transit(self):
        self.order = create_order(number="2-10001", user=self.user, shop=self.shop)

        # Event marked as shipped, but not in transit, no payment made
        shipped_event = self.order.shipping_events.create(
            event_type=ShippingEventType.objects.get(code="shipped"), group=0)

        for line in self.order.lines.all():
            shipped_event.line_quantities.create(line=line, quantity=line.quantity)

        pay_designers()

        self.assertEqual(len(PaymentEvent.objects.all()), 0,
                      "No payments should exist since there were no 'in transit' events from any designer")


    def create_shipping_events(self, lines=None, line_quantities=None):
        max_query = ShippingEvent.objects.all().aggregate(Max('group'))['group__max']
        group = (max_query+1) if max_query is not None else 0
        shipped_event = self.order.shipping_events.create(
            event_type=ShippingEventType.objects.get(code="shipped"), group=group)
        if lines and line_quantities:
            for line, quantity in zip(lines, line_quantities):
                shipped_event.line_quantities.create(line=line, quantity=quantity)
        else:
            # No specified lines, use all lines from the order
            for line in self.order.lines.all():
                shipped_event.line_quantities.create(line=line, quantity=line.quantity)


        # Event marked as "in transit", payment should be made
        in_transit_event = self.order.shipping_events.create(
            event_type=ShippingEventType.objects.get(code="in_transit"), group=shipped_event.group)
        if lines and line_quantities:
            for line, quantity in zip(lines, line_quantities):
                in_transit_event.line_quantities.create(line=line, quantity=quantity)
        else:
            # No specified lines, use all lines from the order
            for line in self.order.lines.all():
                in_transit_event.line_quantities.create(line=line, quantity=line.quantity)
        return shipped_event, in_transit_event

    def create_shipping_paid_payment_event(self, shipped_event, price, lines, line_quantities):
        shipping_paid_event = self.order.payment_events.create(
            event_type=PaymentEventType.objects.get(code="paid_shipping"),
            amount=price, shipping_event=shipped_event, group=shipped_event.group)
        if lines and line_quantities:
            for line, quantity in zip(lines, line_quantities):
                shipping_paid_event.line_quantities.create(line=line, quantity=quantity)
        else:
            # No specified lines, use all lines from the order
            for line in self.order.lines.all():
                shipping_paid_event.line_quantities.create(
                    line=line, quantity=line.quantity)

    def assert_proper_payment_events(self, total_payment_events, payment_event_group, payout_total):
        self.assertEqual(len(PaymentEvent.objects.all()), total_payment_events,
                         "Another payment event should exist showing that the 1 shipping event was paid out")
        # There should be 1 payment event since there was only 1 shipped package to payout
        designer_payment_event = PaymentEvent.objects.get(
            Q(event_type=PaymentEventType.objects.get(code="paid_designer")) &
            Q(group=payment_event_group))
        self.assertEqual(
            designer_payment_event.group, payment_event_group,
            "Designer payment event should be of the same group as the shipping paid event")
        self.assertAlmostEqual(
            designer_payment_event.amount,
            Decimal(payout_total),
            places=2,
            msg="The amount paid should be the item amount minus shipping and tinville fees. expected: " + str(designer_payment_event.amount) + " actual: " + str(payout_total))
        return designer_payment_event

    def assert_proper_payout_records(self, total_payout_records, payment_event_ref, payout_total):
        designer_payout = DesignerPayout.objects.get(id=payment_event_ref)
        self.assertEqual(len(DesignerPayout.objects.all()), total_payout_records)
        self.assertAlmostEqual(
            designer_payout.amount,
            Decimal(payout_total),
            places=2)
        return designer_payout


    def assert_proper_stripe_records(self, designer_payout):
        stripe_transfer = self.stripe.Transfer.retrieve(designer_payout.reference)
        self.assertEqual((designer_payout.amount * 100), stripe_transfer.amount)
        self.assertEqual(self.user.recipient_id, stripe_transfer.recipient)

    def test_payout_on_one_full_order(self):
        self.order = create_order(number="2-10001", user=self.user, shop=self.shop)
        shipped_event, in_transit_event = self.create_basic_shipping_and_payment_events()

        pay_designers()

        designer_payment_event = self.assert_proper_payment_events(
            total_payment_events=2, payment_event_group=in_transit_event.group, payout_total=5.60)

        designer_payout = self.assert_proper_payout_records(
            total_payout_records=1, payment_event_ref=designer_payment_event.reference, payout_total=5.60)

        self.assert_proper_stripe_records(designer_payout)

    def test_payout_on_one_full_order_bank_account(self):
        self.order = create_order(number="2-10001", user=self.user, shop=self.shop)
        shipped_event, in_transit_event = self.create_basic_shipping_and_payment_events()
        rp = stripe.Recipient.retrieve(self.user.recipient_id)
        rp.bank_account = \
            {
                'country': 'US',
                'currency': 'USD',
                'account_number': '000123456789',
                'routing_number': '110000000'
            }
        rp.save()

        rt = stripe.Recipient.retrieve(self.user.recipient_id)
        self.user.account_token = rt.active_account.id
        self.user.save()

        pay_designers()

        designer_payment_event = self.assert_proper_payment_events(
            total_payment_events=2, payment_event_group=in_transit_event.group, payout_total=5.60)

        designer_payout = self.assert_proper_payout_records(
            total_payout_records=1, payment_event_ref=designer_payment_event.reference, payout_total=5.60)

        self.assert_proper_stripe_records(designer_payout)

    def test_no_payout_if_shipping_not_paid(self):
        self.order = create_order(number="2-10001", user=self.user, shop=self.shop)
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


    def create_basic_shipping_and_payment_events(self, shipping_price=3.00, lines=None, line_quantities=None):
        shipped_event, in_transit_event = self.create_shipping_events(lines, line_quantities)
        self.create_shipping_paid_payment_event(shipped_event, shipping_price, lines, line_quantities)
        return shipped_event, in_transit_event

    def test_no_payout_due_to_no_stripe_recipient_id_for_designer(self):
        self.user.recipient_id = ''
        self.user.save()
        self.order = create_order(number="2-10001", user=self.user, shop=self.shop)
        self.create_basic_shipping_and_payment_events()


        pay_designers()

        # Make sure the exception rolled back any payment and payout events caused
        with self.assertRaises(PaymentEvent.DoesNotExist):
            PaymentEvent.objects.get(event_type=PaymentEventType.objects.get(code="paid_designer"))
        self.assertEquals(len(DesignerPayout.objects.all()), 0)



    def test_payout_of_partial_order_full_line_item(self):

        # Create an order with two line items, but only ship one
        products = [
            create_product(title="Graphic T", product_class="Shirts", price=20.00,
                           num_in_stock=5, partner_users=[self.user], shop=self.shop),
            create_product(title="Fancy pants", product_class="Bottoms", price=40.00,
                           num_in_stock=10, partner_users=[self.user], shop=self.shop)
        ]

        self.order = create_order(number="2-10001", basket=create_basket_with_products(products),
                                  user=self.user, shop=self.shop)

        # Designer only shipped first item
        first_item = self.order.lines.get(product=products[0])
        shipped_event, in_transit_event = \
            self.create_basic_shipping_and_payment_events(
                shipping_price=5.00, lines=[first_item], line_quantities=[first_item.quantity])

        pay_designers()

        designer_payment_event = self.assert_proper_payment_events(
            total_payment_events=2, payment_event_group=in_transit_event.group, payout_total=12.00)

        designer_payout = self.assert_proper_payout_records(
            total_payout_records=1, payment_event_ref=designer_payment_event.reference, payout_total=12.00)

        self.assert_proper_stripe_records(designer_payout)

        # Now ship the next item and pay the designers again
        second_item = self.order.lines.get(product=products[1])
        shipped_event2, in_transit_event2 = \
            self.create_basic_shipping_and_payment_events(
                shipping_price=10.00, lines=[second_item], line_quantities=[second_item.quantity])

        pay_designers()

        designer_payment_event2 = self.assert_proper_payment_events(
            total_payment_events=4, payment_event_group=in_transit_event2.group, payout_total=24.00)

        designer_payout2 = self.assert_proper_payout_records(
            total_payout_records=2, payment_event_ref=designer_payment_event2.reference, payout_total=24.00)

        self.assert_proper_stripe_records(designer_payout2)

    def test_payout_of_partial_order_partial_quantity_line_item(self):
        # Create an order with two line items, but ship only the partial quantities of both
        products = [
            create_product(title="Graphic T", product_class="Shirts", price=20.00,
                           num_in_stock=5, partner_users=[self.user], shop=self.shop),
            create_product(title="Fancy pants", product_class="Bottoms", price=40.00,
                           num_in_stock=10, partner_users=[self.user], shop=self.shop)
        ]
        basket = create_basket(empty=True)
        basket.add_product(products[0], quantity=3)
        basket.add_product(products[1], quantity=4)

        self.order = create_order(number="2-10001", basket=basket,
                                  user=self.user, shop=self.shop)

        # Designer only shipped partial quantities of both items
        shipped_event, in_transit_event = \
            self.create_basic_shipping_and_payment_events(
                shipping_price=5.00, lines=self.order.lines.all(), line_quantities=[2, 3])

        pay_designers()

        designer_payment_event = self.assert_proper_payment_events(
            total_payment_events=2, payment_event_group=in_transit_event.group, payout_total=124.00)

        designer_payout = self.assert_proper_payout_records(
            total_payout_records=1, payment_event_ref=designer_payment_event.reference, payout_total=124.00)

        self.assert_proper_stripe_records(designer_payout)

        # Now ship the remaining quantities
        shipped_event2, in_transit_event2 = \
            self.create_basic_shipping_and_payment_events(
                shipping_price=5.00, lines=self.order.lines.all(), line_quantities=[1, 1])

        pay_designers()

        designer_payment_event2 = self.assert_proper_payment_events(
            total_payment_events=4, payment_event_group=in_transit_event2.group, payout_total=44.00)

        designer_payout2 = self.assert_proper_payout_records(
            total_payout_records=2, payment_event_ref=designer_payment_event2.reference, payout_total=44.00)

        self.assert_proper_stripe_records(designer_payout2)


    def test_payout_of_multiple_orders(self):
        self.order = create_order(number="2-10001", user=self.user, shop=self.shop)
        self.order = create_order(number="2-10002", user=self.user, shop=self.shop)
        self.order = create_order(number="2-10003", user=self.user, shop=self.shop)

        shipped_event, in_transit_event = self.create_basic_shipping_and_payment_events()

        pay_designers()

        designer_payment_event = self.assert_proper_payment_events(
            total_payment_events=2, payment_event_group=in_transit_event.group, payout_total=5.60)

        designer_payout = self.assert_proper_payout_records(
            total_payout_records=1, payment_event_ref=designer_payment_event.reference, payout_total=5.60)

        self.assert_proper_stripe_records(designer_payout)


    def test_multiple_payouts_if_orders_between_pay_periods(self):
        self.test_payout_on_one_full_order()
        self.assertEqual(len(PaymentEvent.objects.all()), 2)
        self.assertEqual(len(DesignerPayout.objects.all()), 1, "1 payout should exist for first payout")

        # Create another order and make sure it is paid in the next pay period
        self.order = create_order(number="2-10002", user=self.user, shop=self.shop)
        shipped_event, in_transit_event = self.create_basic_shipping_and_payment_events()

        pay_designers()

        designer_payment_event = self.assert_proper_payment_events(
            total_payment_events=4, payment_event_group=in_transit_event.group, payout_total=5.60)

        designer_payout = self.assert_proper_payout_records(
            total_payout_records=2, payment_event_ref=designer_payment_event.reference, payout_total=5.60)

        self.assert_proper_stripe_records(designer_payout)
