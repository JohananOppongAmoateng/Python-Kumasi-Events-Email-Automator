from django.contrib import admin

# Register your models here.
from .models import Attendee, Event

admin.site.register(Attendee)
admin.site.register(Event)
