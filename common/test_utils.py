from oscar.core.loading import get_model

ShippingEventType = get_model('order', 'ShippingEventType')
Order = get_model('order', 'Order')

def create_in_transit_event(order_num, event_group, lines=None):

        order = Order.objects.get(number=order_num)

        # Event marked as "in transit", payment should be made
        in_transit_event = order.shipping_events.create(
            event_type=ShippingEventType.objects.get(code="in_transit"), group=event_group)
        if lines:
            for line in lines.all():
                in_transit_event.line_quantities.create(line=line, quantity=line.quantity)
        else:
            # No specified lines, use all lines from the order
            for line in order.lines.all():
                in_transit_event.line_quantities.create(line=line, quantity=line.quantity)