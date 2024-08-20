from django.conf import settings
from django.core.mail import send_mail

# Send an email notification
def send_alert_mail(recorded_video):
    subject = 'ArkTrack System: Disturbance Detected'
    message = f"Motion Detected\nRecording Title: {recorded_video.title}\nTimestamp: {recorded_video.recorded_timestamp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['hyder.devop@gmail.com']
    fail_silently = False

    send_mail(subject, message, from_email, recipient_list, fail_silently)
    print("Email sent successfully!")