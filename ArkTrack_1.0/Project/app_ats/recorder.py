# importing ffmpeg, numpy and other helper libraries
import os
import ffmpeg
import numpy as np
from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
from app_ats.models import RecordedVideo

def record_videos(frames_list, video_id, frame_shape, max_duration, frame_rate):
    """
    The `record_videos` function provides critical functionality for recording and encoding a captured video using FFMPEG library.
    The function therefore, helps to efficiently save the recording in the correct format and ideal compression. 
    The function arguments include:
        frames_list: to store the list of frames/images. 
        frame_shape: to store the shapes of each frames - height, width and channels. 
        video_id: to uniquely identify each recording - added to filename.
        max_duration: to keep track of the maximum duration of each recording.
        frame_rate: to define a specific frame-rate i.e. frames per second for the recordings.
    """
    # setting up the path to the recording directory
    records_dir = os.path.join(settings.MEDIA_ROOT, 'recordings')
    # creating a directory incase does not exist or is not found
    os.makedirs(records_dir, exist_ok=True)

    # creating a full file path for the recorded video with the addition of video_id
    video_title = os.path.join(records_dir, f'recording_{video_id}.mp4')

    # preparing the frames for ffmpeg encoding and compression
    frames_array = np.array(frames_list)
    # extracting height, width and channel information from frame_shape
    height, width, _ = frame_shape
    # total number of frames to encode
    sum_frames = frames_array.shape[0]

    # Input: pipe the raw frames in BGR format with a set frame rate
    set_input = ffmpeg.input('pipe:', framerate=20, format='rawvideo', pix_fmt='bgr24', s=f'{width}x{height}')
    # Output: encoding the recording to mp4 format with a yuv420p pixel format and the desired frame rate
    output = ffmpeg.output(set_input, video_title, pix_fmt='yuv420p', r=frame_rate)
    output = ffmpeg.overwrite_output(output)

    # running FFMPEG
    output.run(input=frames_array.tobytes())
    
    # rounding off the duration of recording to nearest whole second
    duration_in_seconds = round(min(max_duration, sum_frames / frame_rate))
    video_duration = timedelta(seconds=duration_in_seconds)
    
    # saving the recorded video's metadata to the database model - RecordedVideo()
    captured_video = RecordedVideo.objects.create(
        title = os.path.basename(video_title),
        # file path is relative to 'MEDIA_ROOT' in Database
        file_path = os.path.relpath(video_title, start=settings.MEDIA_ROOT),
        duration = video_duration,
        recorded_timestamp = now()
    )

    # verifying that video was successfully saved
    print(f"Video saved and metadata stored: {video_title}")

    return captured_video