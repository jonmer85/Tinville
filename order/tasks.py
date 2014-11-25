from collections import defaultdict
import logging
from celery import task
from designer_shop.models import Shop
from django.conf import settings
from django.db.models import Q
from order.utils import get_designer_payout_amount
from oscar.core.loading import get_model
import stripe


PaymentEvent = get_model('order', 'PaymentEvent')
ShippingEvent = get_model('order', 'ShippingEvent')
ShippingEventType = get_model('order', 'ShippingEventType')
PaymentEventType = get_model('order', 'PaymentEventType')
Order = get_model('order', 'Order')

logger = logging.getLogger(__name__)

@task
def pay_designers():
    # Get all shipping events that are in transit or received
    potential_payments = ShippingEvent.objects.filter(event_type__code='in transit')

    # Remove all payments that have been paid already
    potential_payment_ids = [p.id for p in potential_payments]
    payments_made = PaymentEvent.objects.filter(shipping_event__in=potential_payment_ids)
    payments_to_make = potential_payments.exclude(id__in=payments_made).select_related('order')

    # Group payments to make by designer
    payments_by_designer = defaultdict(list)
    pay_designer_event = PaymentEventType.objects.get(code="paid_designer")
    for payment in payments_to_make.order_by('order__number'):
        shop_id = int(payment.order.number[0:payment.order.number.find("-")])
        designer = Shop.objects.get(id=shop_id).user
        payments_by_designer[designer].append(payment)

    for designer in payments_by_designer.keys():
        try:
            amount_to_pay = 0.0
            for shipping_event in payments_by_designer[designer]:
                for line in shipping_event.lines:
                    amount_to_pay += line.line_price_incl_tax

                    # There should be a payment event for the shipping paid for this line
                    shipping_payment_event = \
                        PaymentEvent.objects.get(Q(shipping_event=line.id) &
                                                 Q(event_type=ShippingEventType.objects.get(code="paid_shipping")))

                    # Deduct the shipping cost
                    amount_to_pay -= shipping_payment_event.amount

                    # Deduct our sales cut
                    amount_to_pay = get_designer_payout_amount(amount_to_pay)

            # Transfer the amount to designer's Stripe account
            stripe.api_key = settings.STRIPE_SECRET_KEY

            result = stripe.Transfer.create(
              amount=amount_to_pay,
              currency="usd",
              recipient=designer.recipient_id,
              description=("Payout to designer (%s)", designer)
            )
            logger.debug(result)

            # Now create a payment event to mark that the designer has been paid for these shipping events
            for shipping_event in payments_by_designer[designer]:
                paid_designer_event = shipping_event.order.payment_events.create(
                    event_type=PaymentEventType.objects.get(code="paid_designer"), reference=result.id)

                paid_designer_event.lines = shipping_event.lines
                paid_designer_event.save()


        except Exception as e:
            logger.error(
                "Unhandled exception while paying designer (%s) payment (%s)",
                designer, e, exc_info=True)
            logger.error("Unable to pay designer due to unknown error")


