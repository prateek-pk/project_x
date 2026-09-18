from django.contrib import admin
from .models import Salon, Service, Appointment

# Register your models here.
admin.site.register(Salon)
admin.site.register(Service)
admin.site.register(Appointment)