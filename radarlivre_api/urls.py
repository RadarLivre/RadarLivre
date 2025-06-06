# -*- coding:utf-8 -*-

from django.conf.urls import include
from django.urls import path

from radarlivre_api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(r"api/airport/", views.AirportList.as_view()),
    path(r"api/airport/<pk>/", views.AirportDetail.as_view()),
    path(r"api/airline/", views.AirlineList.as_view()),
    path(r"api/airline/<pk>/", views.AirlineDetail.as_view()),
    path(r"api/flight/", views.FlightList.as_view()),
    path(r"api/flight/<pk>/", views.FlightDetail.as_view()),
    path(r"api/flight_info/", views.FlightInfoList.as_view()),
    path(
        r"api/flight_propagated_trajectory/",
        views.FlightPropagatedTrajectoryList.as_view(),
    ),
    path(r"api/observation/", views.ObservationList.as_view()),
    path(r"api/observation/<pk>/", views.ObservationDetail.as_view()),
    path(r"api/adsb_info/", views.ADSBInfoList.as_view()),
    path(r"api/about/", views.AboutList.as_view()),
    path(r"api/about/<pk>/", views.AboutDetail.as_view()),
    path(r"api/notify/", views.NotifyList.as_view()),
    path(r"api/notify/<pk>/", views.NotifyDetail.as_view()),
    path(r"api/collector/", views.CollectorList.as_view()),
    path(r"api/collector/<key>/", views.CollectorDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
