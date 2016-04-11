# -*- coding:utf-8 -*-

from rest_framework.filters import BaseFilterBackend
import time
import datetime
from radarlivre_api.models import AirplaneInfo

import logging
logger = logging.getLogger("radarlivre.debug")

class AirplaneInfoAtualFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        now = (time.time()) * 1000
        
        flightinterval = 60 * 1000
        
        paramValue = clearNumericParam(request, "timestampinterval");
        if paramValue != None and paramValue >= 0:
                flightinterval = paramValue
        
        infos = queryset.filter(timestamp__gte = (now - flightinterval))
        
        return infos

# Filtro responsável por pegar apenas as observações do vôo atual da aeronave
class ObservationFlightFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        flightinterval = 60 * 60 * 1000
        
        paramValue = clearNumericParam(request, "timestampinterval");
        if paramValue != None and paramValue >= 0:
            flightinterval = paramValue
        
        objects = queryset.order_by('timestamp')
        objectsFiltered = []
        
        last = None        
        for o in reversed(objects):
            if last:
                interval = last.timestamp - o.timestamp
                if interval > flightinterval:
                    break
                else:
                    objectsFiltered.append(o.pk)
            else:
                objectsFiltered.append(o.pk)
            
            last = o
                    
        return queryset.filter(pk__in=objectsFiltered).order_by('timestamp')


class ObservationLastTimestampFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        lastTimestamp = 0
        
        paramValue = clearNumericParam(request, "lasttimestamp");
        if paramValue != None and paramValue >= 0:
            lastTimestamp = paramValue
        

        return queryset.filter(timestamp__gt = lastTimestamp)

# Filtro responsável por pegar informações com um "espaçamento temporal" entre elas
# Por exemplo, pega informações de 5 em 5 minutos descartando as demais, assim retorna
# uma resposta menor
class ObservationPrecisionFilter(BaseFilterBackend):
    
    def filter_queryset(self, request, queryset, view):
        
        interval = 0
                
        paramValue = clearNumericParam(request, "precision");
        if paramValue != None and paramValue >= 0:
                interval = paramValue
        
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
    

class MapBoundsFilter(BaseFilterBackend):
    
    def filter_queryset(self, request, queryset, view):
        
        topLat = clearNumericParam(request, "top");
        bottomLat = clearNumericParam(request, "bottom");
        leftLng = clearNumericParam(request, "left");
        rightLng = clearNumericParam(request, "right");
        
        if topLat != None and bottomLat != None and leftLng != None and rightLng != None:            
            infos = queryset.all()
            for info in infos:
                if info.latitude > 180:
                    info.latitude -= 360
                if info.longitude > 180:
                    info.longitude -= 360
                info.save() 
            
            if bottomLat > 180:
                bottomLat -= 360
            
            if topLat > 180:
                topLat -= 360
                
            if leftLng > 180:
                leftLng -= 360
                
            if rightLng > 180:
                rightLng -= 360
            
            infos = queryset\
                .filter(latitude__gte = bottomLat)\
                .filter(latitude__lte = topLat)\
                .filter(longitude__gte = leftLng)\
                .filter(longitude__lte = rightLng)
            
            return infos;
            
        else:
            return queryset
    
    
def clearNumericParam(request, param):
    param = request.GET.get(param)
    
    if param:
        try:
            return float(param)
        except:
            pass
            
    return None
    
    