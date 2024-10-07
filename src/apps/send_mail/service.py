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

    async def send_activation_email(self, email: str, token: str) -> None:
        try:
            activation_link = f'http://127.0.0.1:8000//activate/{token}'
            subject = 'Активация вашего аккаунта'
            message = f'Для активации вашего аккаунта перейдите по ссылке: {activation_link}'

            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.email
            msg['To'] = email

            async with aiosmtplib.SMTP(
                hostname=self.host, port=self.port, use_tls=self.tls
            ) as server:
                await server.login(self.email, self.password)
                await server.sendmail(self.email, email, msg.as_string())

        except:
            raise SendMailActivationException


import asyncio

from environs import Env

if __name__ == '__main__':
    env = Env()
    env.read_env()

    jwt_conf = SMTPConfig.from_env(env)

    jwt_service = SendMailService(jwt_conf)

    # jwt_service.send_activation_email('onubee@gmail.com', '777')
    asyncio.run(jwt_service.send_activation_email('onubee@gmail.com', '888'))
