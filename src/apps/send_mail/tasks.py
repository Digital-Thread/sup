from email.mime.text import MIMEText

import aiosmtplib

from src.apps.send_mail.exceptions import SendMailActivationException
from src.broker import broker
from src.config import SMTPConfig


async def connect_smtp(smtp_config: SMTPConfig, email: str, message: str, subject: str) -> None:
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = smtp_config.email
    msg['To'] = email

    async with aiosmtplib.SMTP(
        hostname=smtp_config.host, port=smtp_config.port, use_tls=smtp_config.tls
    ) as server:
        await server.login(smtp_config.email, smtp_config.password)
        await server.sendmail(smtp_config.email, email, msg.as_string())


@broker.task(task_name='send_activation_email')
async def send_activation_email_task(smtp_config: SMTPConfig, email: str, token: str) -> None:
    try:
        activation_link = f'http://0.0.0.0:8080/api/v1/user/activate/{token}'
        subject = 'Активация вашего аккаунта'
        message = f'Здравствуйте, {email}.\n \nЧтобы активировать аккаунт перейдите по ссылке: {activation_link}'

        await connect_smtp(smtp_config, email, message, subject)

    except:
        raise SendMailActivationException


@broker.task(task_name='send_login_and_activate_email')
async def send_login_and_activate_email_task(
    smtp_config: SMTPConfig, email: str, password: str, token: str
) -> None:
    try:
        activation_link = f'http://0.0.0.0:8080/api/v1/user/activate/{token}'
        subject = 'Активация вашего аккаунта'
        message = (
            f'Здравствуйте, {email}.\n \nДля вас был создан аккаунт на сайте http://0.0.0.0:8080 '
            f'\n \nEmail: {email}\nПароль: {password}\n \n'
            f'Чтобы активировать аккаунт перейдите по ссылке: {activation_link}'
        )

        await connect_smtp(smtp_config, email, message, subject)
    except:
        raise SendMailActivationException


@broker.task(task_name='send_login_email')
async def send_login_email_task(smtp_config: SMTPConfig, email: str, password: str) -> None:
    try:
        activation_link = f'http://0.0.0.0:8080/api/v1/user/login'
        subject = 'Вход в аккаунт'
        message = (
            f'Здравствуйте, {email}.\n \nДля вас был создан аккаунт на сайте http://0.0.0.0:8080 \n '
            f'\nEmail: {email}\nПароль: {password}\n '
            f'Для входа вашего аккаунта перейдите по ссылке: {activation_link}'
        )

        await connect_smtp(smtp_config, email, message, subject)

    except:
        raise SendMailActivationException


@broker.task(task_name='send_invite_email')
async def send_invite_email_task(smtp_config: SMTPConfig, email: str, token: str) -> None:
    try:
        invite_link = f'http://0.0.0.0:8080/api/v1/user/registration/{token}'
        subject = 'Приглашение на регистрацию'
        message = f'Здравствуйте, {email}.\n \nДля регистрации вашего аккаунта перейдите по ссылке: {invite_link}'

        await connect_smtp(smtp_config, email, message, subject)

    except:
        raise SendMailActivationException


@broker.task(task_name='password_reset_email')
async def password_reset_email_task(smtp_config: SMTPConfig, email: str, password: str) -> None:
    try:
        activation_link = f'http://0.0.0.0:8080/api/v1/user/login'
        subject = 'Вход в аккаунт'
        message = (
            f'Здравствуйте, {email}.\n \nВаш пароль на сайте http://0.0.0.0:8080 был изменен.\n '
            f'\nВаш новый пароль: {password}\n '
            f'Для входа вашего аккаунта перейдите по ссылке: {activation_link}\n '
            f'\nНе забудьте его изменить в настройках аккаунта. '
        )

        await connect_smtp(smtp_config, email, message, subject)

    except:
        raise SendMailActivationException
