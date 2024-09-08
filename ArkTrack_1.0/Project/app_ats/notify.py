from django.conf import settings
from django.core.mail import send_mail

def send_email_alert(recorded_video):
    """
    The `send_email_alert` function is used to send out an email alert to the owner of the surveillance system.
    The email includes information about the captured footage including the title, timestamp and duration.
    The email also includes a subject and email
    """
    # email heading
    subject = 'ArkTrack System Alert' 
    # plain message for non-HTML supportive email clients
    plain_message = "Motion detected. Please check your system for more details."
    # custom style message to alert user with associated recording metadata
    message = f"""
    <html>
        <body>
            <h3 style="color: red;">ArkTrack System: Motion Detected</h3>
            <p style="font-size: 15px;"> Hello User,</p>
            <p style="font-size: 15px;"> Significant motion has been detected by your ArkTrack System. Kindly review the cause of the recording:</p>
            <ul style="font-size: 15px;">
                <li><strong>Recording Title:</strong> {recorded_video.title}</li>
                <li><strong>Timestamp:</strong> {recorded_video.recorded_timestamp}</li>
                <li><strong>Duration:</strong> {recorded_video.duration} seconds</li>
            </ul>
            <p style="font-size: 15px;">In case of Emergency, use the <b style="color: red;">Report</b> feature of the system to alert authorities immediately.</p>
            <p style="font-size: 15px; color: darkblue;">ArkTrack System</p>
        </body>
    </html>
    """
    # email settings.
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['hyder.devop@gmail.com']
    fail_silently = False

    # sending the email alert with associated recording details
    send_mail(subject, plain_message, from_email, recipient_list, fail_silently, html_message=message)
    print("Email sent successfully!")
