from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from Tinville.user.views import ActivationView, TemplateView, ajax_login, register
from Tinville.user.forms import LoginForm, TinvilleShopperCreationForm, TinvilleDesignerCreationForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='teaser_home.html'), name='home'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #IMPORTANT!!! This route need to always be last since it consumes the entire namespace!
    url(r'^(?P<name>\w+)/$', 'designer_shop.views.shopper'),
)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns() + [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
