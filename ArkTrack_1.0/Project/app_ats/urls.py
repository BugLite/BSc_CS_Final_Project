from django.urls import path
from . import views

# Reference
# {% url 'name = ' %}
# href = /pathname

urlpatterns = [
    path('', views.home, name="home"), # -- homepage --
    path('tracker-main/', views.webcam_feed, name='main_feed'), #(main)tracker 
    path('tracker-sub/', views.motion_detector_view, name='sub_feed'), #(sub)tracker
    path('dashboard/', views.dashboard, name='dashboard'), # -- dashboard page --
    path('intelisense/', views.display_identify_detector, name='intelisense'), # -- intelisense page --
    path('tracker-intelisense/', views.identify_feed, name='intelisense_feed'), #(intel)tracker
]
