from django.shortcuts import render
from django.http import StreamingHttpResponse
from .detector_main import gen_frames

# from .detector_main_2 import gen_frames

from .detector_sub import generate_motion_frames
from .detector_classify import gen_identify_frames

from .models import RecordedVideo
from django.conf import settings

# dashboard media request function
def dashboard(request):
    videos = RecordedVideo.objects.all().order_by('-recorded_timestamp')
    return render(request, 'dashboard.html', {
        'videos': videos,
        'MEDIA_URL': settings.MEDIA_URL,
    })

# Create your views here.
def home(request):
    return render(request, 'home.html')

# Requried: It's responsible for generating and sending the actual video content to the client. 
# Without this function, there would be no mechanism to capture and stream the webcam feed to the browser.
def webcam_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def identify_feed(request):
    return StreamingHttpResponse(gen_identify_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def motion_detector_view(request):
    return StreamingHttpResponse(generate_motion_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

# Required: It provides a user interface (UI) for viewing the stream. This function essentially serves the web page that the user interacts with. 
# Without this function, users wouldn't have a webpage to visit where they could see the motion detection stream
def display_webcam(request):
    return render(request, 'webcam.html')

def display_motion_detector(request):
    return render(request, 'motion_detector.html')

def display_identify_detector(request):
    return render(request, 'identify.html')