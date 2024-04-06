from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models.event import Event
from ..event_serializer import EventSerializer
from django.core.mail import send_mail
from django.conf import settings

'''
Validations:
name
start_time
'''

class EventCreationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    '''def post(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)'''

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class EventUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


'''
class EventUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def post(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        
        return self.request.user.owned_events.all()'''


class EventReminderView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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

        meeting_time = event.start_time.strftime('%H:%M')
        meeting_date = event.date.strftime('%Y-%m-%d')
        participants = event.participants.all()  

        subject = f'Reminder for Meeting Scheduled on {meeting_date}'
        message = f'Hello, a kind reminder that a meeting has been scheduled on {meeting_date} at {meeting_time}.'

        finalized_schedule = {
            'date': meeting_date,
            'start_time': meeting_time
        }

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

        return JsonResponse({'message': 'Reminder sent successfully.', 'finalized_schedule': finalized_schedule})



'''class EventAllListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer'''

class EventAllListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, format=None):
        objects = Event.objects.filter(owner=request.user.id)
        result = []
        for event in objects:
            result.append(dict(EventSerializer(event).data))
        
        return Response(
            data=result
        )

    def get_queryset(self):
        return self.request.user.owned_events.all()
