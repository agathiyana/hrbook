import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
import ssl
import threading

# Email settings (replace with actual details)
status = 'pending'
finalstatus =''

# Email settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL port
SENDER_EMAIL = "venky84.selva@gmail.com"
SENDER_PASSWORD = "qshb sgex koxw zucd"
RECIPIENT_EMAIL = "venky84.selva@gmail.com"
EMAIL_SUBJECT = "HRBook- Test mail"
EMAIL_BODY = "The status of the task has changed."

# Function to send email
def send_email():
    try:
      msg = MIMEMultipart()
      msg['From'] = SENDER_EMAIL
      msg['To'] = RECIPIENT_EMAIL
      msg['Subject'] = EMAIL_SUBJECT

        # Attach the email body
      msg.attach(MIMEText(EMAIL_BODY, 'plain'))

        # Set up the SSL context and the SMTP server connection
      context = ssl.create_default_context()
      with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())

      print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def email_scheduler(value):
    global status
  # Simulating a status change. This can be dynamic.
    print('js execution started 1'+ status+ value);
    # When the status changes, trigger the email sending
    if status != value:
        print(f"Status changed from {status} to {value}. Sending email...")
        send_email()
        status = value
    else:
        print("No status change.")

# Scheduler to check the status periodically (every 5 seconds in this example)
schedule.every(60).seconds.do(email_scheduler(finalstatus))

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
    
