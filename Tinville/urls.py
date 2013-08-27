from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from Tinville.Site.views import home
from Tinville.Site.views import faq
from Tinville.user.views import RegisterView, CreateDesignerView, CreateShopperView, RegisterSuccessView


admin.autodiscover()

urlpatterns = patterns('',
    # Home Page -- Replace as you prefer
    #url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^$', home),
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^register_designer$', CreateDesignerView.as_view(), name='create-designer'),
    url(r'^register_shopper$', CreateShopperView.as_view(), name='create-shopper'),
    url(r'^register_success/(?P<user_slug>\w+)$', RegisterSuccessView.as_view(), name='register-success'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^faq$', faq),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()