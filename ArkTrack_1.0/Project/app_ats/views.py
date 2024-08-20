# django utilities import
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.conf import settings

# tracker functions import
from .tracker_A import gen_frames
from .tracker_B import generate_motion_frames

# database model import
from .models import RecordedVideo

# streaming functions to browers or client
def webcam_feed(request):
    intellisense_active = request.session.get('intellisense_active', False)
    return StreamingHttpResponse(gen_frames(intellisense_active=intellisense_active), content_type='multipart/x-mixed-replace; boundary=frame')

def motion_detector_view(request):
    return StreamingHttpResponse(generate_motion_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


# rendering webpage html url
def home(request):
    if request.method == "POST":
        request.session['intellisense_active'] = 'intellisense_active' in request.POST
    intellisense_active = request.session.get('intellisense_active', False)
    return render(request, 'home.html', {'intellisense_active': intellisense_active})

def display_webcam(request):
    return render(request, 'webcam.html')

def display_motion_detector(request):
    return render(request, 'motion_detector.html')

# dashboard media request function
def dashboard(request):
    videos = RecordedVideo.objects.all().order_by('-recorded_timestamp')
    return render(request, 'dashboard.html', {
        'videos': videos,
        'MEDIA_URL': settings.MEDIA_URL,
    })