# -*- coding:utf-8 -*-

from django.urls import re_path
from django.contrib.sitemaps.views import sitemap

from radarlivre_website import views
from radarlivre_website.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    re_path(r'^$', views.index, name="page_default"),
    re_path(r'^index/$', views.index, name="page_index"),
    re_path(r'^downloads/$', views.downloads_index, name="page_downloads_index"),
    re_path(r'^contrib/$', views.contrib, name="page_contrib"),
    re_path(r'^about/$', views.about_index, name="page_about_index"),
    re_path(r'^about/(?P<pk>[0-9]+)/$', views.about, name="page_about"),

    # To help the search enguine
    re_path(r'^googlec501605f6d7c9fb3.html$', views.googleSearchConsole,
        name="google_search_console"),

    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]
