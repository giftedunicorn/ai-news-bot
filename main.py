#!/usr/bin/env python3
"""
AI News Bot - Main Application

Generates and distributes daily AI news digests using Anthropic's Claude API.
"""
import sys
from datetime import datetime
from src.config import Config
from src.logger import setup_logger
from src.news_generator import NewsGenerator
from src.notifiers import EmailNotifier, WebhookNotifier


def main():
    """Main application entry point"""
    try:
        # Load configuration
        config = Config()

        # Setup logger with config
        logger = setup_logger(
            "ai_news_bot",
            level=config.log_level,
            log_format=config.log_format
        )

        logger.info("=" * 60)
        logger.info("AI News Bot Starting")
        logger.info(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Language: {config.ai_response_language}")
        logger.info("=" * 60)

        # Initialize news generator
        logger.info("Initializing news generator...")
        news_gen = NewsGenerator()

        # Generate news digest
        logger.info("Generating AI news digest...")
        news_digest = news_gen.generate_with_retry(
            topics=config.news_topics,
            prompt_template=config.news_prompt_template,
            language=config.ai_response_language,
            max_retries=3
        )

        logger.info(f"News digest generated ({len(news_digest)} characters)")
        logger.info("-" * 60)
        logger.info("News Digest Preview:")
        logger.info("-" * 60)
        # Print first 500 characters as preview
        preview = news_digest[:500] + "..." if len(news_digest) > 500 else news_digest
        logger.info(preview)
        logger.info("-" * 60)

        # Get enabled notification methods
        notification_methods = config.notification_methods
        logger.info(f"Enabled notification methods: {notification_methods}")

        # Track notification results
        results = {"sent": [], "failed": []}

        # Send email notification if enabled
        if "email" in notification_methods:
            logger.info("Sending email notification...")
            email_notifier = EmailNotifier()
            if email_notifier.send(news_digest):
                results["sent"].append("email")
                logger.info("Email notification sent successfully")
            else:
                results["failed"].append("email")
                logger.warning("Email notification failed")

        # Send webhook notification if enabled
        if "webhook" in notification_methods:
            logger.info("Sending webhook notification...")
            webhook_notifier = WebhookNotifier()
            if webhook_notifier.send(news_digest):
                results["sent"].append("webhook")
                logger.info("Webhook notification sent successfully")
            else:
                results["failed"].append("webhook")
                logger.warning("Webhook notification failed")

        # Summary
        logger.info("=" * 60)
        logger.info("AI News Bot Completed")
        logger.info(f"Successfully sent: {', '.join(results['sent']) if results['sent'] else 'None'}")
        if results["failed"]:
            logger.warning(f"Failed to send: {', '.join(results['failed'])}")
        logger.info("=" * 60)

        # Return exit code based on results
        if notification_methods and not results["sent"]:
            logger.error("All notifications failed")
            return 1

        return 0

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        return 130

    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
