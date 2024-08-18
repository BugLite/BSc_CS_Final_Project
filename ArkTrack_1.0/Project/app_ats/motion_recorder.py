import os
import ffmpeg
import numpy as np
from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
from app_ats.models import RecordedVideo

def record_videos(frames_list, video_id, frame_shape, max_duration):
    records_dir = os.path.join(settings.MEDIA_ROOT, 'recordings')
    os.makedirs(records_dir, exist_ok=True)

    video_title = os.path.join(records_dir, f'recording_id({video_id}).mp4')

    # Saving video using ffmpeg
    out = ffmpeg.input('pipe:', framerate=20, format='rawvideo', pix_fmt='bgr24', s=f'{frame_shape[1]}x{frame_shape[0]}')
    out = ffmpeg.output(out, video_title, pix_fmt='yuv420p')
    out = ffmpeg.overwrite_output(out)
    out.run(input=np.concatenate(frames_list, axis=0).tobytes())
    
    # Save video metadata to the database
    captured_video = RecordedVideo.objects.create(
        title = os.path.basename(video_title),
        # file path is relative to 'MEDIA_ROOT' in Database
        file_path = os.path.relpath(video_title, start=settings.MEDIA_ROOT),
        duration = timedelta(seconds=max_duration),
        recorded_timestamp = now()
    )
    print(f"Video saved and metadata stored: {video_title}")

    return captured_video