# -*- coding=utf-8 -*-

import logging
from time import time

from django.db import transaction
from django.http.response import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from radarlivre_api.filters import ObservationPrecisionFilter, \
    ObservationFlightFilter, MapBoundsFilter, \
    MaxUpdateDelayFilter, AirportTypeZoomFilter, FlightFilter, FlightClusteringFilter
from radarlivre_api.models import Airport, Flight, Observation, About, Notify, Collector, Airline, ADSBInfo, FlightInfo
from radarlivre_api.serializers import AirportSerializer, FlightSerializer, ObservationSerializer, \
    AboutSerializer, NotifySerializer, CollectorSerializer, \
    AirlineSerializer, ADSBInfoSerializer, FlightInfoSerializer
from radarlivre_api.utils import Util


class CollectorList(ListCreateAPIView):
    """Endpoint para listar/registrar coletores de dados (GET/POST)"""

    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer
    filter_backends = (DjangoFilterBackend, MaxUpdateDelayFilter)
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class CollectorDetail(APIView):
    """Detalhes de coletor específico via chave (PUT para atualizar timestamp)"""

    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

    def get_object(self, key):
        try:
            return Collector.objects.get(key=key)
        except Collector.DoesNotExist:
            raise Http404

    def put(self, request, key, format=None):
        # Atualiza timestamp do coletor
        Collector.objects.filter(key=key).update(
            timestamp=int(time() *1000)
        )
        return Response("", status=status.HTTP_200_OK)


class AirlineList(ListCreateAPIView):
    """CRUD básico para companhias aéreas (GET lista todas, POST nova)"""

    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class AirlineDetail(RetrieveUpdateDestroyAPIView):
    """Operações específicas por companhia (GET/PUT/DELETE individual)"""

    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = (permissions.IsAdminUser,)


class AirportList(ListCreateAPIView):
    """Listagem de aeroportos com filtros geoespaciais (mapa/zoom/tipo)"""

    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = (DjangoFilterBackend, MapBoundsFilter, AirportTypeZoomFilter)
    filterset_fields = ('code', 'name', 'country', 'state', 'city', 'latitude', 'longitude', 'type')
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class AirportDetail(RetrieveUpdateDestroyAPIView):
    """Gerenciamento individual de aeroportos (acesso admin)"""

    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (permissions.IsAdminUser,)


class FlightList(ListAPIView):
    """Listagem de voos ativos com filtragem por código/companhia"""

    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = (DjangoFilterBackend, FlightFilter)
    filterset_fields = ('code', 'airline')
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class FlightInfoList(ListAPIView):
    """Dados consolidados de voos para exibição em mapa (com clustering)"""

    serializer_class = FlightInfoSerializer
    filter_backends = (DjangoFilterBackend, MaxUpdateDelayFilter, MapBoundsFilter, FlightClusteringFilter)
    filterset_fields = ('airline',)
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get_queryset(self):
        # Query otimizada com seleção de relacionamentos e campos específicos
        return FlightInfo.objects.select_related(
            'airline', 
            'flight'
        ).prefetch_related(
            'flight__observations'
        ).only(
            'id',
            'latitude',
            'longitude',
            'altitude',
            'verticalVelocity',
            'horizontalVelocity',
            'groundTrackHeading',
            'timestamp',
            'flight__code',
            'flight__airline__icao',
            'airline__name',
            'airline__icao'
        ).order_by('timestamp')


class FlightDetail(RetrieveUpdateDestroyAPIView):
    """Operações detalhadas por voo (exclusivo para administradores)"""
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (permissions.IsAdminUser,)


class FlightPropagatedTrajectoryList(APIView):
    """Gera trajetória prevista para um voo específico"""

    def get(self, request, format=None):
        # Usa parâmetros de propagação para simulação de rota futura
        prop_count = Util.parse_param(request, "propagation_count", 60)
        prop_interval = Util.parse_param(request, "propagation_interval", 1000)
        flight = int(Util.parse_param(request, "flight", -1))
        try:
            info = FlightInfo.objects.get(flight=flight)
            obs = info.generate_propagated_trajectory(prop_count, prop_interval)
            serializer = ObservationSerializer(obs, many=True)
            return Response(serializer.data)
        except FlightInfo.DoesNotExist:
            return Response(ObservationSerializer([], many=True).data)


class ADSBInfoList(APIView):
    """Endpoint crítico para ingestão de dados brutos ADS-B"""

    queryset = ADSBInfo.objects.all()
    serializer_class = ADSBInfoSerializer
    filter_backends = (DjangoFilterBackend)

    filterset_fields = ('observation',)
    ordering_fields = '__all__'
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get(self, request, format=None):
        snippets = ADSBInfo.objects.all()
        serializer = ADSBInfoSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # Processamento transacional: salva dados brutos + cria observações + atualiza FlightInfo
        serializer = ADSBInfoSerializer(data=request.data, many=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            with transaction.atomic():
                infos = serializer.save()
                for info in infos:
                    obs = Observation.generate_from_adsb_info(info)
                    if not obs:
                        raise ValueError("Invalid observation data")
                    FlightInfo.generate_from_flight(obs.flight, obs)
                    logging.info(f"Views: ADSBInfo received [id={info.id}, collector={info.collectorKey}]")
                    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logging.error(f"Error processing ADSB info: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ObservationList(ListCreateAPIView):
    """Histórico de observações de voos (filtros de precisão e voo)"""

    queryset = Observation.objects.filter(simulated=False)
    serializer_class = ObservationSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        ObservationPrecisionFilter,
        ObservationFlightFilter
    )

    filterset_fields = ('flight',)
    ordering_fields = '__all__'


class ObservationDetail(RetrieveUpdateDestroyAPIView):
    """Gerenciamento individual de observações (admin apenas)"""

    queryset = Observation.objects.filter(simulated=False)
    serializer_class = ObservationSerializer
    permission_classes = (permissions.IsAdminUser,)


class AboutList(ListCreateAPIView):
    """CRUD para conteúdos institucionais/sobre o projeto"""

    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class AboutDetail(RetrieveUpdateDestroyAPIView):
    """Edição detalhada de páginas institucionais"""

    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = (permissions.IsAdminUser,)


class NotifyList(ListCreateAPIView):
    """Gerenciamento de notificações push para usuários"""

    queryset = Notify.objects.all()
    serializer_class = NotifySerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class NotifyDetail(RetrieveUpdateDestroyAPIView):
    """Operações específicas por notificação"""

    queryset = Notify.objects.all()
    serializer_class = NotifySerializer
    permission_classes = (permissions.IsAdminUser,)
