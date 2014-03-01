from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import RedirectView, TemplateView
from user.views import ActivationView, ajax_login, register
from user.forms import LoginForm

admin.autodiscover()

urlpatterns = patterns('django.contrib.flatpages.views',
    url(r'^about/$', 'flatpage',  kwargs={'url': '/about/'}, name='home_about'),
    url(r'^faq/$', 'flatpage', kwargs={'url': '/faq/'}, name='home_faq'),
    url(r'^policies/$', 'flatpage', kwargs={'url': '/policies/'}, name='home_policies'),
    url(r'^terms/$', 'flatpage', kwargs={'url': '/terms/'}, name='home_terms'),
)

urlpatterns += patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^register$', 'user.views.register'),
    url(r'^activate/(?P<activation_key>\w+)$', 'user.views.activation', name='activate-user'),
    url(r'^ajax_login$', ajax_login,
        {'template_name': 'login_form.html', 'authentication_form': LoginForm},
        name='ajax_logins'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^shopeditor/test/$', 'designer_shop.views.shopeditor'),
    #IMPORTANT!!! This route need to always be last since it consumes the entire namespace!
    url(r'^(?P<slug>\w+)/$', 'designer_shop.views.shopper'),
)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns() + [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
