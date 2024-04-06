from django.urls import path
from .views.register_view import UserRegistrationView
from .views.login_view import LoginView
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = 'accounts'
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/login/', LoginView.as_view(), name='custom_login'),
]
