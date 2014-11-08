from oscar.apps.order import processing
from oscar.apps.payment import exceptions
from oscar.core.loading import get_model
from django.conf import settings
import easypost
# from .models import PaymentEventType

Partner = get_model('partner', 'Partner')
PartnerAddress = get_model('partner', 'PartnerAddress')

class EventHandler(processing.EventHandler):
    easypost.api_key = settings.EASYPOST_API_KEY

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
        if event_type.name == 'Boxed':
            self.CreateShipping(self, **kwargs)

        shipping_event = self.create_shipping_event(
            order, event_type, lines, line_quantities,
            reference=kwargs.get('reference', None))

    def CreateShipping(self, **kwargs):

        from_address = self.GetShopAddress()

        order = self.get_object()
        to_address = order.shipping.address

        parcel = easypost.Parcel.create(
            predefined_package = 'FlatRateEnvelope',
            weight = 10
        )

        shipment = easypost.Shipment.create(
            to_address=to_address,
            from_address=from_address,
            parcel=parcel
        )

        #TODO: validate shipment response try catch?
        return shipment

    def _GetShopAddress(self):
        partners = Partner._default_manager.filter(users=self.request.user)
        #do something with this broken logic...
        for partner in partners:
            shop_address = partner.addresses.instance.primary_address
            if(shop_address == None):
                #reroute to ShopAddress page
                hello = 2
            return shop_address
