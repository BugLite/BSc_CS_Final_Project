import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import RecordedVideo

def delete_by_title(video_title):
    """
    Function designed to 'find and delete' a recording based on its title passed as an argument.
    The function raises an Http404 (not found) error in case video title is not found in database.
    """

    # retrieves the recording based on the passed title
    video = get_object_or_404(RecordedVideo, title=video_title)
    
    # finds out the complete file path of the recording
    video_path = os.path.join(settings.MEDIA_ROOT, video.file_path)

    # checks if recording file exists in the file system and subsequently deletes if found
    if os.path.exists(video_path):
        os.remove(video_path)
        print(f"Deleted video file: {video_path}") # confirmation message
    else:
        print(f"Recording does not exist - 404 : {video_path}")

    # deletes the recording file from database
    video.delete()
