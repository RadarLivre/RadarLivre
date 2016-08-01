# -*- coding=utf-8 -*-

from rest_framework.filters import DjangoFilterBackend, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from radarlivre_api.models import Airplane, Airport, Flight, Observation, ADSBMessage, HalfObservation, AirplaneInfo,\
    About, Notify, Contrib
from radarlivre_api.models.serializers import AirplaneSerializer, AirportSerializer, FlightSerializer, ObservationSerializer, ADSBMessageSerializer, AirplaneInfoSerializer, HalfObservationSerializer,\
    AboutSerializer, NotifySerializer, ContribSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from radarlivre_api.adsb import decoder
from radarlivre_api.utils import airline_info
from radarlivre_api.views.filters import ObservationPrecisionFilter,\
    ObservationFlightFilter, AirplaneInfoAtualFilter, MapBoundsFilter,\
    ObservationLastTimestampFilter, ContribAtualFilter

import logging

logger = logging.getLogger("radarlivre.log")

def getClientIp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class AirplaneList(ListCreateAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    
class AirplaneDetail(RetrieveUpdateDestroyAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class AirplaneInfoList(ListCreateAPIView):
    queryset = AirplaneInfo.objects.all()
    serializer_class = AirplaneInfoSerializer
    filter_backends = (DjangoFilterBackend, AirplaneInfoAtualFilter, MapBoundsFilter)
    filter_fields = ('airplane', 'flight')
    
class AirplaneInfoDetail(RetrieveUpdateDestroyAPIView):
    queryset = AirplaneInfo.objects.all()
    serializer_class = AirplaneInfoSerializer


class AirportList(ListCreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('prefix', 'name', 'country', 'city', 'latitude', 'longitude', 'altitude')
    
class AirportDetail(RetrieveUpdateDestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class FlightList(ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('airplane', 'origin', 'destine')
    
class FlightDetail(RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


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
    
class ObservationDetail(RetrieveUpdateDestroyAPIView):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer


class HalfObservationList(APIView):
    def get(self, request, format=None):
        halfObservations = HalfObservation.objects.all()
        serializer = HalfObservationSerializer(halfObservations, many=True)
        return Response(serializer.data)
        
    def post(self, request, format=None):
        serializer = HalfObservationSerializer(data=request.data)
        if(serializer.is_valid()):
            
            newHalfObservation = serializer.save()
            newHalfObservation.delete()
            handleHalfObservation(newHalfObservation, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer = HalfObservationSerializer(data=request.data, many=True)
            if(serializer.is_valid()):
                obs = serializer.save()
                
                for newHalfObservation in obs: 
                    
                    newHalfObservation.delete()
                    handleHalfObservation(newHalfObservation, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HalfObservationDetail(RetrieveUpdateDestroyAPIView):
    queryset = HalfObservation.objects.all()
    serializer_class = HalfObservationSerializer

class ADSBMessageList(APIView):
    def get(self, request, format=None):
        adsbMessages = ADSBMessage.objects.all()
        serializer = ADSBMessageSerializer(adsbMessages, many=True)
        return Response(serializer.data)
        
    def post(self, request, format=None):
        serializer = ADSBMessageSerializer(data=request.data)
        if(serializer.is_valid()):
            
            adsbMessage = serializer.save()
            # adsbMessage.delete()
            
            # Getting a new observation from message
            newHalfObservation = decoder.decodeMessage(adsbMessage)
            
            # If observation has no returned None 
            if newHalfObservation:
                handleHalfObservation(newHalfObservation, request)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
def handleHalfObservation(newHalfObservation, request):
                
    # Get the current observation
    currentHalfObservationsList = HalfObservation.objects.filter(airplane=newHalfObservation.airplane)
    
    currentHalfObservation = None
    
    # If current observation not exists, a new will be created
    if len(currentHalfObservationsList) == 0:
        
        currentHalfObservation = HalfObservation()
        currentHalfObservation.airplane = newHalfObservation.airplane
        currentHalfObservation.save()
    else:
        
        currentHalfObservation = currentHalfObservationsList[0]
    
    currentHalfObservation.update(newHalfObservation)
    
    # If the half observation has been completed, will be saved as a final observation
    if currentHalfObservation.isComplete():
        
        # Creating a new airplane
        airplane = Airplane(icao=currentHalfObservation.airplane)
        
        # If the airplane already exists, will be updated
        airplane.save()
        
        # Creating a new Route
        flight = Flight(calsign=currentHalfObservation.flight, airplane=airplane)
        
        # If the route already exists, will be updated
        flight.save()
            
        observation = decoder.fromHalfObservation(currentHalfObservation)
                
        if observation:
            logger.info("Airplane information accepted: " + airplane.icao)
            
            # Creating a new contributor
            contrib = Contrib(
                  ip=getClientIp(request),
                  latitude=currentHalfObservation.latitudeCollector,
                  longitude=currentHalfObservation.longitudeCollector, 
                  timestamp=observation.timestamp
            )
            contrib.save()
            logger.info("Saving contrib: " + contrib.ip)
            
            observation.airplane = airplane
            observation.flight = flight
            
            # Saving the observation
            observation.save()
            
            # Deleting the auxiliary half observation
            currentHalfObservation.delete()
            
            # Updating the airplane info
            airplaneInfo = None
            airplaneInfoList = AirplaneInfo.objects.filter(airplane=airplane)
            
            if len(airplaneInfoList) == 0:
                # # print "Creating a new AirplaneInfo to", airplane.icao
                airplaneInfo = AirplaneInfo(airplane=airplane)
            else:
                # print "Getting AirplaneInfo from", airplane.icao
                airplaneInfo = airplaneInfoList[0]
                
            # airplaneInfo.route =
            
            airlineData = airline_info.identifyAirLineInformation(flight.calsign )
            
            if airlineData:
                airplaneInfo.flight = airlineData["flight"]
                airplaneInfo.airline = airlineData["airline"]
                airplaneInfo.airlineCountry = airlineData["country"]
                
            airplaneInfo.latitude = observation.latitude
            airplaneInfo.longitude = observation.longitude
            airplaneInfo.altitude = observation.altitude
            airplaneInfo.verticalVelocity = observation.verticalVelocity
            airplaneInfo.horizontalVelocity = observation.horizontalVelocity
            airplaneInfo.angle = observation.angle
            airplaneInfo.timestamp = observation.timestamp
            airplaneInfo.save()
            
            # print "AirpoaneInfo Created: ", airplaneInfo
        
        else:
            logger.info("Airplane information rejected: " + airplane.icao)

class AboutList(ListCreateAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    
class AboutDetail(RetrieveUpdateDestroyAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

    
class NotifyList(ListCreateAPIView):
    queryset = Notify.objects.all()
    serializer_class = NotifySerializer
    
class NotifyDetail(RetrieveUpdateDestroyAPIView):
    queryset = Notify.objects.all()
    serializer_class = NotifySerializer

class ContribList(ListCreateAPIView):
    queryset = Contrib.objects.all()
    serializer_class = ContribSerializer
    filter_backends = (DjangoFilterBackend, ContribAtualFilter)

class ContribDetail(RetrieveUpdateDestroyAPIView):
    queryset = Contrib.objects.all()
    serializer_class = ContribSerializer
    