# -*- coding:utf-8 -*-

from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap

from radarlivre_website import views
from radarlivre_website.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    url(r'^$', views.index, name="page_default"),
    url(r'^index/$', views.index, name="page_index"),
    url(r'^downloads/$', views.downloads_index, name="page_downloads_index"),
    url(r'^contrib/$', views.contrib, name="page_contrib"),
    url(r'^about/$', views.about_index, name="page_about_index"),
    url(r'^about/(?P<pk>[0-9]+)/$', views.about, name="page_about"),

    # To help the search enguine
    url(r'^googlec501605f6d7c9fb3.html$', views.googleSearchConsole,
        name="google_search_console"),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]
