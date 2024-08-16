from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"), 
    path('webcam/', views.display_webcam, name='display_webcam'),
    path('webcam_feed/', views.webcam_feed, name='webcam_feed'),

    path('motion_identify/', views.identify_feed, name='identify_feed'),
    path('motion_identify_feed/', views.display_identify_detector, name='display_identify_feed'),

    path('motion_detector/', views.display_motion_detector, name='display_motion_detector'),
    path('motion_detector_feed/', views.motion_detector_view, name='motion_detector_feed'),

    path('dashboard/', views.dashboard, name='dashboard'),
]
