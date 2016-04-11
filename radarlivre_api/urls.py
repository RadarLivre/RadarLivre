from django.conf.urls import url
from radarlivre_api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # Urls to manage airplanes
    url(r'^api/airplane/$', views.AirplaneList.as_view()),
    url(r'^api/airplane/(?P<pk>[a-zA-Z0-9]+)/$', views.AirplaneDetail.as_view()),
    
    # Urls to manage airplanes informations
    url(r'^api/airplane_info/$', views.AirplaneInfoList.as_view()),
    url(r'^api/airplane_info/(?P<pk>[a-zA-Z0-9]+)/$', views.AirplaneInfoDetail.as_view()),
    
    # Urls to manage airports
    url(r'^api/airport/$', views.AirportList.as_view()),
    url(r'^api/airport/(?P<pk>[a-zA-Z0-9]+)/$', views.AirportDetail.as_view()),
    
    # Urls to manage route
    url(r'^api/route/$', views.FlightList.as_view()),
    url(r'^api/route/(?P<pk>[0-9]+)/$', views.FlightDetail.as_view()),
    
    # Urls to manage observation
    url(r'^api/observation/$', views.ObservationList.as_view()),
    url(r'^api/observation/(?P<pk>[0-9]+)/$', views.ObservationDetail.as_view()),
    
    # Urls to manage observation
    url(r'^api/half_observation/$', views.HalfObservationList.as_view()),
    url(r'^api/half_observation/(?P<pk>[0-9]+)/$', views.HalfObservationDetail.as_view()),
    
    # Urls to receive ADS-B messages
    url(r'^api/adsb_message/$', views.ADSBMessageList.as_view()),
    
    # Urls to manage about texts
    url(r'^api/about/$', views.AboutList.as_view()),
    url(r'^api/about/(?P<pk>[0-9]+)/$', views.AboutDetail.as_view()),
    
    # Urls to manage notifies
    url(r'^api/notify/$', views.NotifyList.as_view()),
    url(r'^api/notify/(?P<pk>[0-9]+)/$', views.NotifyDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)