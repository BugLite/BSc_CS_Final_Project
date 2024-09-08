from django.urls import path
from . import views

# defining the url paths 

urlpatterns = [
    path('', views.home, name="home"), # -- homepage --

    path('camera-main/', views.camera_feed, name='camera_feed'), # camera feed 
    
    path('tracker-main/', views.webcam_feed, name='main_feed'), # (main) trackerA 

    path('tracker-sub/', views.motion_detector_view, name='sub_feed'), #(sub) trackerB

    path('dashboard/', views.dashboard, name='dashboard'), # -- dashboard page --

    path('delete_video/<str:video_title>/', views.delete_video, name='delete_video'), # delete function

    path('report/', views.report, name='report'), # -- report page --

    path('help/', views.support, name='help'), # -- help page --
]
