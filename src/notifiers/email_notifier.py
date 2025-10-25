"""
Email notification module
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from datetime import datetime
from ..logger import setup_logger


logger = setup_logger(__name__)


class EmailNotifier:
    """Send email notifications with AI news digest"""

    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_user: Optional[str] = None,
        smtp_password: Optional[str] = None,
        email_from: Optional[str] = None,
        email_to: Optional[str] = None
    ):
        """
        Initialize EmailNotifier.

        Args:
            smtp_host: SMTP server host
            smtp_port: SMTP server port
            smtp_user: SMTP username
            smtp_password: SMTP password
            email_from: Sender email address
            email_to: Recipient email address

        All parameters default to environment variables if not provided.
        """
        self.smtp_host = smtp_host or os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = smtp_port or int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = smtp_user or os.getenv("SMTP_USER")
        self.smtp_password = smtp_password or os.getenv("SMTP_PASSWORD")
        self.email_from = email_from or os.getenv("EMAIL_FROM")
        self.email_to = email_to or os.getenv("EMAIL_TO")

        # Validate required fields
        if not all([self.smtp_user, self.smtp_password, self.email_from, self.email_to]):
            logger.warning(
                "Email notifier not fully configured. "
                "Required: SMTP_USER, SMTP_PASSWORD, EMAIL_FROM, EMAIL_TO"
            )

        logger.info(f"EmailNotifier initialized (SMTP: {self.smtp_host}:{self.smtp_port})")

    def send(self, content: str, subject: Optional[str] = None) -> bool:
        """
        Send email notification with news digest.

        Args:
            content: Email body content (news digest)
            subject: Email subject. If None, uses default with current date

        Returns:
            True if email sent successfully, False otherwise
        """
        if not all([self.smtp_user, self.smtp_password, self.email_from, self.email_to]):
            logger.error("Email notifier is not fully configured. Skipping email send.")
            return False

        try:
            # Create default subject if not provided
            if subject is None:
                today = datetime.now().strftime("%Y-%m-%d")
                subject = f"AI News Digest - {today}"

            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.email_from
            msg["To"] = self.email_to

            # Create plain text and HTML versions
            text_part = MIMEText(content, "plain", "utf-8")
            html_content = self._create_html_email(content, subject)
            html_part = MIMEText(html_content, "html", "utf-8")

            # Attach parts (plain text first, then HTML as fallback)
            msg.attach(text_part)
            msg.attach(html_part)

            logger.info(f"Sending email to {self.email_to}")

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            logger.info("Email sent successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}", exc_info=True)
            return False

    def _create_html_email(self, content: str, subject: str) -> str:
        """
        Create HTML version of email.

        Args:
            content: Plain text content
            subject: Email subject

        Returns:
            HTML formatted email
        """
        # Convert plain text to HTML (basic formatting)
        html_content = content.replace("\n", "<br>")

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                .content {{
                    background-color: #f9f9f9;
                    padding: 20px;
                    border-radius: 5px;
                    margin-top: 20px;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <h1>{subject}</h1>
            <div class="content">
                {html_content}
            </div>
            <div class="footer">
                <p>This email was automatically generated by AI News Bot</p>
                <p>Powered by Anthropic Claude</p>
            </div>
        </body>
        </html>
        """
        return html
