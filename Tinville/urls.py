from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from Tinville.Site.views import faq
from Tinville.user.views import CreateDesignerView, CreateShopperView, ActivationView, TemplateView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^register$', TemplateView.as_view(template_name='register.html'), name='register'),
    url(r'^register_designer$', CreateDesignerView.as_view(), name='create-designer'),
    url(r'^register_shopper$', CreateShopperView.as_view(), name='create-shopper'),
    url(r'^activate/(?P<activation_key>\w+)$', ActivationView.as_view(), name='activate-user'),


    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^faq$', faq),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()