from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from Tinville.user.views import CreateDesignerView, CreateShopperView, ActivationView, TemplateView, login
from Tinville.user.forms import LoginForm


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^register$', TemplateView.as_view(template_name='register.html'), name='register'),
    url(r'^register_designer$', CreateDesignerView.as_view(), name='create-designer'),
    url(r'^register_shopper$', CreateShopperView.as_view(), name='create-shopper'),
    url(r'^activate/(?P<activation_key>\w+)$', ActivationView.as_view(), name='activate-user'),

    url(r'^login$', login,
        {'template_name': 'login.html', 'authentication_form': LoginForm},
        name='login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    )


urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^about/$', 'flatpage',  kwargs={'url': '/about/'}, name='home_about'),
    url(r'^faq/$', 'flatpage', kwargs={'url': '/faq/'}, name='home_faq'),
    url(r'^policies/$', 'flatpage', kwargs={'url': '/policies/'}, name='home_policies'),
    url(r'^terms/$', 'flatpage', kwargs={'url': '/terms/'}, name='home_terms'),
)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()