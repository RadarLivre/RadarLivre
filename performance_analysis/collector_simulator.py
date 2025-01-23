import random
import math
import threading
import time
import uuid

import requests

from aircraft_simulator import AircraftSimulator


class CollectorSimulator:
    def __init__(
            self,
            collector_key: str,
            lat: float,
            lon: float,
            hello_url: str,
            adsb_url: str,
            user_credentials: tuple[str, str],
            radius_km: float = 70,
            is_airport: bool = False
    ):
        self.collector_key = collector_key
        self.lat = lat
        self.lon = lon
        self.radius_km = radius_km
        self.is_airport = is_airport
        self.hello_url = hello_url
        self.adsb_url = adsb_url
        self.user_credentials = user_credentials
        self.angle_tracker = set()
        self.avg_interval = random.uniform(30, 300)

    def generate_unique_angle(self):
        while True:
            angle = random.uniform(0, 2 * math.pi)
            if angle not in self.angle_tracker:
                self.angle_tracker.add(angle)
                return angle

    def generate_random_coordinates_on_perimeter(self) -> (float, float):
        radius_deg = self.radius_km / 111
        angle = random.uniform(0, 2 * math.pi)
        lat = self.lat + radius_deg * math.cos(angle)
        lon = self.lon + radius_deg * math.sin(angle) / math.cos(math.radians(self.lat))
        return lat, lon

    def generate_aircraft_coordinates(self) -> (float, float, float, float):
        start_lat, start_lon = self.generate_random_coordinates_on_perimeter()
        if self.is_airport:
            end_lat, end_lon = self.lat, self.lon
        else:
            end_lat, end_lon = self.generate_random_coordinates_on_perimeter()
        return start_lat, start_lon, end_lat, end_lon

    def send_hello(self):
        hello_data = {"id": self.collector_key}
        print("Sending collector hello key={id}".format(**hello_data))
        response = requests.put(self.hello_url, auth=self.user_credentials)
        print(response.status_code)

    def send_adsb_data(self, adsb_data):
        response = requests.post(self.adsb_url, json=[adsb_data], auth=self.user_credentials)
        print(f"ADSB Response: {response.status_code}, {response.text}")

    def manage_aircraft(self):
        while True:
            start_lat, start_lon, end_lat, end_lon = self.generate_aircraft_coordinates()
            simulator = AircraftSimulator(
                mode_s_code="",
                callsign=uuid.uuid4().hex[:4].upper(),
                start_lat=start_lat,
                start_lon=start_lon,
                end_lat=end_lat,
                end_lon=end_lon,
                altitude=10000
            )
            thread = threading.Thread(target=self.simulate_aircraft, args=(simulator,))
            thread.start()

            next_interval = random.expovariate(1 / self.avg_interval)
            print(f"Next aircraft in {next_interval:.2f} seconds")
            time.sleep(next_interval)

    def simulate_aircraft(self, simulator: AircraftSimulator):
        while not simulator.has_reached_destination():
            adsb_data = simulator.generate_adsb_data(self.collector_key)
            self.send_adsb_data(adsb_data)
            time.sleep(1.5)

    def run_collector(self):
        threading.Thread(target=self.manage_aircraft, daemon=True).start()

        while True:
            self.send_hello()
            time.sleep(5)