# -*- coding:utf-8 -*-
import time

from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import Distance
from django.db.models import OuterRef, Subquery, F, Window, Exists
from django.db.models.functions import RowNumber
from rest_framework.filters import BaseFilterBackend

from radarlivre_api.models import Observation
from radarlivre_api.utils import Util


# Filtro responsável por pegar apenas os itens mais recentes
class MaxUpdateDelayFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Pega o timestamp atual em milisegundos
        now = int((time.time()) * 1000)
        # Valor padrão o intervalo: 1 min
        max_update_delay = Util.parseParam(request, "max_update_delay", 1 * 60 * 1000)
        return queryset.filter(timestamp__gte=(now - max_update_delay))


# Filtro responsável por pegar apenas as observações do vôo atual da aeronave
class ObservationFlightFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # 1 hora
        flight_interval = 3600 * 1000

        latest_observations = Observation.objects.filter(
            flight=OuterRef("flight")
        ).order_by("-timestamp")[:1]

        return queryset.filter(
            timestamp__gte=Subquery(latest_observations.values("timestamp")) - flight_interval
        )


# Filtro responsável por pegar informações com um "espaçamento temporal" entre elas
# Por exemplo, pega informações de 5 em 5 minutos descartando as demais, assim retorna
# uma resposta menor
class ObservationPrecisionFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        interval = Util.parseParam(request, "interval", 0)

        if interval == 0:
            return queryset
        
        annotated = queryset.annotate(
            row_number=Window(
                expression=RowNumber(),
                partition=F("flight"),
                order_by=F("timestamp").asc()
            )
        )

        return annotated.filter(row_number__mod=interval)


# Pega apenas as aeronaves em um pedaço do mapa
class MapBoundsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        top_lat = Util.parseParam(request, "top", 90);
        bootom_lat = Util.parseParam(request, "bottom", -90);
        left_lng = Util.parseParam(request, "left", -180);
        right_lng = Util.parseParam(request, "right", 180);

        return queryset.filter(
            point__within=Polygon.from_bbox((left_lng, bootom_lat, right_lng, top_lat))
        )


# Pega apenas as aeronaves em um pedaço do mapa
class FlightClusteringFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        map_height = Util.parseParam(request, "map_height", None)
        map_zoom = Util.parseParam(request, "map_zoom", None)
        min_airplane_distance = Util.parseParam(request, "min_airplane_distance", 50)

        if not map_height or not map_zoom:
            return queryset
        
        earth_circumference = 40075000
        tiles = 2 ** map_zoom

        meters_per_pixel =  (earth_circumference / tiles) / map_height
        min_distance_meters = min_airplane_distance * meters_per_pixel

        # Subquery para encontrar pontos próximos
        nearby_points = queryset.model.objects.filter(
            point__dwithin=(OuterRef('point'), Distance(m=min_distance_meters)),
            pk__lt=OuterRef('pk')
        )

        # Filtra apenas pontos que não têm vizinhos próximos
        return queryset.annotate(
            has_nearby=Exists(nearby_points)
        ).filter(
            has_nearby=False
        )


class AirportTypeZoomFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        zoom = Util.parseParam(request, "zoom", 0)

        if zoom <= 4:
            return queryset.none()
        elif zoom <= 7:
            return queryset.filter(type__in=["large_airport"])
        elif zoom <= 10:
            return queryset.filter(type__in=["large_airport", "medium_airport"])
        elif zoom <= 13:
            return queryset.filter(type__in=["large_airport", "medium_airport", "small_airport"])
        else:
            return queryset


class FlightFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset
