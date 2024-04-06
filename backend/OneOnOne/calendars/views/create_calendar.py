from calendars.models.calendar import Calendar
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class CalendarCreationView(APIView):
    # Ensure the user is authenticated
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def post(self, request, format=None):
        # Check if the user already has a calendar
        if Calendar.objects.filter(owner=request.user.id).exists():
            return Response(
                {"error":"user already has a calendar"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            c = Calendar()
            c.owner = request.user
            c.last_modified = None
            c.save()
            return Response(status=status.HTTP_201_CREATED)