from collections import defaultdict
import logging
from decimal import Decimal
from celery import task
from designer_shop.models import Shop
from user.models import TinvilleUser
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from common.utils import get_designer_payout_amount, get_promoter_payout_amount
from oscar.core.loading import get_model
import stripe
from user.models import DesignerPayout
from user.models import PromoterPayout


PaymentEvent = get_model('order', 'PaymentEvent')
ShippingEvent = get_model('order', 'ShippingEvent')
ShippingEventType = get_model('order', 'ShippingEventType')
PaymentEventType = get_model('order', 'PaymentEventType')
Order = get_model('order', 'Order')

logger = logging.getLogger(__name__)

@task
def pay_designers():
    # Get all shipping events that are in transit or received
    potential_payments = ShippingEvent.objects.filter(event_type__code='in_transit')

    # Remove all payments that have been paid already
    potential_payment_ids = [p.id for p in potential_payments]
    payments_made = PaymentEvent.objects.filter(shipping_event__in=potential_payment_ids) \
        .filter(event_type=PaymentEventType.objects.get(code="paid_designer"))
    payments_to_make = potential_payments.exclude(group__in=[p.group for p in payments_made]).select_related('order')

    # Group payments to make by designer
    payments_by_designer = defaultdict(list)
    for payment in payments_to_make.order_by('order__number'):
        shop_id = int(payment.order.number[0:payment.order.number.find("-")])
        designer = Shop.objects.get(id=shop_id).user
        payments_by_designer[designer].append(payment)

    for designer in payments_by_designer.keys():
        try:
            # This is done within a DB transaction so any payment events created are rolled back if there is any exception
            with transaction.atomic():
                amount_to_payout = Decimal(0.0)

                # Create a Designer Payout record to mark the total amount paid
                payout = DesignerPayout.objects.create(designer=designer, amount=0.00)

                for in_transit_event in payments_by_designer[designer]:
                    amount_to_pay_for_shipping_event = Decimal(0.0)
                    for line, quantity in zip(in_transit_event.lines.all(), in_transit_event.line_quantities.all()):
                        amount_to_pay_for_shipping_event += line.unit_price_excl_tax * quantity.quantity

                    # There should be a payment event for the shipping paid for this line

                    # Get the "Shipped" event that caused the payment event, it should have the same group id as our
                    # "In transit" event
                    shipped_event = \
                        ShippingEvent.objects.get(Q(group=in_transit_event.group) &
                                                  Q(event_type=ShippingEventType.objects.get(code="shipped")))

                    shipping_payment_event = \
                        PaymentEvent.objects.get(Q(shipping_event=shipped_event.id) &
                                                 Q(event_type=PaymentEventType.objects.get(code="paid_shipping")))

                    # Deduct the shipping cost
                    amount_to_pay_for_shipping_event -= shipping_payment_event.amount

                    # Deduct our sales cut
                    amount_to_pay_for_shipping_event = get_designer_payout_amount(amount_to_pay_for_shipping_event)

                    # Add this to the total payout
                    amount_to_payout += amount_to_pay_for_shipping_event

                    # Now create a payment event to mark that the designer has been paid for these shipping events
                    paid_designer_event = in_transit_event.order.payment_events.create(
                        amount=amount_to_pay_for_shipping_event, group=shipping_payment_event.group,
                        event_type=PaymentEventType.objects.get(code="paid_designer"), reference=payout.id,
                        shipping_event=in_transit_event)
                    for line in in_transit_event.order.lines.all():
                        paid_designer_event.line_quantities.create(
                            line=line, quantity=line.quantity)

                # Transfer the amount to designer's Stripe account
                stripe.api_key = settings.STRIPE_SECRET_KEY

                if designer.account_token.startswith('ba_'):
                    result = stripe.Transfer.create(
                      amount=int(amount_to_payout * 100),  # Amount expected in cents
                      currency="usd",
                      recipient=designer.recipient_id,
                      description="Payout to designer %s " % designer,
                      bank_account=designer.account_token
                    )
                    logger.debug(result)
                    # And save the payout record with the stripe reference
                    payout.reference = result.id
                    payout.amount = amount_to_payout
                    payout.save()
                else:
                    result = stripe.Transfer.create(
                      amount=int(amount_to_payout * 100),  # Amount expected in cents
                      currency="usd",
                      recipient=designer.recipient_id,
                      description="Payout to designer %s " % designer,
                      card=designer.account_token
                    )
                    logger.debug(result)
                    # And save the payout record with the stripe reference
                    payout.reference = result.id
                    payout.amount = amount_to_payout
                    payout.save()

        except Exception as e:
            logger.error(
                "Unhandled exception while paying designer (%s) payment (%s)",
                designer, e, exc_info=True)
#

@task
def pay_promoters():
    # Get all shipping events that are in transit or received
    potential_payments = ShippingEvent.objects.filter(event_type__code='in_transit')

    # Remove all payments that have been paid already
    potential_payment_ids = [p.id for p in potential_payments]
    payments_made = PaymentEvent.objects.filter(shipping_event__in=potential_payment_ids) \
        .filter(event_type=PaymentEventType.objects.get(code="paid_promoter"))
    payments_to_make = potential_payments.exclude(group__in=[p.group for p in payments_made]).select_related('order')

    # Group payments to make by designer
    payments_by_promoter = defaultdict(list)
    for payment in payments_to_make.order_by('order__number'):
        promoter = payment.order.promoter
        payments_by_promoter[promoter].append(payment)

    for promoter in payments_by_promoter.keys():
        if promoter.promoter_balance >= settings.TINVILLE_PROMOTER_MINIMUM_PAYOUT:
            try:
                with transaction.atomic():
                    amount_to_payout = Decimal(0.0)

                    # Create a Promoter Payout record to mark the total amount paid
                    payout = PromoterPayout.objects.create(promoter=promoter, amount=0.00)

                    for in_transit_event in payments_by_promoter[promoter]:
                        amount_to_pay_for_shipping_event = Decimal(0.0)
                        for line, quantity in zip(in_transit_event.lines.all(), in_transit_event.line_quantities.all()):
                            amount_to_pay_for_shipping_event += line.unit_price_excl_tax * quantity.quantity

                        # Get the "Shipped" event that caused the payment event, it should have the same group id as our
                        # "In transit" event
                        shipped_event = \
                            ShippingEvent.objects.get(Q(group=in_transit_event.group) &
                                                      Q(event_type=ShippingEventType.objects.get(code="shipped")))

                        shipping_payment_event = \
                            PaymentEvent.objects.get(Q(shipping_event=shipped_event.id) &
                                                     Q(event_type=PaymentEventType.objects.get(code="paid_shipping")))

                        # Get 3%
                        amount_to_pay_for_shipping_event = get_promoter_payout_amount(amount_to_pay_for_shipping_event)

                        amount_to_payout += amount_to_pay_for_shipping_event

                        # Now create a payment event to mark that the promoter has been paid for these shipping events
                        paid_promoter_event = in_transit_event.order.payment_events.create(
                            amount=amount_to_pay_for_shipping_event, group=shipping_payment_event.group,
                            event_type=PaymentEventType.objects.get(code="paid_promoter"), reference=payout.id,
                            shipping_event=in_transit_event)
                        for line in in_transit_event.order.lines.all():
                            paid_promoter_event.line_quantities.create(
                                line=line, quantity=line.quantity)

                    # Transfer the amount to promoter's Stripe account
                    stripe.api_key = settings.STRIPE_SECRET_KEY

                    if promoter.account_token.startswith('ba_'):
                        result = stripe.Transfer.create(
                          amount=int(amount_to_payout * 100),  # Amount expected in cents
                          currency="usd",
                          recipient=promoter.recipient_id,
                          description="Payout to promoter %s " % promoter,
                          bank_account=promoter.account_token
                        )
                        logger.debug(result)
                        # And save the payout record with the stripe reference
                        payout.reference = result.id
                        payout.amount = amount_to_payout
                        payout.save()
                    else:
                        result = stripe.Transfer.create(
                          amount=int(amount_to_payout * 100),  # Amount expected in cents
                          currency="usd",
                          recipient=promoter.recipient_id,
                          description="Payout to promoter %s " % promoter,
                          card=promoter.account_token
                        )
                        logger.debug(result)
                        # And save the payout record with the stripe reference
                        payout.reference = result.id
                        payout.amount = amount_to_payout
                        payout.save()

                    # if we pay the promoter, reset their estimated balance
                    promoter.promoter_balance = 0.00
                    promoter.save()

            except Exception as e:
                logger.error(
                    "Unhandled exception while paying promoter (%s) payment (%s)",
                    promoter, e, exc_info=True)