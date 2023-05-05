import codecs
from json import loads
from os.path import join, dirname

from django.db import migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('radarlivre_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=lambda *args: insert_data(*args)
        ),
    ]


def insert_data(apps, *args):
    with codecs.open(join(dirname(__file__), "raw_data/airports_and_airlines.json")) as file:
        data = loads(file.read())

    airport_model = apps.get_model("radarlivre_api", "Airport")
    airline_model = apps.get_model("radarlivre_api", "Airline")

    [airport_model.objects.create(**row) for row in data["airports"]]
    [airline_model.objects.create(**row) for row in data["airlines"]]


