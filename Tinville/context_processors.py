from django.conf import settings

from designer_shop.models import Shop

def google_analytics_id(request):
    return { 'GOOGLE_ANALYTICS_TRACKING_ID': settings.GOOGLE_ANALYTICS_TRACKING_ID }

def include_shops(request):
    return { 'shops': Shop.objects.all() }