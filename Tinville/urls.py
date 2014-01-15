from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from Tinville.Site.views import CreateMailingListItemView
from Tinville.user.views import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', CreateMailingListItemView.as_view(), name='home'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns() + [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
