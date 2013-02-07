from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

from Tinville.Site.views import home

admin.autodiscover()

urlpatterns = patterns('',
    # Home Page -- Replace as you prefer
    #url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^$', home),

#    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()