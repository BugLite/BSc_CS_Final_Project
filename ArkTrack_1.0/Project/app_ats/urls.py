from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"), 
    path('webcam/', views.display_webcam, name='display_webcam'),
    path('webcam_feed/', views.webcam_feed, name='webcam_feed'),
]