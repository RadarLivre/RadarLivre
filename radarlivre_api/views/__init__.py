# -*- coding=utf-8 -*-

import logging
from time import time

from django.db.models.aggregates import Max
from django.http.response import Http404
from rest_framework import permissions, status
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from radarlivre_api.models import Airport, Flight, Observation, About, Notify, Collector, Airline, ADSBInfo, FlightInfo
from radarlivre_api.models.serializers import AirportSerializer, FlightSerializer, ObservationSerializer,  \
    AboutSerializer, NotifySerializer, CollectorSerializer, \
    AirlineSerializer, ADSBInfoSerializer, FlightInfoSerializer
from radarlivre_api.utils import Util
from radarlivre_api.views.filters import ObservationPrecisionFilter, \
    ObservationFlightFilter, MapBoundsFilter, \
    MaxUpdateDelayFilter, AirportTypeZoomFilter, FlightFilter, FlightClusteringFilter

logger = logging.getLogger("radarlivre.log")


class CollectorList(ListCreateAPIView):
    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer
    filter_backends = (filters.DjangoFilterBackend, MaxUpdateDelayFilter)
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    

class CollectorDetail(APIView):
    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    
    def get_object(self, key):
        try:
            return Collector.objects.get(key=key)
        except Collector.DoesNotExist:
            raise Http404

    def put(self, request, key, format=None):
        collector = self.get_object(key)
        serializer = CollectorSerializer(collector, data=request.data)
        collector.timestamp = int(time() * 1000)
        collector.save()
        return Response("", status=status.HTTP_200_OK)


class AirlineList(ListCreateAPIView):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    
class AirlineDetail(RetrieveUpdateDestroyAPIView):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = (permissions.IsAdminUser,)


class AirportList(ListCreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = (filters.DjangoFilterBackend, MapBoundsFilter, AirportTypeZoomFilter)
    filter_fields = ('code', 'name', 'country', 'state', 'city', 'latitude', 'longitude', 'type')
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    
class AirportDetail(RetrieveUpdateDestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (permissions.IsAdminUser,)


class FlightList(ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = (filters.DjangoFilterBackend, FlightFilter)
    filter_fields = ('code', 'airline')
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class FlightInfoList(ListAPIView):
    queryset = FlightInfo.objects.all()
    serializer_class = FlightInfoSerializer
    filter_backends = (filters.DjangoFilterBackend, MaxUpdateDelayFilter, MapBoundsFilter, FlightClusteringFilter)
    filter_fields = ('airline',)
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class FlightDetail(RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (permissions.IsAdminUser,)

class FlightPropagatedTrajectoryList(APIView):

    def get(self, request, format=None):
        propCount = Util.parseParam(request, "propagation_count", 60)
        propInterval = Util.parseParam(request, "propagation_interval", 1000)
        flight = int(Util.parseParam(request, "flight", -1))
        try:
            info = FlightInfo.objects.get(flight=flight)
            obs = info.generatePropagatedTrajectory(propCount, propInterval)
            serializer = ObservationSerializer(obs, many=True)
            return Response(serializer.data)
        except FlightInfo.DoesNotExist as err:
            print (str(err))

        return Response(ObservationSerializer([], many=True).data)

class ADSBInfoList(APIView):
    queryset = ADSBInfo.objects.all()
    serializer_class = ADSBInfoSerializer
    filter_backends = (
        filters.DjangoFilterBackend
    )
    
    filter_fields = ('observation')
    ordering_fields = '__all__'
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get(self, request, format=None):
        snippets = ADSBInfo.objects.all()
        serializer = ADSBInfoSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ADSBInfoSerializer(data=request.data, many=True)

        if serializer.is_valid():
            infos = serializer.save()

            # Generating a observation based in ADS-B info and updating collector
            # timestamp ...
            for info in infos:
                obs = Observation.generateFromADSBInfo(info)
                if obs:
                    FlightInfo.generateFromFlight(obs.flight, obs)
                    logging.info("Views: ADSBInfo received [id=%d, collector=%s]" % (info.id, str(info.collectorKey)))
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ObservationList(ListCreateAPIView):
    queryset = Observation.objects.filter(simulated=False)
    serializer_class = ObservationSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
        ObservationPrecisionFilter,
        ObservationFlightFilter
    )

    filter_fields = ('flight',)
    ordering_fields = '__all__'

class ObservationDetail(RetrieveUpdateDestroyAPIView):
    queryset = Observation.objects.filter(simulated=False)
    serializer_class = ObservationSerializer
    permission_classes = (permissions.IsAdminUser,)


class AboutList(ListCreateAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
    
class AboutDetail(RetrieveUpdateDestroyAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = (permissions.IsAdminUser,)

    
class NotifyList(ListCreateAPIView):
    queryset = Notify.objects.all()
    serializer_class = NotifySerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    
class NotifyDetail(RetrieveUpdateDestroyAPIView):
    queryset = Notify.objects.all()
    serializer_class = NotifySerializer
    permission_classes = (permissions.IsAdminUser,)

