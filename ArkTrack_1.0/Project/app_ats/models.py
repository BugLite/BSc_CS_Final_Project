from django.db import models

# RecordedVideo model stores videos
class RecordedVideo(models.Model):
    title = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    duration = models.DurationField()  # Duration in seconds
    recorded_timestamp = models.DateTimeField()

    def __str__(self):
        return self.title
