from django.http import JsonResponse
from rest_framework.views import APIView
from calendars.services import suggest_schedules
from calendars.models.event import Event
from rest_framework.permissions import IsAuthenticated
from datetime import time
from django.core.mail import send_mail
from django.conf import settings


class CalendarEventSuggestedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        user = request.user
        try:
            # Fetch the event by id
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found.'}, status=404)

        # Check if the logged-in user is the owner of the event
        if event.owner != user:
            # If not the owner, return a forbidden response
            return JsonResponse({'error': 'You do not have permission to view the suggested schedules for this event.'}, status=403)

        # Proceed if the user is the event owner
        suggestions = suggest_schedules(event.id)
        if not suggestions:
            return JsonResponse({'error': 'No available schedules because some participants are not available.'}, status=400)

        return JsonResponse({'suggestions': suggestions})


class FinalizeScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        user = request.user
        try:
            # Fetch the event by id
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found.'}, status=404)

        # Check if the logged-in user is the owner of the event
        if event.owner != user:
            # If not the owner, return a forbidden response
            return JsonResponse({'error': 'You do not have permission to finalize the schedule for this event.'}, status=403)

        # Proceed if the user is the event owner
        selected_schedule = request.data

        # if missing fields:
        if not all([selected_schedule.get('start_time'), selected_schedule.get('date')]):
            return JsonResponse({'error': 'missing fields'}, status=400)

        if not selected_schedule:
            return JsonResponse({'error': 'No selected schedule provided.'}, status=400)

        start_time = selected_schedule['start_time']
        start_time = float_to_time(start_time)
        event.start_time = start_time
        event.save()
        meeting_time = event.start_time.strftime('%H:%M')
        meeting_date = event.date.strftime('%Y-%m-%d')

        finalized_schedule = {
            'date': meeting_date,
            'start_time': meeting_time
        }

        participants = event.participants.all()  

        subject = f'Meeting Scheduled for {meeting_date}'
        message = f'Hello, a meeting has been scheduled on {meeting_date} at {meeting_time}. Please mark your calendar.'

        # Send an email to each participant
        for participant in participants:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # From email
                # To email
                [participant.email],
                fail_silently=False,
            )

        return JsonResponse({'message': 'Schedule finalized successfully.', 'finalized_schedule': finalized_schedule})


def float_to_time(time_float):
    # Split the float into hours and minutes
    hours = int(time_float)
    minutes = int((time_float - hours) * 60)

    # Create a datetime.time object
    return time(hour=hours, minute=minutes)
