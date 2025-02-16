# -*- coding:utf-8 -*-

qfrom decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework.fields import ImageField
from rest_framework.serializers import ModelSerializer

from radarlivre_api.models import Airport, Flight, Observation, \
    About, Notify, Collector, Airline, ADSBInfo, FlightInfo


class SpatialCompatibleSerializer(serializers.ModelSerializer):  
    def to_internal_value(self, data):
        for field in ['latitude', 'longitude']:
            if field in data and isinstance(data[field], str):
                data[field] = Decimal(data[field])

        if 'latitude' in data and 'longitude' in data:    
            data['point'] = Point(
                float(data['longitude']), 
                float(data['latitude'])
            )    

        return super().to_internal_value(data)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class CollectorSerializer(SpatialCompatibleSerializer):
    user = UserSerializer(read_only=True)
    key = serializers.UUIDField(format='hex_verbose', write_only=True)

    class Meta:
        model = Collector
        fields = '__all__'
        extra_kwargs = {
            'point': {'write_only': True}
        }


class AirlineSerializer(ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'


class ObservationSerializer(SpatialCompatibleSerializer):
    class Meta:
        model = Observation
        fields = '__all__'
        extra_kwargs = {
            'point': {'write_only': True}
        }


class FlightSerializer(ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'


class FlightInfoSerializer(SpatialCompatibleSerializer):
    airline = AirlineSerializer(read_only=True)
    lastObservation = ObservationSerializer(read_only=True)
    flight = FlightSerializer(read_only=True)

    class Meta:
        model = FlightInfo
        fields = '__all__'
        extra_kwargs = {
            'point': {'write_only': True}
        }


class AirportSerializer(SpatialCompatibleSerializer):
    class Meta:
        model = Airport
        fields = '__all__'
        extra_kwargs = {
            'point': {'write_only': True}
        }


class ADSBInfoSerializer(SpatialCompatibleSerializer):
    class Meta:
        model = ADSBInfo
        fields = '__all__'
        extra_kwargs = {
            'point': {'write_only': True}
        }


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
