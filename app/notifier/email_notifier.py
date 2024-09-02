import smtplib
from email.mime.text import MIMEText
from .notifier import NotifierBase

class EmailNotifier(NotifierBase):
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str, recipient: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.recipient = recipient

    def notify(self, message: str):
        msg = MIMEText(message)
        msg['Subject'] = 'Scraping Tool Notification'
        msg['From'] = self.username
        msg['To'] = self.recipient

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, self.recipient, msg.as_string())
