import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional
import datetime

from fastapi import BackgroundTasks
from fastapi.templating import Jinja2Templates

from app.utils.config import settings

logger = logging.getLogger(__name__)

templates_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


def render_template(template_name: str, **kwargs) -> str:
    """Render a template with the given context."""
    template = templates.get_template(template_name)
    return template.render(**kwargs)


class EmailService:
    async def send_email(
        self,
        email_to: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        if not all(
            [
                settings.SMTP_HOST,
                settings.SMTP_PORT,
                settings.SMTP_USER,
                settings.SMTP_PASSWORD,
                settings.EMAILS_FROM_EMAIL,
            ]
        ):
            logger.error("Email settings not configured")
            return False

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        message["To"] = email_to

        if text_content is None:
            text_content = html_content.replace("<br>", "\n").replace("</p>", "\n</p>")
            import re

            text_content = re.sub(r"<[^>]*>", "", text_content)

        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)

        try:
            if not settings.SMTP_HOST or not settings.SMTP_PORT:
                raise ValueError("SMTP_HOST and SMTP_PORT must be set")

            server = smtplib.SMTP(str(settings.SMTP_HOST), int(settings.SMTP_PORT))
            if settings.SMTP_TLS:
                server.starttls()

            if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
                raise ValueError("SMTP_USER and SMTP_PASSWORD must be set")
            server.login(str(settings.SMTP_USER), str(settings.SMTP_PASSWORD))

            if not settings.EMAILS_FROM_EMAIL:
                raise ValueError("EMAILS_FROM_EMAIL must be set")
            server.sendmail(str(settings.EMAILS_FROM_EMAIL), email_to, message.as_string())

            server.quit()

            logger.info(f"Email sent successfully to {email_to}")
            return True

        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False


email_service = EmailService()

async def send_password_reset_email(
    background_tasks: BackgroundTasks, user_email: str, first_name: str, reset_link: str
) -> None:
    """Send password reset email."""
    subject = "Reset Your Password"
    current_year = datetime.datetime.now().year

    html_content = render_template(
        "emails/password_reset.html", first_name=first_name, reset_link=reset_link, current_year=current_year
    )

    background_tasks.add_task(
        email_service.send_email,
        email_to=user_email,
        subject=subject,
        html_content=html_content,
    )