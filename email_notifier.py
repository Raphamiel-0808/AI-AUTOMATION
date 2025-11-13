"""
Email Notification Module
Sends daily task summaries via email
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional


class EmailNotifier:
    """Handles sending email notifications for task summaries"""

    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str,
                 sender_password: str, use_tls: bool = True):
        """
        Initialize the email notifier

        Args:
            smtp_server: SMTP server address (e.g., smtp.gmail.com)
            smtp_port: SMTP server port (e.g., 587 for TLS, 465 for SSL)
            sender_email: Email address to send from
            sender_password: Password or app-specific password
            use_tls: Whether to use TLS encryption
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.use_tls = use_tls

    def send_daily_summary(self, recipient_email: str, summary: str,
                          subject: Optional[str] = None) -> bool:
        """
        Send daily task summary email

        Args:
            recipient_email: Email address of the recipient (boss)
            summary: Task summary text to send
            subject: Email subject (auto-generated if not provided)

        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient_email

            # Auto-generate subject if not provided
            if not subject:
                today = datetime.now().strftime("%Y-%m-%d")
                subject = f"Daily Task Summary - {today}"

            message["Subject"] = subject

            # Create email body
            body = self._format_email_body(summary)
            message.attach(MIMEText(body, "plain"))

            # Send email
            if self.use_tls:
                # Use STARTTLS
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(message)
            else:
                # Use SSL
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(message)

            print(f"✓ Email sent successfully to {recipient_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            print("✗ Email authentication failed. Check your credentials.")
            return False
        except smtplib.SMTPException as e:
            print(f"✗ SMTP error occurred: {e}")
            return False
        except Exception as e:
            print(f"✗ Failed to send email: {e}")
            return False

    def _format_email_body(self, summary: str) -> str:
        """
        Format the email body with a professional header and footer

        Args:
            summary: Task summary text

        Returns:
            Formatted email body
        """
        body = "Hello,\n\n"
        body += "Please find below my daily task summary:\n\n"
        body += summary
        body += "\n\n"
        body += "Best regards,\n"
        body += "Automated Task Tracker\n"
        return body

    @staticmethod
    def from_env() -> Optional['EmailNotifier']:
        """
        Create EmailNotifier from environment variables

        Required environment variables:
            - SMTP_SERVER: SMTP server address
            - SMTP_PORT: SMTP port number
            - SENDER_EMAIL: Sender email address
            - SENDER_PASSWORD: Sender password or app password

        Returns:
            EmailNotifier instance or None if env vars not set
        """
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = os.getenv("SMTP_PORT")
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")

        if not all([smtp_server, smtp_port, sender_email, sender_password]):
            print("Warning: Email configuration not found in environment variables")
            return None

        use_tls = os.getenv("USE_TLS", "true").lower() == "true"

        return EmailNotifier(
            smtp_server=smtp_server,
            smtp_port=int(smtp_port),
            sender_email=sender_email,
            sender_password=sender_password,
            use_tls=use_tls
        )
