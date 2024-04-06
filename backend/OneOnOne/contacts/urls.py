from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.contact_create, name='contact_create'),
    path('', views.contact_list, name='contact_list'),
    path('<int:pk>/', views.contact_detail, name='contact_detail'),
]