from django.contrib import admin
from .models import RecordedVideo

class ArkTrackAdmin(admin.ModelAdmin):
    """
    A customised admin interface for management of the ArkTrack System Recordings.
    """
    list_display = ('title', 'file_path', 'duration', 'recorded_timestamp')
    search_fields = ('title', 'file_path')
    ordering = ('-recorded_timestamp',)

# registering my RecordedVideo model with the admin site
admin.site.register(RecordedVideo, ArkTrackAdmin)
