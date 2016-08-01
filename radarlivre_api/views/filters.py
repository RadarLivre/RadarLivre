# -*- coding:utf-8 -*-

from rest_framework.filters import BaseFilterBackend
import time
import logging


logger = logging.getLogger("radarlivre.debug")


# Filtro responsável por pegar apenas as aeronaves mais recentes
class AirplaneInfoAtualFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        # Pega o timestamp atual em milisegundos
        now = int((time.time()) * 1000)
        # Valor padrão o intervalo: 1 min
        maxUpdateDelay = parseParam(request, "max_update_delay", 60 * 1000)
        return queryset.filter(timestamp__gte = (now - maxUpdateDelay))


# Filtro responsável por pegar apenas os contribuintes mais recentes
class ContribAtualFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        # Pega o timestamp atual em milisegundos
        now = int((time.time()) * 1000)
        # Valor padrão o intervalo: 1 min
        maxUpdateDelay = parseParam(request, "max_update_delay", 3600 * 1000)
        
        return queryset.filter(timestamp__gte = (now - maxUpdateDelay))



# Filtro responsável por pegar apenas as observações do vôo atual da aeronave
class ObservationFlightFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        # 1 hora
        flightInterval = 3600 * 1000
        # 1 dia
        baseFlightInterval = 24 * 3600 * 1000
        
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


# Pega todas as observações apartir de um determinado timestamp
class ObservationLastTimestampFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view): 

        firstTimestamp = parseParam(request, "first_timestamp", 0);
        return queryset.filter(timestamp__gt = firstTimestamp)


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

        infos = queryset.all()

        for info in infos:
            if info.longitude > 180:
                info.longitude -= 360
            info.save() 
        
        if bottomLat < -90:
            bottomLat = -90
        
        if topLat > 90:
            topLat = 90
            
        if leftLng < -180:
            leftLng = -180
            
        if rightLng > 180:
            rightLng = 180
        
        infos = queryset\
            .filter(latitude__gte = bottomLat)\
            .filter(latitude__lte = topLat)\
            .filter(longitude__gte = leftLng)\
            .filter(longitude__lte = rightLng)
        
        return infos;
    
    
def parseParam(request, param, defaultValue):
    param = request.GET.get(param)
    
    if param:
        try:
            return float(param)
        except:
            pass
            
    return defaultValue
    
    