from oscar.apps.dashboard.orders.views import *
from oscar.apps.dashboard.orders.views import OrderListView as CoreOrderListView
from oscar.apps.dashboard.orders.views import OrderDetailView as CoreOrderDetailView
from oscar.apps.dashboard.orders.views import LineDetailView as CoreLineDetailView
from oscar.apps.dashboard.orders.views import OrderStatsView as CoreOrderStatsView
from oscar.core.loading import get_model
from django.views.generic import View
import re
import json
import easypost

Order = get_model('order', 'Order')
Partner = get_model('partner', 'Partner')
Line = get_model('order', 'Line')

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
            EventHandler().handle_shipping_event(order, event_type, lines,
                                                 quantities, request, response,
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
        else:
            messages.success(request, ("Shipping event created"))
        return self.reload_page_response()

    def get_context_data(self, **kwargs):
        ctx = super(OrderDetailView, self).get_context_data(**kwargs)
        ctx['box_types'] = self.get_shipment_context(**kwargs)
        ctx['box_types_json'] = json.dumps(ctx['box_types'])
        return ctx

    def get_shipment_context(self, **kwargs):
        shipment_collection = []
        parcelType = {
                        'predefined_package' : 'FlatRateEnvelope',
                        'weight' : 10
                    }
        shipment_collection.append(self.get_specific_shipment(kwargs, parcelType))

        parcelType = {
            'predefined_package' : 'FlatRatePaddedEnvelope',
            'weight' : 10
        }
        shipment_collection.append(self.get_specific_shipment(kwargs, parcelType))

        parcelType = {
            'predefined_package' : 'SmallFlatRateBox',
            'weight' : 10
        }
        shipment_collection.append(self.get_specific_shipment(kwargs, parcelType))

        parcelType = {
            'predefined_package' : 'MediumFlatRateBox',
            'weight' : 10
        }
        shipment_collection.append(self.get_specific_shipment(kwargs, parcelType))

        parcelType = {
            'predefined_package' : 'LargeFlatRateBox',
            'weight' : 10
        }
        shipment_collection.append(self.get_specific_shipment(kwargs, parcelType))

        return shipment_collection

    def get_specific_shipment(self, kwargs, parcelType):

        order = kwargs['object']
        try:

            #TODO: Get current user
            #from_address = self._GetShopAddress(order.number)
            from_address = self._EasyPostAddressFormatter(order.shipping_address)

        except ValueError as e:
            #TODO Redirect to Shop's Address Form Page rather than home
            return HttpResponseRedirect(reverse('home'))

        to_address = self._EasyPostAddressFormatter(order.shipping_address)

        try:
            shipment = easypost.Shipment.create(
                to_address=to_address,
                from_address=from_address,
                parcel=parcelType
            )
        except Exception as e:
            #TODO Handle a failed Shipment Create
            pass

        #TODO: Add appropriate logging/Exception message for shipment validation
        if(shipment == None):
            raise ValueError("Shipment is empty")

        if(shipment.parcel == None):
            raise ValueError("Parcel is empty")

        if(shipment.parcel.predefined_package == None):
            raise ValueError("Parcel type is empty")

        if(shipment.rates == None):
            raise ValueError("Shipping rates is empty")

        rates = []
        for current in range(0, len(shipment.rates)):
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

    def _GetShopAddress(self,request):
        partners = Partner._default_manager.filter(users=request.user)
        #TODO do something with this broken logic...
        for partner in partners:
            shop_address = self._EasyPostAddressFormatter(partner.addresses.instance.primary_address)
            return shop_address

    def _EasyPostAddressFormatter(self, address):
        #TODO Validate address
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






