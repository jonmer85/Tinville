from datetime import timedelta
from decimal import Decimal as D, ROUND_UP
from custom_oscar.apps.dashboard.orders.views import queryset_orders_for_user
from django.utils.timezone import now
from oscar.core.loading import get_model
from django.db.models import Avg, Sum, Count
from oscar.core.compat import get_user_model
from oscar.apps.promotions.models import AbstractPromotion
from oscar.apps.dashboard.views import IndexView as CoreIndexView
from django.views.generic import TemplateView
from common.utils import get_list_or_empty, get_or_none

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


class IndexView(CoreIndexView):
    def get_template_names(self):
        if self.request.user.is_staff:
            return ['templates/dashboard/index.html', ]
        else:
            return ['templates/dashboard/index_nonstaff.html', 'templates/dashboard/index.html']

    def get_context_data(self, **kwargs):
        ctx = TemplateView.get_context_data(self, **kwargs)
        ctx.update(self.get_stats())
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
        # Get datetime for 24 hours ago
        time_now = now().replace(minute=0, second=0)
        start_time = time_now - timedelta(hours=hours - 1)

        orders_last_day = queryset_orders_for_user(self.request.user).filter(date_placed__gt=start_time)
        return super(IndexView, self).get_hourly_report()


    def get_stats(self):
        datetime_24hrs_ago = now() - timedelta(hours=24)

        orders = queryset_orders_for_user(self.request.user)
        orders_last_day = orders.filter(date_placed__gt=datetime_24hrs_ago)

        open_alerts = StockAlert.objects.filter(status=StockAlert.OPEN)
        closed_alerts = StockAlert.objects.filter(status=StockAlert.CLOSED)

        total_lines_last_day = Line.objects.filter(
            order__in=orders_last_day).count()

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
            'total_customers_last_day': User.objects.filter(
                date_joined__gt=datetime_24hrs_ago,
            ).count(),

            'total_open_baskets_last_day': self.get_open_baskets({
                'date_created__gt': datetime_24hrs_ago
            }).count(),

            'total_products': get_total_product_count(self.request.user),
            'total_open_stock_alerts': open_alerts.count(),
            'total_closed_stock_alerts': closed_alerts.count(),

            'total_site_offers': self.get_active_site_offers().count(),
            'total_vouchers': self.get_active_vouchers().count(),
            'total_promotions': self.get_number_of_promotions(),

            'total_customers': User.objects.count(),
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
        return stats


