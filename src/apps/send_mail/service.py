import smtplib
from email.mime.text import MIMEText

from src.apps.send_mail.exceptions import SendMailActivationException
from src.config import SMTPConfig


class SendMailService:
    def __init__(self, smtp_config: SMTPConfig):
        self.host = smtp_config.host
        self.port = smtp_config.port
        self.password = smtp_config.password
        self.email = smtp_config.email

    def send_activation_email(self, email: str, token: str) -> None:
        try:
            activation_link = f'http://127.0.0.1:8000//activate/{token}'
            subject = 'Активация вашего аккаунта'
            message = f'Для активации вашего аккаунта перейдите по ссылке: {activation_link}'

            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.email
            msg['To'] = email

            with smtplib.SMTP_SSL(self.host, self.port) as server:
                server.login(self.email, self.password)
                server.sendmail(self.email, email, msg.as_string())

        except:
            raise SendMailActivationException
