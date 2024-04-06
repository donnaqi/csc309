from django.contrib.auth.models import User
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        email = self.validated_data['email'].lower()

        if not email:
            raise serializers.ValidationError(
                {'error': 'This field may not be blank.'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'error': 'Email already exists.'})

        username = self.validated_data['username']

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        # if password length less than 8
        if len(password) < 8:
            raise serializers.ValidationError(
                {'error': 'Password must be at least 8 characters long.'})
        if password != password2:
            raise serializers.ValidationError(
                {'error': 'Passwords must match.'})

        account = User(email=email, username=username)
        account.set_password(password)
        account.save()
        return account
