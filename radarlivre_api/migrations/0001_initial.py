# Generated by Django 4.2.1 on 2023-05-05 08:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=1000)),
                ('subtitle', models.CharField(blank=True, default='', max_length=1000)),
                ('info', models.TextField(blank=True, default='')),
                ('index', models.IntegerField(default=0)),
                ('externURL', models.URLField(blank=True, default='', verbose_name='Extern link')),
                ('image', models.ImageField(null=True, upload_to='about_images')),
            ],
        ),
        migrations.CreateModel(
            name='ADSBInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collectorKey', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('modeSCode', models.CharField(blank=True, default='', max_length=16, null=True)),
                ('callsign', models.CharField(blank=True, default='', max_length=16, null=True)),
                ('latitude', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('longitude', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('altitude', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('verticalVelocity', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('horizontalVelocity', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('groundTrackHeading', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('timestamp', models.BigIntegerField(default=0)),
                ('timestampSent', models.BigIntegerField(default=0)),
                ('messageDataId', models.CharField(blank=True, default='', max_length=100)),
                ('messageDataPositionEven', models.CharField(blank=True, default='', max_length=100)),
                ('messageDataPositionOdd', models.CharField(blank=True, default='', max_length=100)),
                ('messageDataVelocity', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('alias', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('iata', models.CharField(blank=True, default='', max_length=4, null=True)),
                ('icao', models.CharField(blank=True, default='', max_length=8, null=True)),
                ('callsign', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('state', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('city', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('latitude', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('longitude', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('type', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default=True, max_length=16, null=True)),
                ('airline', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='flights', to='radarlivre_api.airline')),
            ],
        ),
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=1000)),
                ('subtitle', models.CharField(blank=True, default='', max_length=1000)),
                ('info', models.TextField(blank=True, default='')),
                ('showDate', models.DateTimeField()),
                ('vibrate', models.BooleanField(default=True)),
                ('song', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=1000)),
                ('versionName', models.CharField(blank=True, default='', max_length=1000)),
                ('versionCode', models.IntegerField(default=0)),
                ('lastUpdate', models.DateField(default=0)),
                ('executable', models.FileField(upload_to='softwares/collector')),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('longitude', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('altitude', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('verticalVelocity', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('horizontalVelocity', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('groundTrackHeading', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('timestamp', models.BigIntegerField(default=0)),
                ('simulated', models.BooleanField(default=False)),
                ('adsbInfo', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='observation', to='radarlivre_api.adsbinfo')),
                ('flight', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='observations', to='radarlivre_api.flight')),
            ],
        ),
        migrations.CreateModel(
            name='FlightInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('longitude', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('altitude', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('verticalVelocity', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('horizontalVelocity', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('groundTrackHeading', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('timestamp', models.BigIntegerField(default=0)),
                ('airline', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='radarlivre_api.airline')),
                ('flight', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='radarlivre_api.flight')),
            ],
        ),
        migrations.CreateModel(
            name='Collector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('latitude', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('longitude', models.DecimalField(decimal_places=10, default=0.0, max_digits=20)),
                ('timestamp', models.BigIntegerField(default=0)),
                ('timestampData', models.BigIntegerField(default=0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='collectors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
