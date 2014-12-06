from oscar.apps.order import processing
from oscar.apps.payment import exceptions

# from .models import PaymentEventType


class EventHandler(processing.EventHandler):

    def handle_shipping_event(self, order, event_type, lines,
                              line_quantities, **kwargs):
        self.validate_shipping_event(
            order, event_type, lines, line_quantities, **kwargs)

        payment_event = None

        if event_type.name == 'Shipped':
            self.consume_stock_allocations(
                order, lines, line_quantities)
            for line, quantity in zip(lines, line_quantities):
                if "Shipped" in line.shipping_event_breakdown:
                    if line.shipping_event_breakdown["Shipped"]["quantity"] + quantity == line.quantity:
                        line.set_status("Shipped")
                    else:
                        line.set_status("Partially Shipped")
                else:
                    if line.quantity == quantity:
                        line.set_status("Shipped")
                    else:
                        line.set_status("Partially Shipped")

        shipping_event = self.create_shipping_event(
            order, event_type, lines, line_quantities,
            reference=kwargs.get('reference', None))
