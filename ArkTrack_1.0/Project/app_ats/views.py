from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse
from .detector_main import gen_frames

# Create your views here.

def home(request):
    return HttpResponse("Hello Unaiza!")

def webcam_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def display_webcam(request):
    return render(request, 'webcam.html')