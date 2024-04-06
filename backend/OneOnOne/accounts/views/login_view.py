import requests
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from calendars.models.calendar import Calendar


class LoginView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        # if missing username
        if not username:
            return Response({"error": "Missing username."}, status=status.HTTP_400_BAD_REQUEST)
        # if missing password
        if not password:
            return Response({"error": "Missing password."}, status=status.HTTP_400_BAD_REQUEST)
        # if not all([username, password]):
        #     return Response({"error": "missing fields"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)

            # Check if the user has a calendar, if not create one
            if not Calendar.objects.filter(owner=user.id).exists():
                access_token = 'Bearer ' + str(AccessToken.for_user(user))
                requests.post(
                    url='http://127.0.0.1:8000/calendar/create/',
                    headers={
                        'Authorization': access_token
                    }
                )

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
            })
        else:
            return Response({"error": "Your username or password is incorrect. Please try again."}, status=status.HTTP_401_UNAUTHORIZED)
