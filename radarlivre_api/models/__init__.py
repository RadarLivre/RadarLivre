# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import datetime
import uuid
from time import time

import numpy as np
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.core.cache import cache
from django.db import models, transaction
from django.db.models.fields import CharField, DecimalField, IntegerField, BigIntegerField, \
    BooleanField, TextField, DateTimeField, DateField, URLField
from django.db.models.fields.files import ImageField, FileField
from django.db.models.fields.related import ForeignKey, OneToOneField
from imagekit.models.fields import ImageSpecField
from pilkit.processors.resize import ResizeToFill

from radarlivre_api.utils import Math


class SpatialModelMixin:
    def update_spatial_fields(self):
        if self.point and (self.point.x != self.longitude or self.point.y != self.latitude):
            self.longitude = self.point.x
            self.latitude = self.point.y
        elif not self.point and self.latitude and self.longitude:
            self.point = Point(float(self.longitude), float(self.latitude))

    def clean(self):
        super().clean()
        self.update_spatial_fields()


class Collector(SpatialModelMixin, models.Model):
    key = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collectors", null=True)

    latitude = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    longitude = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    timestamp = BigIntegerField(default=0)
    timestampData = BigIntegerField(default=0)

    point = gis_models.PointField(geography=True, srid=4326, null=True, blank=True, spatial_index=True)

    def save(self, *args, **kwargs):
        self.update_spatial_fields()
        super().save(*args, **kwargs)

    def getDate(self):
        return datetime.datetime.fromtimestamp(
            int(self.timestamp / 1000)
        ).strftime('%d/%m/%Y %H:%M:%S')

    def getStrLatitude(self):
        return "%.8f" % self.latitude

    def getStrLongitude(self):
        return "%.8f" % self.longitude

    def __unicode__(self):
        return "Active collector from " + self.user.username


class Airline(models.Model):
    name = CharField(max_length=255, blank=True, null=True, default="")
    alias = CharField(max_length=255, blank=True, null=True, default="")
    iata = CharField(max_length=4, blank=True, null=True, default="")
    icao = CharField(max_length=8, blank=True, null=True, default="")
    callsign = CharField(max_length=255, blank=True, null=True, default="")
    country = CharField(max_length=255, blank=True, null=True, default="")
    active = BooleanField(default=True)


class Flight(models.Model):
    # Flight identification
    code = CharField(max_length=16, blank=True, null=True, default=True)
    airline = ForeignKey(Airline, null=True, related_name="flights", on_delete=models.PROTECT)

    def __unicode__(self):
        return "Flight " + str(self.code)


class Airport(SpatialModelMixin, models.Model):
    # Airport identification
    code = CharField(max_length=100, blank=True, default='', null=True)
    name = CharField(max_length=100, blank=True, default='', null=True)

    # Airport location
    country = CharField(max_length=100, blank=True, default='', null=True)
    state = CharField(max_length=100, blank=True, default='', null=True)
    city = CharField(max_length=100, blank=True, default='', null=True)
    latitude = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    longitude = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    point = gis_models.PointField(geography=True, srid=4326, null=True, blank=True, spatial_index=True)

    type = CharField(max_length=100, blank=True, default='', null=True)

    def save(self, *args, **kwargs):
        self.update_spatial_fields()
        super().save(*args, **kwargs)

    def __unicode__(self):
        return "Airport " + self.code + " - " + self.name


class ADSBInfo(SpatialModelMixin, models.Model):
    collectorKey = models.CharField(max_length=64, blank=True, null=True, default="")

    modeSCode = CharField(max_length=16, blank=True, null=True, default="")
    callsign = CharField(max_length=16, blank=True, null=True, default="")

    # Airplane position
    latitude = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    longitude = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    altitude = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    point = gis_models.PointField(geography=True, srid=4326, null=True, blank=True, spatial_index=True)
    
    # Airplane velocity
    verticalVelocity = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    horizontalVelocity = DecimalField(max_digits=20, decimal_places=10, default=0.0)

    # Airplane angle
    groundTrackHeading = DecimalField(max_digits=20, decimal_places=10, default=0.0)

    # Observation date time generated by server
    timestamp = BigIntegerField(default=0)
    timestampSent = BigIntegerField(default=0)

    # Originals ADS-B messages
    messageDataId = CharField(max_length=100, blank=True, default='')
    messageDataPositionEven = CharField(max_length=100, blank=True, default='')
    messageDataPositionOdd = CharField(max_length=100, blank=True, default='')
    messageDataVelocity = CharField(max_length=100, blank=True, default='')

    def save(self, *args, **kwargs):
        self.update_spatial_fields()
        super().save(*args, **kwargs)


class Observation(SpatialModelMixin, models.Model):
    flight = ForeignKey(Flight, db_index=True, null=True, blank=True, default=None,
                        related_name='observations', on_delete=models.PROTECT)
    adsbInfo = OneToOneField(ADSBInfo, related_name="observation", null=True, on_delete=models.PROTECT)

    # Airplane position
    latitude = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    longitude = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    altitude = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    point = gis_models.PointField(geography=True, srid=4326, null=True, blank=True, spatial_index=True)

    # Airplane velocity
    verticalVelocity = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    horizontalVelocity = DecimalField(max_digits=20, decimal_places=10, default=0.0)

    # Airplane angle
    groundTrackHeading = DecimalField(max_digits=20, decimal_places=10, default=0.0)

    # Observation date time generated by server
    timestamp = BigIntegerField(default=0, db_index=True)

    simulated = BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.update_spatial_fields()
        super().save(*args, **kwargs)

    def __unicode__(self):
        return "Observation of flight " + str(self.flight.code)

    @staticmethod
    def generateFromADSBInfo(info):
        try:
            collector = Collector.objects.get(key=info.collectorKey)
        except Collector.DoesNotExist:
            return None

        callsign = info.callsign
        airlineICAO = callsign[:3]

        def get_airline():
            try:
                return Airline.objects.get(icao=airlineICAO)
            except:
                return None
            
        airline = cache.get_or_set(
            f"airline_icao_{airlineICAO}",
            get_airline(),
            3600
        )

        # Bulk create/update for flight
        flight, _ = Flight.objects.select_for_update().get_or_create(
            code=callsign,
            defaults={'airline': airline}
        )

        # Calculate timestamp once
        timestamp = int(time() * 1000) - (info.timestampSent - info.timestamp)

        # Update longitude in memory before saving
        if info.longitude > 180:
            info.longitude -= 360

        # Batch updates
        with transaction.atomic():
            info.save()
            
            # Update collector timestamp in bulk
            Collector.objects.filter(key=info.collectorKey).update(
                timestampData=timestamp
            )

            # Create observation
            obs = Observation(
                flight=flight,
                adsbInfo=info,
                timestamp=timestamp,
                point=info.point,
                altitude=info.altitude,
                verticalVelocity=info.verticalVelocity,
                horizontalVelocity=info.horizontalVelocity,
                groundTrackHeading=info.groundTrackHeading
            )
            obs.save()
    
        return obs


class FlightInfo(SpatialModelMixin, models.Model):
    # Flight identification
    flight = OneToOneField(Flight, null=True, on_delete=models.CASCADE)
    airline = ForeignKey(Airline, null=True, on_delete=models.PROTECT)

    # Airplane position
    latitude = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    longitude = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    altitude = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    point = gis_models.PointField(geography=True, srid=4326, null=True, blank=True, spatial_index=True)

    # Airplane velocity
    verticalVelocity = DecimalField(max_digits=20, decimal_places=10, default=0.0)
    horizontalVelocity = DecimalField(max_digits=20, decimal_places=10, default=0.0)

    # Airplane angle
    groundTrackHeading = DecimalField(max_digits=20, decimal_places=10, default=0.0)

    # Observation date time generated by server
    timestamp = BigIntegerField(default=0, db_index=True)

    def save(self, *args, **kwargs):
        self.update_spatial_fields()
        super().save(*args, **kwargs)

    @staticmethod
    def generateFromFlight(flight, obs):
        FlightInfo.objects.update_or_create(
            flight=flight,
            defaults={
                'airline': flight.airline,
                'altitude': obs.altitude,
                'point': obs.point,
                'latitude': obs.latitude,
                'longitude': obs.longitude,
                'verticalVelocity': obs.verticalVelocity,
                'horizontalVelocity': obs.horizontalVelocity,
                'groundTrackHeading': obs.groundTrackHeading,
                'timestamp': obs.timestamp  
            }
        ) 

    def generatePropagatedTrajectory(self, propCount, propInterval):
        Observation.objects.filter(
            flight=self.flight,
            simulated=True
        ).delete()

        observations = list(Observation.objects.filter(flight=self.flight)
                            .select_related('flight')
                            .order_by("-timestamp")[:2])
        
        if len(observations) < 2:
            return []
        
        R = 6371000.0  # Earth radius in meters
        propIntervalSec = propInterval / 1000.0
        
        obs_array = np.array([(o['latitude'], o['longitude'], o['altitude'],
                            o['groundTrackHeading'], o['horizontalVelocity'],
                            o['verticalVelocity'], o['timestamp']) 
                            for o in observations], 
                            dtype=np.float64)
        
        # Converter para arrays NumPy
        timestamps = np.array([o.timestamp for o in observations], dtype=np.float64)
        velocities = np.array([Math.knotsToMetres(o.horizontalVelocity) for o in observations], dtype=np.float64)
        headings = np.radians([o.groundTrackHeading for o in observations])
        lats = np.radians([o.latitude for o in observations])
        lons = np.radians([o.longitude for o in observations])
        alts = np.array([o.altitude for o in observations], dtype=np.float64)
        v_velocities = np.array([o.verticalVelocity for o in observations], dtype=np.float64)

        # Cálculos vetorizados
        dt = propInterval / 1000.0
        n_steps = int(propCount)
        R = 6371000.0  # Raio da Terra
        
        # Alocar arrays para resultados
        new_lats = np.zeros(n_steps)
        new_lons = np.zeros(n_steps)
        new_alts = np.zeros(n_steps)
        new_headings = np.zeros(n_steps)
        
        # Calcular taxa de variação inicial
        time_diff = (timestamps[1] - timestamps[0]) / 1000.0
        heading_diff = headings[1] - headings[0]
        turn_rate = heading_diff / time_diff if time_diff != 0 else 0
        
        # Vetorizar cálculos principais
        current_velocity = velocities[-1]
        current_heading = headings[-1]
        current_lat = lats[-1]
        current_lon = lons[-1]
        current_alt = alts[-1]
        current_v_velocity = v_velocities[-1]
        
        # Gerar todos os passos de uma vez
        steps = np.arange(1, n_steps + 1)
        time_steps = dt * steps
        
        # Cálculo de headings
        new_headings = current_heading + (turn_rate * time_steps)
        
        # Cálculo de distâncias
        distances = current_velocity * time_steps
        
        # Cálculo de latitudes/longitudes
        new_lats = np.arcsin(
            np.sin(current_lat) * np.cos(distances/R) +
            np.cos(current_lat) * np.sin(distances/R) * np.cos(new_headings)
        )
        
        new_lons = current_lon + np.arctan2(
            np.sin(new_headings) * np.sin(distances/R) * np.cos(current_lat),
            np.cos(distances/R) - np.sin(current_lat) * np.sin(new_lats)
        )
        
        # Conversão para graus
        new_lats_deg = np.degrees(new_lats)
        new_lons_deg = np.degrees(new_lons)
        
        # Cálculo de altitudes
        new_alts = current_alt + (current_v_velocity * time_steps)
        
        # Criar objetos em lote
        observations_to_create = [
            Observation(
                flight=self.flight,
                latitude=new_lats_deg[i],
                longitude=new_lons_deg[i],
                altitude=new_alts[i],
                groundTrackHeading=np.degrees(new_headings[i]),
                verticalVelocity=self.verticalVelocity,
                horizontalVelocity=self.horizontalVelocity,
                timestamp=self.timestamp + int(propInterval * (i + 1)),
                simulated=True
            )
            for i in range(n_steps)
        ]
        
        created_obs = Observation.objects.bulk_create(observations_to_create)
        
        return created_obs


# Used to store project information
class About(models.Model):
    title = CharField(max_length=1000, blank=True, default="")
    subtitle = CharField(max_length=1000, blank=True, default="")
    info = TextField(blank=True, default="")

    index = IntegerField(default=0)

    externURL = URLField(verbose_name="Extern link", default="", blank=True)

    image = ImageField(upload_to="about_images", null=True)

    largeImage = ImageSpecField(source="image",
                                processors=[ResizeToFill(1920, 1080)],
                                format='JPEG',
                                options={'quality': 75, 'progressive': True})

    mediumImage = ImageSpecField(source="image",
                                 processors=[ResizeToFill(1280, 720)],
                                 format='JPEG',
                                 options={'quality': 75, 'progressive': True})

    smallImage = ImageSpecField(source="image",
                                processors=[ResizeToFill(640, 360)],
                                format='JPEG',
                                options={'quality': 75, 'progressive': True})

    def getShortDescription(self):
        return str(self.title + " - " + self.subtitle[:50] + "...")

    def toHTML(self):
        return self.info.replace("<p", "<p class=\"rl-document__paragraph\"") \
            .replace("<span", "<span class=\"rl-document__title\"")

    def __unicode__(self):
        return self.title + " - " + self.subtitle


# Send notify to all app's
class Notify(models.Model):
    title = CharField(max_length=1000, blank=True, default="")
    subtitle = CharField(max_length=1000, blank=True, default="")
    info = TextField(blank=True, default="")

    showDate = DateTimeField()

    vibrate = BooleanField(default=True)
    song = BooleanField(default=False)

    def __unicode__(self):
        return self.title + " - " + self.subtitle


# Radar Livre Softwares
class Software(models.Model):
    title = CharField(max_length=1000, blank=True, default="")

    versionName = CharField(max_length=1000, blank=True, default="")
    versionCode = IntegerField(default=0)

    lastUpdate = DateField(default=0)

    executable = FileField(
        upload_to="softwares/collector"
    )
