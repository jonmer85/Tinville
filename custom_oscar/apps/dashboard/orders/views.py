from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from oscar.apps.dashboard.orders.views import *
from oscar.apps.dashboard.orders.views import OrderListView as CoreOrderListView
from oscar.apps.dashboard.orders.views import OrderDetailView as CoreOrderDetailView
from oscar.apps.dashboard.orders.views import LineDetailView as CoreLineDetailView
from oscar.apps.dashboard.orders.views import OrderStatsView as CoreOrderStatsView
from oscar.core.loading import get_model
from django.views.generic import View
from designer_shop.models import Shop
from custom_oscar.apps.order.models import ShippingEvent
from custom_oscar.apps.order.exceptions import *
import json
import re
import easypost
import logging
from common.utils import isNoneOrEmptyOrWhitespace, ExtractDesignerIdFromOrderId

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
        orderlines = [l.order_id for l in Line.objects.filter(partner__in=partners)]
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
    order_actions = ('save_note', 'delete_note', 'change_order_status',
                     'create_order_payment_event', 'calculate_shipping_cost')

    def create_shipping_event(self, request, order, lines, quantities):
        code = request.POST['shipping_event_type']
        try:
            event_type = ShippingEventType._default_manager.get(code=code)
        except ShippingEventType.DoesNotExist:
            messages.error(request, _("The event type '%s' is not valid")
                           % code)
            return self.reload_page()

        reference = request.POST.get('reference', None)
        response = HttpResponse()
        try:
            if event_type.name == 'Shipped':
                parcelType = request.POST.get('parcel_type', None)
                if parcelType == "Parcel":
                    weight = float(request.POST.get('weight', None))*16
                else:
                    weight = 10
                self.validate_parcel_type(parcelType)
                parcelType = {
                    'predefined_package' : parcelType,
                    'weight' : weight
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
        return self.reload_page()

    def post_specific_shipment(self, order, parcelType):
        shipment = self.get_shipment(order, parcelType)
        try:
            shipment.buy(rate=shipment.lowest_rate(carriers=['USPS'], services=['Priority']))
        except Exception as e:
            messages.error(self.request, "Failed to buy shipping label, please try again.")
            logger.error(e)

        shipment_info = {
            "labelUrl": shipment.postage_label.label_url,
            "tracking": shipment.tracking_code,
            "rate": shipment.selected_rate.rate
        }

        return shipment_info

    def get_context_data(self, **kwargs):
        ctx = super(OrderDetailView, self).get_context_data(**kwargs)
        ctx['calculated_shipping_cost'] = self.calculate_shipping_cost(None, kwargs['object'])
        ctx['partner_address_exists'] = self._partner_address_exists()
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
        if cache.get('parcel_types') == None or len(self.get_supported_parcel_types()) > len(cache.get('parcel_types')):
            for parcel_type in self.get_supported_parcel_types():
                if parcel_type['type'] == 'flatrate':
                    parcelType = { 'predefined_package': parcel_type['easypostname'],
                                  'weight': 10 }
                    flatrate_type = self.get_specific_shipment(order, parcelType)
                    shipment_collection.append(flatrate_type)
                    logger.info("flatrate_type: " + str(parcelType) + "=" + str(flatrate_type))
                elif parcel_type['type'] == 'calculated':
                    shipment_collection.append({'type': parcel_type['easypostname'],
                                                'name':parcel_type['displayname'],
                                                'rates': [{'rate': '0.00'}]})
                cache.set('parcel_types', shipment_collection, 7200)
            return shipment_collection
        else:
            return cache.get('parcel_types')

    def get_shipment(self, order, parcelType):
        from_address = self._GetShopAddress(order.number)
        to_address = EasyPostAddressFormatter(order.shipping_address)
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
        return [
                {'type': 'calculated', 'easypostname': 'Parcel', 'displayname': 'Weight Based'},
                {'type': 'flatrate', 'easypostname': 'FlatRateEnvelope', 'displayname': 'Flat-Rate Envelope'},
                {'type': 'flatrate', 'easypostname': 'FlatRatePaddedEnvelope', 'displayname': 'Flat-Rate Padded Envelope'},
                {'type': 'flatrate', 'easypostname': 'SmallFlatRateBox', 'displayname': 'Small Flat-Rate Box'},
                {'type': 'flatrate', 'easypostname': 'MediumFlatRateBox', 'displayname': 'Medium Flat-Rate Box'},
                {'type': 'flatrate', 'easypostname': 'LargeFlatRateBox', 'displayname': 'Large Flat-Rate Box'}]

    def validate_parcel_type(self, parcel_type):
        validtypes = []
        for types in self.get_supported_parcel_types():
            validtypes.append(types['easypostname'])
        if parcel_type not in validtypes:
            msg = (parcel_type)
            raise InvalidParcelType(msg)

    def calculate_shipping_cost(self, request, order):
        if request == None:
            return 0.00
        else:
            if 'weight' in request.POST and is_number(request.POST['weight']) and request.POST['weight'] > 0:
                weight = float(request.POST['weight']) * 16
            else:
                raise "Blame Andy"
            if 'parcel_type' in request.POST:
                try:
                    self.validate_parcel_type(request.POST['parcel_type'])
                except InvalidParcelType as e:
                    messages.error(request, ("Unable to create shipping event due to"
                                      " unsupported Parcel Type: %s") % e)
                    return self.reload_page()
                parcelType = { 'predefined_package': request.POST['parcel_type'],
                               'weight': weight }
            else:
                raise "Blame Andy"
            shipment = self.get_specific_shipment(order, parcelType)
            shippingcost = shipment['rates'][0]['rate']
            return HttpResponse(shippingcost, content_type='application/json')

    def _GetShopAddress(self,orderId):
        userId = ExtractDesignerIdFromOrderId(orderId)

        partners = Partner._default_manager.filter(users=userId)
        if(partners == None or len(partners) == 0):
            raise ValueError("Partners Address is empty")

        shop_address = EasyPostAddressFormatter(partners[0].addresses.instance.primary_address)
        return shop_address

    def _partner_address_exists(self):
        partners = Partner._default_manager.filter(users=self.request.user.id)
        if(partners == None or len(partners) == 0 or partners[0].addresses.instance.primary_address == None):
            return False
        return True

def EasyPostAddressFormatter(address):

        if(address == None):
            raise ValueError("Address is Empty.")

        if not hasattr(address, 'name') or not isNoneOrEmptyOrWhitespace(address.name):
            raise ValueError("Missing Name for Address")

        if not hasattr(address, 'line1') or not isNoneOrEmptyOrWhitespace(address.line1):
            raise ValueError("Missing line1 for Address")

        if not hasattr(address, 'city') or not isNoneOrEmptyOrWhitespace(address.city):
            raise ValueError("Missing City for Address")

        if not hasattr(address, 'state') or not isNoneOrEmptyOrWhitespace(address.state):
            raise ValueError("Missing State for Address")

        if not hasattr(address, 'postcode') or not isNoneOrEmptyOrWhitespace(address.postcode):
            raise ValueError("Missing postcode for Address")

        _address = {
            'name': address.name,
            'street1': address.line1,
            'street2': address.line2,
            'city': address.city,
            'state': address.state,
            'zip': address.postcode
        }
        return _address

@csrf_exempt
def packageStatus(request):

        response = HttpResponse()
        if(isNoneOrEmptyOrWhitespace(request.body) == False):
            response.reason_phrase = 'BadRequest'
            response.status_code = 400
            return response

        package = json.loads(request.body)

        if('result' not in package):
            response.reason_phrase = 'BadRequest'
            response.status_code = 400
            return response

        result = package['result']

        if(result is None):
            response.reason_phrase = 'BadRequest'
            response.status_code = 400
            return response

        if('status' not in result):
            response.reason_phrase = 'BadRequest'
            response.status_code = 400
            return response

        if(isNoneOrEmptyOrWhitespace(result['status']) == False):
            response.reason_phrase = 'BadRequest'
            response.status_code = 400
            return response

        if result['status'] == 'in_transit':
            if('tracking_code' not in result):
                response.reason_phrase = 'BadRequest'
                response.status_code = 400
                return response

            tracking_code = result['tracking_code']

            if(isNoneOrEmptyOrWhitespace(tracking_code) == False):
                response.reason_phrase = 'BadRequest'
                response.status_code = 400
                return response

            try:
                EventHandler().create_inTransit_event(tracking_code)
            except:
                response.reason_phrase = 'BadRequest'
                response.status_code = 400
                return response

        response.status_code = 200
        response.reason_phrase = 'OK'

        return response

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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






