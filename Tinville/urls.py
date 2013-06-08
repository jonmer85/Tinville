from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from Tinville.Site.views import home
from Tinville.Site.views import register
from Tinville.Site.views import register_designer

admin.autodiscover()

urlpatterns = patterns('',
    # Home Page -- Replace as you prefer
    #url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^$', home),
    url(r'^register$', register),
    url(r'^register_designer$', register_designer),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()