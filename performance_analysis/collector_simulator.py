import logging
import math
import random
import threading
import time
import uuid
from logging.handlers import RotatingFileHandler

import requests

from aircraft_simulator import AircraftSimulator

logging.basicConfig(
    level=logging.INFO,
    format="{levelname} | {asctime} | {name} | {message}",
    style="{",
    handlers=[
        RotatingFileHandler("collectors_action.log"),
        logging.StreamHandler(),
    ],
)

class CollectorSimulator:
    def __init__(
            self,
            collector_key: str,
            lat: float,
            lon: float,
            hello_url: str,
            adsb_url: str,
            user_credentials: tuple[str, str],
            is_airport: bool = False
    ):
        self.collector_key = collector_key
        self.lat = lat
        self.lon = lon
        self.radius_km = int(random.uniform(100, 300))
        self.is_airport = is_airport
        self.hello_url = hello_url
        self.adsb_url = adsb_url
        self.user_credentials = user_credentials
        self.angle_tracker = set()
        self.avg_interval = random.uniform(30, 300)
        self.action_logger = logging.getLogger(f"Collector-{self.collector_key}")
        
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
        start_time = time.time()
        try:
            response = requests.put(self.hello_url, auth=self.user_credentials)
            duration_ms = (time.time() - start_time) * 1000
            self.action_logger.info(f"HELLO,{response.status_code},{duration_ms:.2f}")
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.action_logger.error(f"HELLO,ERROR,{duration_ms:.2f},{str(e)}")

    def send_adsb_data(self, adsb_data):
        start_time = time.time()
        try:
            response = requests.post(self.adsb_url, json=[adsb_data], auth=self.user_credentials)
            duration_ms = (time.time() - start_time) * 1000
            self.action_logger.info(f"ADSB,{response.status_code},{duration_ms:.2f}")
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.action_logger.error(f"ADSB,ERROR,{duration_ms:.2f},{str(e)}")

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
            self.action_logger.info(f"Próxima aeronave em {next_interval:.2f} segundos")
            time.sleep(next_interval)

    def simulate_aircraft(self, simulator: AircraftSimulator):
        while not simulator.has_reached_destination():
            adsb_data = simulator.generate_adsb_data(self.collector_key)
            self.send_adsb_data(adsb_data)
            time.sleep(1.5)

    def run_collector(self):
        self.action_logger.info(f"Iniciando coletor: {self.collector_key}")
        threading.Thread(target=self.manage_aircraft, daemon=True).start()

        while True:
            self.send_hello()
            time.sleep(5)