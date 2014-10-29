from oscar.apps.dashboard.orders.views import OrderListView as CoreOrderListView
from oscar.apps.dashboard.orders.views import OrderDetailView as CoreOrderDetailView
from oscar.apps.dashboard.orders.views import LineDetailView as CoreLineDetailView
from oscar.core.loading import get_model
from django.views.generic import View

Order = get_model('order', 'Order')
Partner = get_model('partner', 'Partner')

def queryset_orders_for_user(user):
    """
    Returns a queryset of all orders that a user is allowed to access.
    A staff user may access all orders.
    To allow access to an order for a non-staff user, at least one line's
    partner has to have the user in the partner's list.
    """
    queryset = Order._default_manager.select_related(
        'billing_address', 'billing_address__country',
        'shipping_address', 'shipping_address__country',
        'user'
        ).prefetch_related('lines')
    if user.is_staff:
        return queryset
    else:
        partners = Partner._default_manager.filter(users=user)
        return queryset.filter(number__contains="-").filter(lines__partner__in=partners).distinct()

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






