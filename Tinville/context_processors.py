from django.conf import settings

def google_analytics_id(request):
    return { 'GOOGLE_ANALYTICS_TRACKING_ID': settings.GOOGLE_ANALYTICS_TRACKING_ID }