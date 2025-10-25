"""
Webhook notification module
"""
import os
import requests
from typing import Optional, Dict, Any
from datetime import datetime
from ..logger import setup_logger


logger = setup_logger(__name__)


class WebhookNotifier:
    """Send webhook notifications with AI news digest"""

    def __init__(
        self,
        webhook_url: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize WebhookNotifier.

        Args:
            webhook_url: Webhook URL to send notifications to
            timeout: Request timeout in seconds
        """
        self.webhook_url = webhook_url or os.getenv("WEBHOOK_URL")
        self.timeout = timeout

        if not self.webhook_url:
            logger.warning("Webhook URL not configured")
        else:
            logger.info(f"WebhookNotifier initialized (URL: {self._mask_url(self.webhook_url)})")

    def send(
        self,
        content: str,
        title: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send webhook notification with news digest.

        Args:
            content: News digest content
            title: Title for the notification. If None, uses default with current date
            additional_data: Additional data to include in webhook payload

        Returns:
            True if webhook sent successfully, False otherwise
        """
        if not self.webhook_url:
            logger.error("Webhook URL is not configured. Skipping webhook send.")
            return False

        try:
            # Create default title if not provided
            if title is None:
                today = datetime.now().strftime("%Y-%m-%d")
                title = f"AI News Digest - {today}"

            # Prepare payload
            payload = {
                "title": title,
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "source": "AI News Bot"
            }

            # Add additional data if provided
            if additional_data:
                payload.update(additional_data)

            logger.info(f"Sending webhook to {self._mask_url(self.webhook_url)}")
            logger.debug(f"Payload keys: {list(payload.keys())}")

            # Send webhook
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )

            # Check response
            response.raise_for_status()

            logger.info(f"Webhook sent successfully (status: {response.status_code})")
            return True

        except requests.exceptions.Timeout:
            logger.error(f"Webhook request timed out after {self.timeout} seconds")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send webhook: {str(e)}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending webhook: {str(e)}", exc_info=True)
            return False

    def _mask_url(self, url: str) -> str:
        """
        Mask sensitive parts of URL for logging.

        Args:
            url: Original URL

        Returns:
            Masked URL
        """
        if not url:
            return ""

        # Keep protocol and domain, mask path
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return f"{parsed.scheme}://{parsed.netloc}/***"
        except Exception:
            return "***"
