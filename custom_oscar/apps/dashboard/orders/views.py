from oscar.apps.dashboard.orders.views import *
from oscar.apps.dashboard.orders.views import OrderListView as CoreOrderListView
from oscar.apps.dashboard.orders.views import OrderDetailView as CoreOrderDetailView
from oscar.apps.dashboard.orders.views import LineDetailView as CoreLineDetailView
from oscar.apps.dashboard.orders.views import OrderStatsView as CoreOrderStatsView
from oscar.core.loading import get_model
from django.views.generic import View

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
                'status').annotate(freq=Count('id'))
        }
        return stats






