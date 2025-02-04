import logging
import random
import time
import requests
import json
from threading import Thread
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="{levelname} | {asctime} | {name} | {message}",
    style="{",
    handlers=[
        RotatingFileHandler("web_clients_action.log"),
        logging.StreamHandler(),
    ],
)


class WebClientSimulator:
    def __init__(self, client_id):
        self.client_id = client_id
        self.base_url = "http://localhost:8000/api"
        self.selected_flight = None
        self.enable_observations = random.choice([True, False])
        self.logger = logging.getLogger(f"WebClient-{self.client_id}")

        self.bounding_box = {
            "top": 18.204756443706668,
            "bottom": -26.06030440392178,
            "left": -70.46312175250968,
            "right": -32.71409831500968
        }

    def log_request(self, endpoint: str, status: str, duration: float):
        self.logger.info(f"{endpoint},{status},{duration:.2f}")

    def log_error(self, endpoint: str, error: str, duration: float):
        self.logger.error(f"{endpoint},ERROR,{duration:.2f},{error}")

    def make_request(self, endpoint: str, params: dict):
        start_time = time.time()
        try:
            params.update({
                "format": "jsonp",
                "callback": "_jqjsp",
                f"_{int(time.time() * 1000)}": ""
            })

            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            duration = (time.time() - start_time) * 1000

            if response.status_code == 200:
                self.log_request(endpoint, str(response.status_code), duration)
                return self.parse_jsonp(response.text)

            self.log_error(endpoint, f"HTTP {response.status_code}", duration)
            return None

        except Exception as e:
            duration = (time.time() - start_time) * 1000
            self.log_error(endpoint, str(e), duration)
            return None

    def parse_jsonp(self, response):
        try:
            return json.loads(response[response.index("(") + 1:-2])
        except:
            return None

    def run_collector_polling(self):
        while True:
            self.make_request("collector/", {"max_update_delay": ""})
            time.sleep(5)

    def run_flight_polling(self):
        while True:
            data = self.make_request("flight_info/", {
                **self.bounding_box,
                "map_height": 1036,
                "map_zoom": 5,
                "min_airplane_distance": 0
            })

            if data and "results" in data and data["results"]:
                self.selected_flight = random.choice(data["results"])["flight"]

            time.sleep(10)

    def run_airport_request(self):
        self.make_request("airport/", {
            "zoom": 9,
            **self.bounding_box
        })

    def run_observation_polling(self):
        while True:
            if self.selected_flight:
                self.make_request("observation/", {
                    "flight": self.selected_flight,
                    "interval": ""
                })
            time.sleep(random.randint(5, 15))

    def start(self):
        Thread(target=self.run_collector_polling).start()
        Thread(target=self.run_flight_polling).start()
        self.run_airport_request()

        if self.enable_observations:
            Thread(target=self.run_observation_polling).start()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python3 web_client_simulator.py <client_id>")
        sys.exit(1)

    client = WebClientSimulator(sys.argv[1])
    client.start()

    while True:
        time.sleep(3600)