from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import UserRegistrationSerializer


class UserRegistrationView(APIView):
    def post(self, request):
        # missing username
        if not (request.data.get('username')):
            return Response({"error": "Missing username."}, status=status.HTTP_400_BAD_REQUEST)
        # missing email
        if not (request.data.get('email')):
            return Response({"error": "Missing email."}, status=status.HTTP_400_BAD_REQUEST)
        # missing password
        if not (request.data.get('password')):
            return Response({"error": "Missing password."}, status=status.HTTP_400_BAD_REQUEST)
        # missing password2
        if not (request.data.get('password2')):
            return Response({"error": "Missing confirm password."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
