from django.db import models

class RecordedVideo(models.Model):
    """
    The following fields are used to define a Database model to store the metadata for the recorded videos.
    This includes the recording title, file path, duration and date/time information.
    """
    title = models.CharField(max_length=255) # recording title (length 255)
    file_path = models.CharField(max_length=500) # recording file path size (max 500)
    duration = models.DurationField()  # recording length in seconds
    recorded_timestamp = models.DateTimeField()

    def __str__(self):
        return self.title
