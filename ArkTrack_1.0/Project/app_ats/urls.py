from django.urls import path
from . import views

# Reference
# {% url 'name = ' %}
# href = /pathname

urlpatterns = [
    path('', views.home, name="home"), # -- homepage --

    path('camera-main/', views.camera_feed, name='camera_feed'), #camera feed 
    
    path('tracker-main/', views.webcam_feed, name='main_feed'), #(main)tracker 

    path('tracker-sub/', views.motion_detector_view, name='sub_feed'), #(sub)tracker

    path('dashboard/', views.dashboard, name='dashboard'), # -- dashboard page --
]
