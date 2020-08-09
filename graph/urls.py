from django.urls import path

from . import views

# app_name = 'features'

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('rooms/', views.rooms, name='rooms'),
]
