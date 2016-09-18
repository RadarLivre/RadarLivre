# -*- coding:utf-8 -*-

from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from rest_framework.fields import ImageField
from rest_framework.serializers import ModelSerializer

from radarlivre_api.models import Airport, Flight, Observation, \
    About, Notify, Collector, Airline, ADSBInfo, FlightInfo
from rest_framework import serializers


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class CollectorSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    key = serializers.UUIDField(format='hex_verbose', write_only=True)
    class Meta:
        model = Collector
        fields = '__all__'

class AirlineSerializer(ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'

class ObservationSerializer(ModelSerializer):
    class Meta:
        model = Observation
        fields = '__all__'


class FlightSerializer(ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class FlightInfoSerializer(ModelSerializer):
    airline = AirlineSerializer(read_only=True)
    lastObservation = ObservationSerializer(read_only=True)
    flight = FlightSerializer(read_only=True)
    class Meta:
        model = FlightInfo
        fields = '__all__'


class AirportSerializer(ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class ADSBInfoSerializer(ModelSerializer):

    class Meta:
        model = ADSBInfo
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
