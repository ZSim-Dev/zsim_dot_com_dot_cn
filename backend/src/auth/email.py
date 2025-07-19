import smtplib
import tomllib
from email.mime.text import MIMEText

from pydantic import BaseModel


class EmailConfig(BaseModel):
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_from: str
    send_real_email: bool


# Load config
with open("backend/config.toml", "rb") as f:
    config = EmailConfig(**tomllib.load(f)["aliyun"]["email"])


def send_email(to_email: str, subject: str, content: str):
    """
    Sends an email.
    If send_real_email in the config is set to True, it sends a real email.
    Otherwise, it prints the email content to the console.
    """
    if config.send_real_email:
        msg = MIMEText(content, "html", "utf-8")
        msg["Subject"] = subject
        msg["From"] = config.smtp_from
        msg["To"] = to_email

        with smtplib.SMTP_SSL(config.smtp_host, config.smtp_port) as server:
            server.login(config.smtp_username, config.smtp_password)
            server.send_message(msg)
    else:
        print("--- Mock Email Sent ---")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Content: {content}")
        print("----------------------")


if __name__ == "__main__":
    # Example usage:
    send_email(
        "test@example.com",
        "Test Subject",
        "<h1>This is a test</h1><p>Your code is 123456</p>",
    )
