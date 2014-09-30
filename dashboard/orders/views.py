from oscar.apps.dashboard.orders.views import OrderListView as CoreOrderListView

class OrderListView(CoreOrderListView):
    template_name = 'templates/dashboard/orders/order_list.html'
