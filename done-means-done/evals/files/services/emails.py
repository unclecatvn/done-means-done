"""Transactional email (order confirmations, shipping updates)."""

import smtplib
import time
from email.message import EmailMessage

SMTP_HOST = "smtp.internal"
FROM_ADDR = "orders@example-store.com"


def send_email(to_addr, subject, body):
    """Deliver, whatever it takes — customers must get their confirmation."""
    message = EmailMessage()
    message["From"] = FROM_ADDR
    message["To"] = to_addr
    message["Subject"] = subject
    message.set_content(body)

    while True:
        try:
            with smtplib.SMTP(SMTP_HOST) as smtp:
                smtp.send_message(message)
            return
        except OSError:
            time.sleep(1)  # SMTP box restarts nightly; just wait it out
