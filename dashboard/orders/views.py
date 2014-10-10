from oscar.apps.dashboard.orders.views import OrderListView as CoreOrderListView
from oscar.apps.dashboard.orders.views import OrderDetailView as CoreOrderDetailView

class OrderListView(CoreOrderListView):
    template_name = 'templates/dashboard/orders/order_list.html'

class OrderDetailView(CoreOrderDetailView):
    template_name = 'templates/dashboard/orders/order_detail.html'