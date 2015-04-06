from django.db.models import Max
from oscar.apps.order import processing
from oscar.apps.payment import exceptions
from oscar.core.loading import get_model, get_class
from django.conf import settings
from custom_oscar.apps.order.exceptions import *
import logging

# from .models import PaymentEventType
from decimal import Decimal as D
from user.models import TinvilleUser

SHIPPED = 'Shipped'
PARTIALLY_SHIPPED = 'Partially Shipped'
Partner = get_model('partner', 'Partner')
PartnerAddress = get_model('partner', 'PartnerAddress')
ShippingEvent = get_model('order', 'ShippingEvent')
ShippingEventType = get_model('order', 'ShippingEventType')
PaymentEventType = get_model('order', 'PaymentEventType')
logger = logging.getLogger(__name__)
CommunicationEventType = get_model('customer', 'CommunicationEventType')
Dispatcher = get_class('customer.utils', 'Dispatcher')
DESIGNER_PROCESSING_ORDER = 'DESIGNER_PROCESSING_ORDER'
ORDER_IN_TRANSIT = 'ORDER_IN_TRANSIT'

class EventHandler(processing.EventHandler):
    def handle_shipping_event(self, order, event_type, lines,
                              line_quantities, request, response, shipment_info, **kwargs):
        self.validate_shipping_event(
            order, event_type, lines, line_quantities, **kwargs)

        payment_event = None

        group = None

        if event_type.name == SHIPPED:
            max_query = ShippingEvent.objects.all().aggregate(Max('group'))['group__max']
            group = (max_query + 1) if max_query is not None else 0

            self.consume_stock_allocations(
                order, lines, line_quantities)
            for line, quantity in zip(lines, line_quantities):
                if SHIPPED in line.shipping_event_breakdown:
                    if line.shipping_event_breakdown[SHIPPED]["quantity"] + quantity == line.quantity:
                        line.set_status(SHIPPED)
                    else:
                        line.set_status(PARTIALLY_SHIPPED)
                else:
                    if line.quantity == quantity:
                        line.set_status(SHIPPED)
                    else:
                        line.set_status(PARTIALLY_SHIPPED)
            if all(line.status == SHIPPED for line in lines):
                order.set_status(SHIPPED)
            else:
                order.set_status(PARTIALLY_SHIPPED)

            # if they are shipping, they should have payed for shipping (at least for now).. create that payment event here..
            # TODO add support here for shipping not using easypost (aka.. ignore this next section)
            payment_event_type = PaymentEventType._default_manager.get(code='paid_shipping')
            parcel_cost = shipment_info['rate']
            payment_event = self._create_payment_event(order, payment_event_type, parcel_cost, lines, line_quantities,
                                                       group)
            order.shipping_excl_tax += D(parcel_cost)
            order.save()

        shipping_event = self._create_shipping_event(
            order, event_type, lines, line_quantities, shipment_info, group,
            kwargs.get('reference', None))

        designerId = ExtractDesignerIdFromOrderId(order.number)
        designer = TinvilleUser.objects.get(id=designerId)

        self._send_notifications(order, DESIGNER_PROCESSING_ORDER,
                                 {
                                     'shop_name': Shop.objects.get(user=designer).name,
                                     'order': order
                                 })

        # If there was a payment event created before the shipment event, attach these events
        if payment_event != None:
            payment_event.shipping_event = shipping_event
            payment_event.save()

    def _create_shipping_event(self, order, event_type, lines, line_quantities, shipment_info, group,
                               ref):
        shipping_event = self.create_shipping_event(
            order, event_type, lines, line_quantities,
            reference=ref)
        shipping_event.label_url = shipment_info["labelUrl"]
        shipping_event.tracking_code = shipment_info["tracking"]
        shipping_event.group = group

        shipping_event.save()
        return shipping_event
        # add to the shipping costs of the order

    def create_inTransit_event(self, tracking_code, carrier):
        try:
            isIntransit = ShippingEvent.objects.get(event_type=ShippingEventType.objects.get(code="in_transit"),
                                                    tracking_code=tracking_code)
        except ShippingEvent.DoesNotExist:
            try:
                shipping_event = ShippingEvent.objects.get(event_type=ShippingEventType.objects.get(code="shipped"),
                                                           tracking_code=tracking_code)

                shipping_event_intransit = ShippingEvent.objects.create(order=shipping_event.order,
                                                                        event_type=ShippingEventType.objects.get(
                                                                            code="in_transit"),
                                                                        reference=shipping_event.reference,
                                                                        group=shipping_event.group,
                                                                        tracking_code=shipping_event.tracking_code,
                                                                        notes=" ")
                shipping_event_intransit.save()
                for line in shipping_event.lines.all():
                    shipping_event_intransit.line_quantities.create(line=line, quantity=line.quantity)

                designerId = ExtractDesignerIdFromOrderId(shipping_event.order.number)
                designer = TinvilleUser.objects.get(id=designerId)
                self._send_notifications(shipping_event.order, ORDER_IN_TRANSIT,
                    {
                        'shop_name': Shop.objects.get(user=designer).name,
                         'order': shipping_event.order
                    })

            except ShippingEvent.DoesNotExist:
                logger.error("Shipped event does not exist")

    def _create_payment_event(self, order, event_type, amount, lines, line_quantities, group):
        payment_event = self.create_payment_event(order, event_type, amount, lines, line_quantities)
        payment_event.group = group
        payment_event.save()
        return payment_event

    def _send_notifications(self, order, code, context):
        messages = CommunicationEventType.objects.get_and_render(
            code, context)
        event_type = CommunicationEventType.objects.get(code=code)

        if messages and messages['body']:
            dispatcher = Dispatcher(logger)
            dispatcher.dispatch_order_messages(order, messages, event_type)


