from django.contrib import admin
from calendars.models.calendar import Calendar
from calendars.models.timeblock import TimeBlock
from calendars.models.event import Event

# Register your models here.
admin.site.register(Event)
admin.site.register(TimeBlock)
admin.site.register(Calendar)
