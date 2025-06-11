from django.contrib import admin
from radarlivre_api.models import (
    About,
    Notify,
    Software,
    Collector,
    Observation,
    ADSBInfo,
)


# Register your models here.


class CollectorAdmin(admin.ModelAdmin):
    list_display = ("key", "latitude", "longitude")


admin.site.register(About)
admin.site.register(Notify)
admin.site.register(Software)
admin.site.register(Collector, CollectorAdmin)
admin.site.register(Observation)
admin.site.register(ADSBInfo)
