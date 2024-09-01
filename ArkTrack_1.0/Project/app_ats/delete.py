# app_ats/delete.py
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import RecordedVideo

def delete_video_by_title(video_title):
    # Get the video object from the database by title
    video = get_object_or_404(RecordedVideo, title=video_title)
    
    # Construct the full file path
    video_path = os.path.join(settings.MEDIA_ROOT, video.file_path)

    # Delete the video file from the filesystem
    if os.path.exists(video_path):
        os.remove(video_path)
        print(f"Deleted video file: {video_path}")

    # Delete the video object from the database
    video.delete()
