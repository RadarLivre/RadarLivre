# -*- coding:utf-8 -*-

from rest_framework.serializers import ModelSerializer
from radarlivre_api.models import Airplane, Airport, Flight, Observation, ADSBMessage,\
    AirplaneInfo, HalfObservation, About, Notify, Contrib
from rest_framework.fields import ImageField

class AirplaneSerializer(ModelSerializer):
    class Meta:
        model = Airplane
        fields = '__all__'
        
class AirplaneInfoSerializer(ModelSerializer):
    class Meta:
        model = AirplaneInfo
        fields = '__all__'
        
class AirportSerializer(ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'
        
class FlightSerializer(ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'
        
class ObservationSerializer(ModelSerializer):
    class Meta:
        model = Observation
        fields = '__all__'
        
class HalfObservationSerializer(ModelSerializer):
    class Meta:
        model = HalfObservation
        fields = '__all__'
        
class ADSBMessageSerializer(ModelSerializer):
    class Meta:
        model = ADSBMessage 
        fields = '__all__'
        
class AboutSerializer(ModelSerializer):
    smallImage = ImageField()
    mediumImage = ImageField()
    largeImage = ImageField()
    class Meta:
        model = About 
        fields = ['title', 'subtitle', 'info', 'largeImage', 'mediumImage', 'smallImage']
        
class NotifySerializer(ModelSerializer):
    class Meta:
        model = Notify 
        fields = '__all__'

class ContribSerializer(ModelSerializer):
    class Meta:
        model = Contrib
        fields = '__all__'