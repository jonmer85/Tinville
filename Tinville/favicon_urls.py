from django.views.generic.base import RedirectView
from Tinville.settings.base import STATIC_URL
from django.conf.urls import url, patterns

urlpatterns = patterns('',
url(r'^android-icon-36x36.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/android-icon-36x36.png')),
url(r'^android-icon-48x48.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/android-icon-48x48.png')),
url(r'^android-icon-72x72.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/android-icon-72x72.png')),
url(r'^android-icon-96x96.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/android-icon-96x96.png')),
url(r'^android-icon-144x144.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/android-icon-144x144.png')),
url(r'^android-icon-192x192.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/android-icon-192x192.png')),
url(r'^apple-touch-icon.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/apple-icon.png')),
url(r'^apple-icon.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/apple-icon.png')),
url(r'^apple-icon-57x57.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/apple-icon-57x57.png')),
url(r'^apple-icon-60x60.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/apple-icon-60x60.png')),
url(r'^apple-icon-72x72.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/')),
url(r'^apple-icon-76x76.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/apple-icon-76x76.png')),
url(r'^apple-icon-114x114.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/apple-icon-114x114.png')),
url(r'^apple-icon-120x120.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/apple-icon-120x120.png')),
url(r'^apple-icon-144x144.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/apple-icon-144x144.png')),
url(r'^apple-icon-152x152.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/apple-icon-152x152.png')),
url(r'^apple-icon-180x180.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/apple-icon-180x180.png')),
url(r'^apple-icon-precomposed.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/apple-icon-precomposed.png')),
url(r'^favicon.ico$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/favicon.ico')),
url(r'^favicon-16x16.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/favicon-16x16.png')),
url(r'^favicon-32x32.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/favicon-32x32.png')),
url(r'^favicon-96x96.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/favicon-96x96.png')),
url(r'^manifest.json$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/manifest.json')),
url(r'^ms-icon-70x70.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/ms-icon-70x70.png')),
url(r'^ms-icon-144x144.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/ms-icon-144x144.png')),
url(r'^ms-icon-150x150.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/ms-icon-150x150.png')),
url(r'^ms-icon-310x310.png$', RedirectView.as_view(url=STATIC_URL + 'img/favicon/ms-icon-310x310.png'))
)
