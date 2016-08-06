# -*- coding=utf-8 -*-

import logging

from rest_framework import status, permissions
from rest_framework.filters import DjangoFilterBackend, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,\
    UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from radarlivre_api.adsb import decoder
from radarlivre_api.models import Airplane, Airport, Flight, Observation, AirplaneInfo, \
    About, Notify, Collector
from radarlivre_api.models.serializers import AirplaneSerializer, AirportSerializer, FlightSerializer, ObservationSerializer,  \
    AboutSerializer, NotifySerializer, CollectorSerializer,\
    AirplaneInfoSerializer
from radarlivre_api.utils import airline_info
from radarlivre_api.views.filters import ObservationPrecisionFilter, \
    ObservationFlightFilter, MapBoundsFilter, \
    ObservationLastTimestampFilter, MaxUpdateDelayFilter
from django.http.response import Http404
from time import time


logger = logging.getLogger("radarlivre.log")


class CollectorList(ListCreateAPIView):
    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer
    filter_backends = (DjangoFilterBackend, MaxUpdateDelayFilter)
    permission_classes = (permissions.DjangoModelPermissions,)
    

class CollectorDetail(APIView):
    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    
    def get_object(self, pk):
        try:
            return Collector.objects.get(pk=pk)
        except Collector.DoesNotExist:
            raise Http404
    
    def put(self, request, pk, format=None):
        collector = self.get_object(pk)
        serializer = CollectorSerializer(collector, data=request.data)
        if serializer.is_valid():
            collector.timestamp = int(time() * 1000)
            collector.save()
        return Response(serializer.data)


class AirplaneList(ListCreateAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    
class AirplaneDetail(RetrieveUpdateDestroyAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (permissions.IsAdminUser,)


class AirplaneInfoList(ListCreateAPIView):
    queryset = AirplaneInfo.objects.all()
    serializer_class = AirplaneInfoSerializer
    filter_backends = (DjangoFilterBackend, MaxUpdateDelayFilter, MapBoundsFilter)
    filter_fields = ('airplane', 'flight')
    permission_classes = (permissions.DjangoModelPermissions,)
    
class AirplaneInfoDetail(RetrieveUpdateDestroyAPIView):
    queryset = AirplaneInfo.objects.all()
    serializer_class = AirplaneInfoSerializer
    permission_classes = (permissions.IsAdminUser,)


class AirportList(ListCreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('prefix', 'name', 'country', 'state', 'city', 'latitude', 'longitude', 'altitude')
    permission_classes = (permissions.DjangoModelPermissions,)
    
class AirportDetail(RetrieveUpdateDestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (permissions.IsAdminUser,)


class FlightList(ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('airplane', 'origin', 'destine')
    permission_classes = (permissions.DjangoModelPermissions,)
    
class FlightDetail(RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (permissions.IsAdminUser,)


class ObservationList(ListCreateAPIView):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,   
        ObservationPrecisionFilter,
        ObservationFlightFilter, 
        ObservationLastTimestampFilter
    )
    
    filter_fields = ('airplane', 'flight')
    ordering_fields = '__all__'
    permission_classes = (permissions.DjangoModelPermissions,)
    
class ObservationDetail(RetrieveUpdateDestroyAPIView):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
    permission_classes = (permissions.IsAdminUser,)


class AboutList(ListCreateAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = (permissions.DjangoModelPermissions, )
    
class AboutDetail(RetrieveUpdateDestroyAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = (permissions.IsAdminUser,)

    
class NotifyList(ListCreateAPIView):
    queryset = Notify.objects.all()
    serializer_class = NotifySerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    
class NotifyDetail(RetrieveUpdateDestroyAPIView):
    queryset = Notify.objects.all()
    serializer_class = NotifySerializer
    permission_classes = (permissions.IsAdminUser,)
    