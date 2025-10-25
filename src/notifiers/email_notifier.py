"""
Email notification module using Resend.com service
"""
import os
import resend
from typing import Optional
from datetime import datetime
from ..logger import setup_logger


logger = setup_logger(__name__)


class EmailNotifier:
    """Send email notifications with AI news digest using Resend.com"""

    def __init__(
        self,
        resend_api_key: Optional[str] = None,
        email_from: Optional[str] = None,
        email_to: Optional[str] = None
    ):
        """
        Initialize EmailNotifier with Resend.com.

        Args:
            resend_api_key: Resend API key
            email_from: Sender email address (must be verified in Resend)
            email_to: Recipient email address

        All parameters default to environment variables if not provided.
        """
        self.resend_api_key = resend_api_key or os.getenv("RESEND_API_KEY")
        self.email_from = email_from or os.getenv("EMAIL_FROM")
        self.email_to = email_to or os.getenv("EMAIL_TO")

        # Set the Resend API key
        if self.resend_api_key:
            resend.api_key = self.resend_api_key
        else:
            logger.warning("Resend API key not configured")

        # Validate required fields
        if not all([self.resend_api_key, self.email_from, self.email_to]):
            logger.warning(
                "Email notifier not fully configured. "
                "Required: RESEND_API_KEY, EMAIL_FROM, EMAIL_TO"
            )

        logger.info(f"EmailNotifier initialized with Resend.com (from: {self.email_from})")

    def send(self, content: str, subject: Optional[str] = None) -> bool:
        """
        Send email notification with news digest using Resend.

        Args:
            content: Email body content (news digest)
            subject: Email subject. If None, uses default with current date

        Returns:
            True if email sent successfully, False otherwise
        """
        if not all([self.resend_api_key, self.email_from, self.email_to]):
            logger.error("Email notifier is not fully configured. Skipping email send.")
            return False

        try:
            # Create default subject if not provided
            if subject is None:
                today = datetime.now().strftime("%Y-%m-%d")
                subject = f"AI News Digest - {today}"

            # Create HTML email content
            html_content = self._create_html_email(content, subject)

            logger.info(f"Sending email via Resend to {self.email_to}")

            # Send email using Resend
            params = {
                "from": self.email_from,
                "to": [self.email_to],
                "subject": subject,
                "html": html_content,
                "text": content,  # Plain text fallback
            }

            response = resend.Emails.send(params)

            logger.info(f"Email sent successfully via Resend (ID: {response.get('id', 'N/A')})")
            return True

        except Exception as e:
            logger.error(f"Failed to send email via Resend: {str(e)}", exc_info=True)
            return False

    def _create_html_email(self, content: str, subject: str) -> str:
        """
        Create HTML version of email with proper formatting.

        Args:
            content: Plain text content
            subject: Email subject

        Returns:
            HTML formatted email
        """
        import re

        # Convert content to HTML with smart formatting
        html_content = content

        # Convert section headers (lines ending with :) to h2
        html_content = re.sub(
            r'^([A-Z][^\n:]+:)\s*$',
            r'<h2>\1</h2>',
            html_content,
            flags=re.MULTILINE
        )

        # Convert numbered items (1. 2. 3. etc.) to styled divs
        html_content = re.sub(
            r'^(\d+)\.\s+(.+?)$',
            r'<div class="news-item"><div class="news-number">\1</div><div class="news-content">\2</div></div>',
            html_content,
            flags=re.MULTILINE
        )

        # Convert bullet points to list items
        html_content = re.sub(
            r'^[\-\*]\s+(.+?)$',
            r'<li>\1</li>',
            html_content,
            flags=re.MULTILINE
        )

        # Wrap consecutive list items in ul tags
        html_content = re.sub(
            r'(<li>.*?</li>\s*)+',
            lambda m: '<ul>' + m.group(0) + '</ul>',
            html_content,
            flags=re.DOTALL
        )

        # Convert Source: lines to styled citations
        html_content = re.sub(
            r'Source:\s*(.+?)$',
            r'<div class="source">Source: \1</div>',
            html_content,
            flags=re.MULTILINE
        )

        # Convert remaining line breaks to <br> (but not inside already formatted elements)
        lines = html_content.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip() and not any(tag in line for tag in ['<h2>', '<div', '<li>', '<ul>', '</ul>']):
                formatted_lines.append(line + '<br>')
            else:
                formatted_lines.append(line)
        html_content = '\n'.join(formatted_lines)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
                    line-height: 1.6;
                    color: #24292e;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f6f8fa;
                }}
                .container {{
                    background-color: #ffffff;
                    border-radius: 8px;
                    padding: 30px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
                }}
                h1 {{
                    color: #0366d6;
                    font-size: 28px;
                    margin-bottom: 10px;
                    padding-bottom: 10px;
                    border-bottom: 3px solid #0366d6;
                }}
                h2 {{
                    color: #2c3e50;
                    font-size: 20px;
                    margin-top: 30px;
                    margin-bottom: 15px;
                    padding-bottom: 8px;
                    border-bottom: 2px solid #e1e4e8;
                }}
                .news-item {{
                    display: flex;
                    margin: 20px 0;
                    padding: 15px;
                    background-color: #f6f8fa;
                    border-left: 4px solid #0366d6;
                    border-radius: 4px;
                }}
                .news-number {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #0366d6;
                    min-width: 40px;
                    margin-right: 15px;
                }}
                .news-content {{
                    flex: 1;
                    line-height: 1.7;
                }}
                .source {{
                    font-size: 13px;
                    color: #586069;
                    margin-top: 8px;
                    font-style: italic;
                }}
                ul {{
                    margin: 10px 0;
                    padding-left: 20px;
                }}
                li {{
                    margin: 5px 0;
                    line-height: 1.6;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #e1e4e8;
                    text-align: center;
                    font-size: 13px;
                    color: #586069;
                }}
                .footer p {{
                    margin: 5px 0;
                }}
                a {{
                    color: #0366d6;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{subject}</h1>
                <div class="content">
                    {html_content}
                </div>
            </div>
            <div class="footer">
                <p>This email was automatically generated by AI News Bot</p>
                <p>Powered by Anthropic Claude</p>
            </div>
        </body>
        </html>
        """
        return html
