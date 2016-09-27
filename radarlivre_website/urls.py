# -*- coding:utf-8 -*-

from django.conf.urls import url
from radarlivre_website import views

urlpatterns = [
    url(r'^$', views.index, name="page_default"),
    url(r'^index/$', views.index, name="page_index"),
    url(r'^downloads/$', views.downloads_index, name="page_downloads_index"),
    url(r'^contrib/$', views.contrib, name="page_contrib"),
    url(r'^about/$', views.about_index, name="page_about_index"),
    url(r'^about/(?P<pk>[0-9]+)/$', views.about, name="page_about"),
    url(r'^googlec501605f6d7c9fb3.html$', views.googleSearchConsole, name="google_search_console"),
]