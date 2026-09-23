import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv


load_dotenv()
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")

def send_email(to, subject, body):
    msg = EmailMessage()
    msg["From"] = email_address
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_address, email_password)
        server.send_message(msg)


if __name__ == "__main__":
    send_email(email_address, "Test from book tracker", "If you see this, email works!")