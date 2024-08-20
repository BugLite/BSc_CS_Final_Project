import os
import ffmpeg
import numpy as np
from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
from app_ats.models import RecordedVideo

def record_videos(frames_list, video_id, frame_shape, max_duration, frame_rate):
    records_dir = os.path.join(settings.MEDIA_ROOT, 'recordings')
    os.makedirs(records_dir, exist_ok=True)

    video_title = os.path.join(records_dir, f'recording_id({video_id}).mp4')

    # Prepare the frames for ffmpeg
    frames_array = np.array(frames_list)
    height, width, _ = frame_shape
    num_frames = frames_array.shape[0]

    # Saving video using ffmpeg
    out = ffmpeg.input('pipe:', framerate=20, format='rawvideo', pix_fmt='bgr24', s=f'{width}x{height}')
    out = ffmpeg.output(out, video_title, pix_fmt='yuv420p', r=frame_rate)
    out = ffmpeg.overwrite_output(out)
    out.run(input=frames_array.tobytes())
    
    # Save video metadata to the database
    captured_video = RecordedVideo.objects.create(
        title = os.path.basename(video_title),
        # file path is relative to 'MEDIA_ROOT' in Database
        file_path = os.path.relpath(video_title, start=settings.MEDIA_ROOT),
        duration = timedelta(seconds=min(max_duration, num_frames / frame_rate)),
        recorded_timestamp = now()
    )
    print(f"Video saved and metadata stored: {video_title}")

    return captured_video