import subprocess
from datetime import datetime
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def log_timeout():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ping_log.txt")
    with open(log_file, "a") as f:
        f.write(f"Request timeout at {timestamp}\n")
    return log_file

def send_email(log_file, failed_timestamp,cc_emails=["cc@example.com","cc@example.com"]):
    # Email configuration
    sender_email = "abc@example.com"
    receiver_email = "abc@example.com"
    cc_emails = cc_emails if cc_emails else []
    password = "Add App Password from Google Apps"
    
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Cc'] = ", ".join(cc_emails)
    msg['Subject'] = f"Alert! Server is down at {failed_timestamp}"

    # Email body
    body = """Hello Devs,

The  server has failed to respond and users might face issues. Please check and fix to resolve this alert.

Thanks
Server Bot

"""
    msg.attach(MIMEText(body, 'plain'))

    # Attach log file
    with open(log_file, "r") as f:
        attachment = MIMEText(f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(log_file))
    msg.attach(attachment)

    # Connect to SMTP server and send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)

def ping_ip(ip_address):
    try:
        if os.name == 'nt':  # Check if running on Windows
            output = subprocess.check_output(['ping', ip_address, '-n', '1'], timeout=5, universal_newlines=True)
        else:
            output = subprocess.check_output(['ping', ip_address, '-c', '1'], timeout=5, universal_newlines=True)
        
        if "1 packets transmitted, 0 received" in output or "Request timeout" in output:
            failed_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file = log_timeout()
            send_email(log_file, failed_timestamp)
        print(output)
    except subprocess.TimeoutExpired:
        failed_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = log_timeout()
        send_email(log_file, failed_timestamp)
        print("Request timed out")

if __name__ == "__main__":
    ip_address = "10.10.10.10"
    ping_count = 0
    max_pings = 15
    while ping_count < max_pings:
        ping_ip(ip_address)
        ping_count += 1
        time.sleep(300)  # 5 minutes interval (300 seconds)
