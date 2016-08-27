# -*- coding:utf-8 -*-
import math
from django.db.models.aggregates import Max
from rest_framework.filters import BaseFilterBackend
import time
import logging

from radarlivre_api.models import Observation

logger = logging.getLogger("radarlivre.debug")


# Filtro responsável por pegar apenas os itens mais recentes
class MaxUpdateDelayFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        # Pega o timestamp atual em milisegundos
        now = int((time.time()) * 1000)
        # Valor padrão o intervalo: 1 min
        maxUpdateDelay = parseParam(request, "max_update_delay", 1 * 60 * 1000)
        return queryset.filter(timestamp__gte = (now - maxUpdateDelay))

# Filtro responsável por pegar apenas as observações do vôo atual da aeronave
class ObservationFlightFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        # 1 hora
        flightInterval = 3600 * 1000
        
        objects = queryset.order_by('timestamp')
        objectsFiltered = []
        
        last = None        
        for o in reversed(objects):
            if last:
                interval = last.timestamp - o.timestamp
                if interval > flightInterval:
                    break
                else:
                    objectsFiltered.append(o.pk)
            else:
                objectsFiltered.append(o.pk)
            
            last = o
                    
        return queryset.filter(pk__in=objectsFiltered).order_by('timestamp')


# Filtro responsável por pegar informações com um "espaçamento temporal" entre elas
# Por exemplo, pega informações de 5 em 5 minutos descartando as demais, assim retorna
# uma resposta menor
class ObservationPrecisionFilter(BaseFilterBackend):
    
    def filter_queryset(self, request, queryset, view):
        
        interval = parseParam(request, "interval", 0);
        
        if interval == 0:
            return queryset.all()
        
        objects = queryset.all()
        objectsFiltered = []
        
        last = None
        for o in objects:
            
            if len(objectsFiltered) == 0:
                
                objectsFiltered.append(o.pk)
                last = o
                
            else:
                
                currentInterval = o.timestamp - last.timestamp
                
                if currentInterval >= interval:
                    objectsFiltered.append(o.pk)
                    last = o               
        
        
        return queryset.filter(pk__in=objectsFiltered).order_by('timestamp')
    

# Pega apenas as aeronaves em um pedaço do mapa
class MapBoundsFilter(BaseFilterBackend):
    
    def filter_queryset(self, request, queryset, view):
        
        topLat = parseParam(request, "top", 90);
        bottomLat = parseParam(request, "bottom", -90);
        leftLng = parseParam(request, "left", -180);
        rightLng = parseParam(request, "right", 180);

        return queryset\
            .filter(latitude__gte = bottomLat)\
            .filter(latitude__lte = topLat)\
            .filter(longitude__gte = leftLng)\
            .filter(longitude__lte = rightLng)


# Pega apenas as aeronaves em um pedaço do mapa
class FlightClusteringFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        mapHeight = parseParam(request, "map_height", None)
        mapZoom = parseParam(request, "map_zoom", None)
        minAirplaneDistance = parseParam(request, "min_airplane_distance", 50)

        if mapHeight and mapZoom:
            print "Clustering..."

            def min(a, b):
                return a if a < b else b;

            def max(a, b):
                return a if a > b else b;

            def getProjection(latlng, mapHeight):
                pass

                siny = math.sin(latlng["lat"] * math.pi / 180.0)
                siny = min(max(siny, -0.9999), 0.9999)

                return {
                    "x": mapHeight * (0.5 + latlng["lng"] / 360),
                    "y": mapHeight * (0.5 - math.log((1 + siny) / (1 - siny)) / (4 * math.pi))
                }

            def getPixelCoordinate(latlng, mapHeigth, mapZoom):
                scale = 1 << int(mapZoom);
                worldCoordinate = getProjection(latlng, mapHeigth);

                pixelCoordinate = {
                    "x": math.floor(worldCoordinate["x"] * scale),
                    "y": math.floor(worldCoordinate["y"] * scale)
                }

                return pixelCoordinate;

            def getDistanceBetween(pos1, pos2, mapHeight, mapZoom):
                a = getPixelCoordinate(pos1, mapHeight, mapZoom);
                b = getPixelCoordinate(pos2, mapHeight, mapZoom);
                return math.sqrt(math.pow(a["x"] - b["x"], 2) + math.pow(a["y"] - b["y"], 2));

            infos = queryset.all()
            wrappedInfos = []

            for i in infos:
                wrappedInfos.append({
                    "id": i.pk,
                    "info": i,
                    "toHide": False
                })

            for i in wrappedInfos:
                for j in wrappedInfos:
                    if not i["id"] == j["id"] and not i["toHide"]:
                        d = getDistanceBetween(
                            {"lat": float(i["info"].latitude), "lng": float(i["info"].longitude)},
                            {"lat": float(j["info"].latitude), "lng": float(j["info"].longitude)},
                            mapHeight,
                            mapZoom
                        )

                        if d <= minAirplaneDistance:
                            j["toHide"] = True

            toShow = [i["id"] for i in wrappedInfos if not i["toHide"]]

            return queryset.filter(pk__in=toShow)

        else:
            return queryset



class AirportTypeZoomFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):

        zoom = parseParam(request, "zoom", 0)

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
    
def parseParam(request, param, defaultValue):
    param = request.GET.get(param)
    
    if param:
        try:
            return float(param)
        except:
            pass
            
    return defaultValue
    
    