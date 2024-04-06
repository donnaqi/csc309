from rest_framework import serializers
from django.contrib.auth.models import User
from .models.event import Event 

class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # Read-only field for the owner's username
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Event
        fields = ('id', 'owner', 'name', 'description', 'date', 'start_time', 'duration', 'participants')

    def validate_name(self, value):
        """
        Check if an event with the same title already exists.
        """
        if Event.objects.filter(name=value).exists():
            raise serializers.ValidationError("An event with this name already exists.")
        return value
    
    def validate_start_time(self, value):
        """
        Check if the start time is in 30-minute increments.
        """
        if value.minute % 30 != 0:
            raise serializers.ValidationError("Start time must be in 30-minute increments.")
        return value
