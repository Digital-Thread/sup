from src.apps.send_mail.tasks import (
    password_reset_email_task,
    send_activation_email_task,
    send_invite_email_task,
    send_login_and_activate_email_task,
)
from src.config import SMTPConfig


class SendMailService:

    @staticmethod
    async def send_activation_email(smtp_config: SMTPConfig, email: str, token: str) -> None:
        await send_activation_email_task.kiq(smtp_config=smtp_config, email=email, token=token)

    @staticmethod
    async def send_login_and_activate_email(
        smtp_config: SMTPConfig, email: str, password: str, token: str
    ) -> None:
        await send_login_and_activate_email_task(
            smtp_config=smtp_config, email=email, password=password, token=token
        )

    @staticmethod
    async def send_login_email(
        smtp_config: SMTPConfig, email: str, password: str, token: str
    ) -> None:
        await send_login_and_activate_email_task(
            smtp_config=smtp_config, email=email, password=password, token=token
        )

    @staticmethod
    async def send_invite_email(smtp_config: SMTPConfig, email: str, token: str) -> None:
        await send_invite_email_task(smtp_config=smtp_config, email=email, token=token)

    @staticmethod
    async def password_reset_email(smtp_config: SMTPConfig, email: str, password: str) -> None:
        await password_reset_email_task(smtp_config=smtp_config, email=email, password=password)
