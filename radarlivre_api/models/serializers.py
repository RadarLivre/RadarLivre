# -*- coding:utf-8 -*-

from django.contrib.auth.models import User
from rest_framework.fields import ImageField
from rest_framework.serializers import ModelSerializer

from radarlivre_api.models import Airplane, Airport, Flight, Observation, \
    AirplaneInfo, About, Notify, Collector
from rest_framework import serializers


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class CollectorSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    id = serializers.UUIDField(format='hex_verbose', write_only=True)
    class Meta:
        model = Collector
        fields = '__all__'

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
