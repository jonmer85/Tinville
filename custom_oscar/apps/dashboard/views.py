from datetime import timedelta
from decimal import Decimal as D, ROUND_UP
from designer_shop.models import Shop

from django.utils.timezone import now
from oscar.core.loading import get_model
from django.db.models import Avg, Sum, Count, Q
from oscar.core.compat import get_user_model
from oscar.apps.dashboard.views import IndexView as CoreIndexView
from django.views.generic import TemplateView

from custom_oscar.apps.customer.views import _get_shipping_address_pk_that_is_shop_shipping_address
from custom_oscar.apps.dashboard.orders.views import queryset_orders_for_user
from common.utils import get_list_or_empty

ConditionalOffer = get_model('offer', 'ConditionalOffer')
Voucher = get_model('voucher', 'Voucher')
Basket = get_model('basket', 'Basket')
StockAlert = get_model('partner', 'StockAlert')
Product = get_model('catalogue', 'Product')
Order = get_model('order', 'Order')
Line = get_model('order', 'Line')
Partner = get_model('partner', 'Partner')
User = get_user_model()


def get_total_product_count(user):
    if user.is_staff:
        return Product.objects.count()
    else:
        return len(get_list_or_empty(Product, shop__user=user, parent__isnull=True))


def get_dashboard_notifications(request, orders):
    orders_ready_to_be_shipped = orders.filter(Q(status='Ready for Shipment') | Q(status='Partially Shipped'))
    count = orders_ready_to_be_shipped.count()
    designer_payment_info_not_configured = len(request.user.recipient_id) == 0
    if designer_payment_info_not_configured:
        count += 1
    designer_shop_shipping_address_not_configured = _get_shipping_address_pk_that_is_shop_shipping_address(
        request) is None
    if designer_shop_shipping_address_not_configured:
        count += 1

    return \
        {
            "notifications":
                {
                    'orders_ready_to_be_shipped': orders_ready_to_be_shipped.count(),
                    'designer_payment_info_not_configured': designer_payment_info_not_configured,
                    'designer_shop_shipping_address_not_configured': designer_shop_shipping_address_not_configured
                },
            "count": count
        }


class IndexView(CoreIndexView):
    def get_template_names(self):
        if self.request.user.is_staff:
            return ['templates/dashboard/index.html', ]
        else:
            return ['templates/dashboard/index_nonstaff.html', 'templates/dashboard/index.html']

    def get_context_data(self, **kwargs):
        ctx = TemplateView.get_context_data(self, **kwargs)
        ctx.update(self.get_stats())
        if not self.request.user.is_staff or self.request.user.is_seller:
            ctx.update({"shop_slug": Shop.objects.get(user=self.request.user).slug})
        else:
            ctx.update({"shop_slug": "demo"})
        return ctx

    def get_hourly_report(self, hours=24, segments=10):
        """
        Get report of order revenue split up in hourly chunks. A report is
        generated for the last *hours* (default=24) from the current time.
        The report provides ``max_revenue`` of the hourly order revenue sum,
        ``y-range`` as the labeling for the y-axis in a template and
        ``order_total_hourly``, a list of properties for hourly chunks.
        *segments* defines the number of labeling segments used for the y-axis
        when generating the y-axis labels (default=10).
        """
        # Get datetime for 24 hours agao
        time_now = now().replace(minute=0, second=0)
        start_time = time_now - timedelta(hours=hours - 1)

        orders_last_day = queryset_orders_for_user(self.request.user).filter(date_placed__gt=start_time)

        order_total_hourly = []
        for hour in range(0, hours, 2):
            end_time = start_time + timedelta(hours=2)
            hourly_orders = orders_last_day.filter(date_placed__gt=start_time,
                                                   date_placed__lt=end_time)
            total = hourly_orders.aggregate(
                Sum('total_incl_tax')
            )['total_incl_tax__sum'] or D('0.0')
            order_total_hourly.append({
                'end_time': end_time,
                'total_incl_tax': total
            })
            start_time = end_time

        max_value = max([x['total_incl_tax'] for x in order_total_hourly])
        divisor = 1
        while divisor < max_value / 50:
            divisor *= 10
        max_value = (max_value / divisor).quantize(D('1'), rounding=ROUND_UP)
        max_value *= divisor
        if max_value:
            segment_size = (max_value) / D('100.0')
            for item in order_total_hourly:
                item['percentage'] = int(item['total_incl_tax'] / segment_size)

            y_range = []
            y_axis_steps = max_value / D(str(segments))
            for idx in reversed(range(segments + 1)):
                y_range.append(idx * y_axis_steps)
        else:
            y_range = []
            for item in order_total_hourly:
                item['percentage'] = 0

        ctx = {
            'order_total_hourly': order_total_hourly,
            'max_revenue': max_value,
            'y_range': y_range,
        }
        return ctx

    def get_stats(self):
        datetime_24hrs_ago = now() - timedelta(hours=24)

        orders = queryset_orders_for_user(self.request.user)
        orders_last_day = orders.filter(date_placed__gt=datetime_24hrs_ago)

        open_alerts = StockAlert.objects.filter(status=StockAlert.OPEN)
        closed_alerts = StockAlert.objects.filter(status=StockAlert.CLOSED)

        total_lines_last_day = Line.objects.filter(
            order__in=orders_last_day).count()

        # total_open_baskets = self.get_open_baskets()
        #
        # # {'lines__stockrecord__partner_id': self.request.user.id}
        # inner_qs = self.get_open_baskets()
        # entries = Entry.objects.filter(blog__name__in=inner_qs)
        #
        # for basket in total_open_baskets:
        #     # lines__stockrecord__partner==self.request.user
        #     for line in basket.lines.all():
        #         sdsd = 2
        # # total_filtered_baskets_users

        stats = {
            'total_orders_last_day': orders_last_day.count(),
            'total_lines_last_day': total_lines_last_day,

            'average_order_costs': orders_last_day.aggregate(
                Avg('total_incl_tax')
            )['total_incl_tax__avg'] or D('0.00'),

            'total_revenue_last_day': orders_last_day.aggregate(
                Sum('total_incl_tax')
            )['total_incl_tax__sum'] or D('0.00'),

            'hourly_report_dict': self.get_hourly_report(hours=24),
            'total_customers_last_day': orders_last_day.values_list('user', flat=True).distinct().count() +
                                        orders_last_day.values_list('guest_email', flat=True).distinct().count(),

            'total_open_baskets_last_day': self.get_open_baskets({
                'date_created__gt': datetime_24hrs_ago
            }).count(),

            'total_products': get_total_product_count(self.request.user),
            'total_open_stock_alerts': open_alerts.count(),
            'total_closed_stock_alerts': closed_alerts.count(),

            'total_site_offers': self.get_active_site_offers().count(),
            'total_vouchers': self.get_active_vouchers().count(),
            'total_promotions': self.get_number_of_promotions(),

            'total_customers': orders.values_list('user', flat=True).distinct().count() +
                               orders.values_list('guest_email', flat=True).distinct().count(),
            'total_open_baskets': self.get_open_baskets().count(),
            'total_orders': orders.count(),
            'total_lines': Line.objects.filter(order__in=orders).count(),
            'total_revenue': orders.aggregate(
                Sum('total_incl_tax')
            )['total_incl_tax__sum'] or D('0.00'),

            'order_status_breakdown': orders.order_by(
                'status'
            ).values('status').annotate(freq=Count('id'))

        }
        stats.update(get_dashboard_notifications(self.request, orders)["notifications"])
        return stats
