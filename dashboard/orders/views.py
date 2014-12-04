from django.core.cache import cache
from oscar.apps.dashboard.orders.views import *
from oscar.apps.dashboard.orders.views import OrderListView as CoreOrderListView
from oscar.apps.dashboard.orders.views import OrderDetailView as CoreOrderDetailView
from oscar.apps.dashboard.orders.views import LineDetailView as CoreLineDetailView
from oscar.apps.dashboard.orders.views import OrderStatsView as CoreOrderStatsView
from oscar.core.loading import get_model
from django.views.generic import View
from designer_shop.models import Shop
from order.exceptions import *
import json
import re
import easypost
import logging

Order = get_model('order', 'Order')
Partner = get_model('partner', 'Partner')
Line = get_model('order', 'Line')
logger = logging.getLogger(__name__)

def queryset_orders_for_user(user):
    """
    Returns a queryset of all orders that a user is allowed to access.
    A staff user may access all orders.
    To allow access to an order for a non-staff user, at least one line's
    partner has to have the user in the partner's list.
    """
    if user.is_staff:
        queryset = Order._default_manager.select_related(
        'billing_address', 'billing_address__country',
        'shipping_address', 'shipping_address__country',
        'user'
        ).prefetch_related('lines')
        return queryset.exclude(number__contains="-")
    else:
        partners = Partner._default_manager.filter(users=user)
        orderlines = Line.objects.filter(partner__in=partners)
        return Order.objects.filter(id__in=orderlines).distinct().filter(number__contains="-")

class OrderListView(CoreOrderListView):
    template_name = 'templates/dashboard/orders/order_list.html'

    def dispatch(self, request, *args, **kwargs):
        # base_queryset is equal to all orders the user is allowed to access
        self.set_base_queryset(request)
        return View.dispatch(self, request, *args, **kwargs)

    def set_base_queryset(self, request):
        self.base_queryset = queryset_orders_for_user(
            request.user).order_by('-date_placed')

class OrderDetailView(CoreOrderDetailView):
    template_name = 'templates/dashboard/orders/order_detail.html'
    easypost.api_key = settings.EASYPOST_API_KEY


    def create_shipping_event(self, request, order, lines, quantities):
        code = request.POST['shipping_event_type']
        try:
            event_type = ShippingEventType._default_manager.get(code=code)
        except ShippingEventType.DoesNotExist:
            messages.error(request, _("The event type '%s' is not valid")
                           % code)
            return self.reload_page_response()

        reference = request.POST.get('reference', None)
        response = HttpResponse()
        try:
            if event_type.name == 'Shipped':
                parcelType = request.POST.get('parcel_type', None)
                self.validate_parcel_type(parcelType)
                parcelType = {
                    'predefined_package' : parcelType,
                    'weight' : 10
                }
                shipment_info = self.post_specific_shipment(order, parcelType)

            EventHandler().handle_shipping_event(order, event_type, lines,
                                                 quantities, request, response, shipment_info,
                                                 reference=reference)
        except InvalidShippingEvent as e:
            messages.error(request,
                           _("Unable to create shipping event: %s") % e)
        except InvalidStatus as e:
            messages.error(request,
                           _("Unable to create shipping event: %s") % e)
        except PaymentError as e:
            messages.error(request, _("Unable to create shipping event due to"
                                      " payment error: %s") % e)
        except InvalidParcelType as e:
            messages.error(request, ("Unable to create shipping event due to"
                                      " unsupported Parcel Type: %s") % e)
        else:
            messages.success(request, ("Shipping event created"))
        return self.reload_page_response()

    def post_specific_shipment(self, order, parcelType):
        shipment = self.get_shipment(order, parcelType)
        try:
            shipment.buy(rate=shipment.lowest_rate(carriers=['USPS'], services=['Priority']))
        except Exception as e:
            logger.error(e)

        shipment_info = {
            "labelUrl": shipment.postage_label.label_url,
            "tracking": shipment.tracking_code,
            "rate": shipment.selected_rate.rate
        }

        return shipment_info

    def get_context_data(self, **kwargs):
        ctx = super(OrderDetailView, self).get_context_data(**kwargs)
        try:
            order = kwargs['object']
            ctx['box_types'] = self.get_shipment_context(order)
            ctx['box_types_json'] = json.dumps(ctx['box_types'])
        except ValueError as e:
            #NOTE: If get shipment context fails we return empty box types
            ctx['box_types'] = []
            ctx['box_types_json'] = []
        return ctx

    def get_shipment_context(self, order):
        shipment_collection = []
        if cache.get('parcel_types') == None:
            for parcel_type in self.get_supported_parcel_types():
                parcelType = { 'predefined_package': parcel_type,
                               'weight': 10 }
                shipment_collection.append(self.get_specific_shipment(order, parcelType))
            cache.set('parcel_types', shipment_collection, 60)
            return shipment_collection
        else:
            return cache.get('parcel_types')

    def get_shipment(self, order, parcelType):
        from_address = self._GetShopAddress(order.number)
        to_address = self._EasyPostAddressFormatter(order.shipping_address)
        try:
            shipment = easypost.Shipment.create(
                to_address=to_address,
                from_address=from_address,
                parcel=parcelType
            )
        except Exception as e:
            logger.error(e)
            raise Exception('Failed to retrieve Shipment Information')
        if (shipment == None):
            logger.error("Shipment is empty")
            raise Exception('Failed to retrieve Shipment Information')
        if (shipment.parcel == None):
            logger.error("Parcel is empty")
            raise Exception('Failed to retrieve Shipment Information')
        if (shipment.parcel.predefined_package == None):
            logger.error("Parcel type is empty")
            raise Exception('Failed to retrieve Shipment Information')
        if (shipment.rates == None):
            logger.error("Shipping rates is empty")
            raise Exception('Failed to retrieve Shipment Information')
        return shipment

    def get_specific_shipment(self, order, parcelType):

        shipment = self.get_shipment(order, parcelType)

        rates = []
        for current in range(0, len(shipment.rates)):
            #NOTE: Only append priority service
            if(shipment.rates[current].service == 'Priority'):
                rate = {
                    'carrier': shipment.rates[current].carrier,
                    'rate': shipment.rates[current].rate,
                    'service': shipment.rates[current].service
                }
                rates.append(rate)

        basic_shipment = {'type': shipment.parcel.predefined_package,
                          'name': re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', shipment.parcel.predefined_package).replace('Flat Rate','Flat-Rate'),
                          'rates' : rates}
        return basic_shipment

    def get_supported_parcel_types(self):
        return ['FlatRateEnvelope', 'FlatRatePaddedEnvelope',
                'SmallFlatRateBox', 'MediumFlatRateBox',
                'LargeFlatRateBox']

    def validate_parcel_type(self, parcel_type):
        if parcel_type not in self.get_supported_parcel_types():
            msg = (parcel_type)
            raise InvalidParcelType(msg)

    def _GetShopAddress(self,orderId):

        shopIdMatch = re.search('^([0-9]+)',orderId)
        shopId = shopIdMatch.group()
        shop = Shop.objects.get(pk=shopId)
        userId = shop.user.id

        partners = Partner._default_manager.filter(users=userId)
        if(partners == None or len(partners) == 0):
            raise ValueError("Partners Address is empty")

        shop_address = self._EasyPostAddressFormatter(partners[0].addresses.instance.primary_address)
        return shop_address

    def _EasyPostAddressFormatter(self, address):

        if(address == None):
            raise ValueError("Address is Empty.")
        #TODO check for multiple Address Lines
        _address = {
            'name': address.name,
            'street1': address.line1,
            'city': address.city,
            'state': address.state,
            'zip': address.postcode
        }
        return _address


class LineDetailView(CoreLineDetailView):
    template_name = 'templates/dashboard/orders/line_detail.html'

class OrderStatsView(CoreOrderStatsView):
    template_name = 'templates/dashboard/orders/statistics.html'

    def get_stats(self, filters):
        orders = queryset_orders_for_user(self.request.user).filter(**filters)
        stats = {
            'total_orders': orders.count(),
            'total_lines': Line.objects.filter(order__in=orders).count(),
            'total_revenue': orders.aggregate(
                Sum('total_incl_tax'))['total_incl_tax__sum'] or D('0.00'),
            'order_status_breakdown': orders.order_by('status').values(
                'status').annotate(freq=Count('id')),
        }
        return stats






