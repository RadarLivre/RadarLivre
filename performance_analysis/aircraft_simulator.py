import math
import uuid
from time import time
from random import random, uniform
from typing import Dict, Any

class AircraftSimulator:
    def __init__(self, mode_s_code: str, callsign: str, start_lat: float, start_lon: float, end_lat: float, end_lon: float, altitude: float):
        self.mode_s_code = mode_s_code
        self.callsign = callsign
        self.lat = start_lat
        self.lon = start_lon
        self.end_lat = end_lat
        self.end_lon = end_lon
        self.altitude = altitude
        self.vertical_velocity = uniform(-500, 500)
        self.horizontal_velocity = uniform(300, 900)
        self.ground_track_heading = self.calculate_initial_heading()

    def calculate_initial_heading(self) -> float:
        delta_lon = math.radians(self.end_lon - self.lon)
        start_lat_rad = math.radians(self.lat)
        end_lat_rad = math.radians(self.end_lat)

        x = math.sin(delta_lon) * math.cos(end_lat_rad)
        y = math.cos(start_lat_rad) * math.sin(end_lat_rad) - \
            math.sin(start_lat_rad) * math.cos(end_lat_rad) * math.cos(delta_lon)

        azimuth = math.atan2(x, y)
        return math.degrees(azimuth) % 360

    def update_position(self):
        self.ground_track_heading = self.calculate_initial_heading()

        self.horizontal_velocity += uniform(-5, 5)
        self.horizontal_velocity = max(200, min(self.horizontal_velocity, 900))

        self.altitude += self.vertical_velocity * 0.1
        self.altitude = max(0, self.altitude)
        self.vertical_velocity += uniform(-50, 50)

        distance = self.horizontal_velocity * 0.1 / 3600
        self.lat += distance * math.cos(math.radians(self.ground_track_heading))
        self.lon += distance * math.sin(math.radians(self.ground_track_heading))

    def has_reached_destination(self, tolerance=0.01):
        lat_diff = abs(self.lat - self.end_lat)
        lon_diff = abs(self.lon - self.end_lon)
        return lat_diff < tolerance and lon_diff < tolerance

    def generate_adsb_data(self, collector_key):
        self.update_position()
        timestamp = int(time())
        message_id = uuid.uuid4().hex
        return {
            "collectorKey": collector_key,
            "modeSCode": self.mode_s_code,
            "callsign": self.callsign,
            "latitude": f"{self.lat:.7f}",
            "longitude": f"{self.lon:.7f}",
            "altitude": round(self.altitude, 9),
            "verticalVelocity": round(self.vertical_velocity, 9),
            "horizontalVelocity": self.horizontal_velocity,
            "groundTrackHeading": self.ground_track_heading,
            "timestamp": timestamp,
            "timestampSent": timestamp,
            "messageDataId": message_id,
            "messageDataPositionEven": message_id[:20] + "EVEN",
            "messageDataPositionOdd": message_id[:20] + "ODD",
            "messageDataVelocity": message_id[:20] + "VEL"
        }