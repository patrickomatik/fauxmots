import smtplib
from email.message import EmailMessage

# Create a simple test email
msg = EmailMessage()
msg.set_content("This is a quick test email.")
msg['Subject'] = 'Quick Test'
msg['From'] = 'test@example.com'
msg['To'] = 'recipient@example.com'

try:
    # Connect to our SMTP server and send the message
    with smtplib.SMTP('127.0.0.1', 2025) as server:
        server.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
