# -*- coding:utf-8 -*-

from django.urls import include, re_path
from radarlivre_api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    
    re_path(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    re_path(r'^api/airport/$', views.AirportList.as_view()),
    re_path(r'^api/airport/(?P<pk>[0-9]+)/$', views.AirportDetail.as_view()),


    re_path(r'^api/airline/$', views.AirlineList.as_view()),
    re_path(r'^api/airline/(?P<pk>[0-9]+)/$', views.AirlineDetail.as_view()),
    

    re_path(r'^api/flight/$', views.FlightList.as_view()),
    re_path(r'^api/flight/(?P<pk>[0-9]+)/$', views.FlightDetail.as_view()),


    re_path(r'^api/flight_info/$', views.FlightInfoList.as_view()),
    re_path(r'^api/flight_propagated_trajectory/$', views.FlightPropagatedTrajectoryList.as_view()),
    

    re_path(r'^api/observation/$', views.ObservationList.as_view()),
    re_path(r'^api/observation/(?P<pk>[0-9]+)/$', views.ObservationDetail.as_view()),


    re_path(r'^api/adsb_info/$', views.ADSBInfoList.as_view()),
    

    re_path(r'^api/about/$', views.AboutList.as_view()),
    re_path(r'^api/about/(?P<pk>[0-9]+)/$', views.AboutDetail.as_view()),
    

    re_path(r'^api/notify/$', views.NotifyList.as_view()),
    re_path(r'^api/notify/(?P<pk>[0-9]+)/$', views.NotifyDetail.as_view()),


    re_path(r'^api/collector/$', views.CollectorList.as_view()),
    re_path(r'^api/collector/(?P<key>[a-zA-Z0-9\-]+)/$', views.CollectorDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)