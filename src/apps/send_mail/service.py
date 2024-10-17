from email.mime.text import MIMEText

import aiosmtplib

from src.apps.send_mail.exceptions import SendMailActivationException
from src.config import SMTPConfig


class SendMailService:
    def __init__(self, smtp_config: SMTPConfig):
        self.host = smtp_config.host
        self.port = smtp_config.port
        self.password = smtp_config.password
        self.email = smtp_config.email
        self.tls = smtp_config.TLS

    async def connect_smtp(self, message: str, subject: str, email_to: str) -> None:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = email_to
        async with aiosmtplib.SMTP(hostname=self.host, port=self.port, use_tls=self.tls) as server:
            await server.login(self.email, self.password)
            await server.sendmail(self.email, email_to, msg.as_string())

    async def send_activation_email(self, email: str, token: str) -> None:
        try:
            activation_link = f'http://127.0.0.1:8000//activate/{token}'
            subject = 'Активация вашего аккаунта'
            message = f'Для активации вашего аккаунта перейдите по ссылке: {activation_link}'

            await self.connect_smtp(message, subject, email)

        except:
            raise SendMailActivationException

    async def send_login_and_activate_email(self, email: str, password: str, token: str) -> None:
        try:
            activation_link = f'http://127.0.0.1:8000//activate/{token}'
            subject = 'Активация вашего аккаунта'
            message = f'Email: {email}\n Пароль: {password} \nДля входа вашего аккаунта перейдите по ссылке: {activation_link}'

            await self.connect_smtp(message, subject, email)
        except:
            raise SendMailActivationException

    async def send_login_email(self, email: str, password: str) -> None:
        try:
            activation_link = f'http://127.0.0.1:8000/login'
            subject = 'Вход в аккаунт'
            message = f'Email: {email}\nПароль: {password}\nДля входа вашего аккаунта перейдите по ссылке: {activation_link}'

            await self.connect_smtp(message, subject, email)

        except:
            raise SendMailActivationException

    async def send_invite_email(self, email: str, token: str) -> None:
        try:
            invite_link = f'http://127.0.0.1:8000//register/{token}'
            subject = 'Приглашение на регистрацию'
            message = f'Для регистрации вашего аккаунта перейдите по ссылке: {invite_link}'

            await self.connect_smtp(message, subject, email)

        except:
            raise SendMailActivationException
