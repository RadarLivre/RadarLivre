# -*- coding:utf-8 -*-

from django.contrib.sitemaps.views import sitemap
from django.urls import path

from radarlivre_website import views
from radarlivre_website.sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path(r"", views.index, name="page_default"),
    path(r"index/", views.index, name="page_index"),
    path(r"downloads/", views.downloads_index, name="page_downloads_index"),
    path(r"contrib/", views.contrib, name="page_contrib"),
    path(r"about/", views.about_index, name="page_about_index"),
    path(r"about/<pk>/", views.about, name="page_about"),
    # To help the search engine
    path(
        r"googlec501605f6d7c9fb3.html",
        views.googleSearchConsole,
        name="google_search_console",
    ),
    path(
        r"sitemap\.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
