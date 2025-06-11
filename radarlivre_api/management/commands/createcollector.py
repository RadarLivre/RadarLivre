from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandError

from radarlivre_api.models import Collector


class Command(BaseCommand):
    help = "Create a new RadarLivreAPI Collector model"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)
        parser.add_argument("collector_latitude", type=float)
        parser.add_argument("collector_longitude", type=float)

    def handle(self, *args, **options):
        username = options["username"]
        latitude = options["collector_latitude"]
        longitude = options["collector_longitude"]
        collector_key = None

        try:
            user = User.objects.get(username=username)
            new_collector = Collector(user=user, latitude=latitude, longitude=longitude)
            new_collector.save()
            collector_key = new_collector.key
        except User.DoesNotExist:
            CommandError(f"User {username} does not exists")

        self.stdout.write(
            self.style.SUCCESS(f"Collector with id {collector_key} was created")
        )
