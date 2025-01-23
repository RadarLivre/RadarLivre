import sys

from collector_simulator import CollectorSimulator

user_credentials = ("root", "tsevaoth")
collector_key = sys.argv[1]
lat = float(sys.argv[2])
lon = float(sys.argv[3])
is_airport = bool(sys.argv[4])

adsb_info_url = "http://localhost:8000/api/adsb_info/"
collector_hello_url = f"http://localhost:8000/api/collector/{collector_key}/"

if __name__ == "__main__":
    collector = CollectorSimulator(
        collector_key=collector_key,
        hello_url=collector_hello_url,
        adsb_url=adsb_info_url,
        lat=lat,
        lon=lon,
        user_credentials=user_credentials,
        is_airport=is_airport
    )
    collector.run_collector()