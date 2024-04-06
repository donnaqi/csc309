from django.db import models
from calendars.models.calendar import Calendar
from calendars.models.event import Event

class TimeBlock(models.Model):
    calendar = models.ForeignKey(
        Calendar, on_delete=models.CASCADE, null=False, blank=False
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=True
    )
    time = models.FloatField(null=False, blank=False)
    yr = models.PositiveIntegerField(default=None, null=True, blank=True)
    wk = models.PositiveIntegerField(default=None, null=True, blank=True)
    day = models.PositiveIntegerField(default=None, null=True, blank=True)
    preference = models.IntegerField(
        choices=((1, 'First Choice'), (2, 'Second Choice')), 
        null=True, blank=False
    )

    def __str__(self):
        return f"{self.yr}-{self.wk}-{self.day} {self.time}"