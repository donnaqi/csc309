from rest_framework import serializers
from calendars.models.timeblock import TimeBlock

class TimeBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeBlock
        fields = ['id', 'event', 'time', 'yr', 'wk', 'day', 'preference']