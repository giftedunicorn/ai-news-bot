#!/usr/bin/env python3
"""
Example usage of AI News Bot components

This script demonstrates how to use the various components programmatically.
"""
from src.config import Config
from src.logger import setup_logger
from src.news_generator import NewsGenerator
from src.notifiers import EmailNotifier, WebhookNotifier


def example_basic_usage():
    """Basic usage example"""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)

    # Setup logger
    logger = setup_logger("example", level="INFO")

    # Load configuration
    config = Config()

    # Initialize news generator
    news_gen = NewsGenerator()

    # Generate news
    news = news_gen.generate_news_digest(
        topics=config.news_topics,
        prompt_template=config.news_prompt_template
    )

    print(f"\nGenerated news ({len(news)} characters):")
    print("-" * 60)
    print(news[:300] + "..." if len(news) > 300 else news)
    print("-" * 60)


def example_custom_topics():
    """Example with custom topics"""
    print("\n" + "=" * 60)
    print("Example 2: Custom Topics")
    print("=" * 60)

    # Custom topics
    custom_topics = [
        "GPT-4 and GPT-5 developments",
        "Open source AI models",
        "AI in healthcare",
    ]

    custom_prompt = """Provide a brief summary of recent developments in:
{topics}

Keep it concise (3-4 sentences per topic)."""

    # Generate with custom settings
    news_gen = NewsGenerator()
    news = news_gen.generate_news_digest(
        topics=custom_topics,
        prompt_template=custom_prompt,
        max_tokens=1000
    )

    print(f"\nGenerated custom news:")
    print("-" * 60)
    print(news)
    print("-" * 60)


def example_notifications():
    """Example of sending notifications"""
    print("\n" + "=" * 60)
    print("Example 3: Send Notifications")
    print("=" * 60)

    # Sample news content
    news_content = "This is a sample AI news digest for testing."

    # Email notification
    print("\nAttempting email notification...")
    email_notifier = EmailNotifier()
    email_result = email_notifier.send(
        content=news_content,
        subject="Test: AI News Digest"
    )
    print(f"Email sent: {email_result}")

    # Webhook notification
    print("\nAttempting webhook notification...")
    webhook_notifier = WebhookNotifier()
    webhook_result = webhook_notifier.send(
        content=news_content,
        title="Test: AI News Digest",
        additional_data={"test": True}
    )
    print(f"Webhook sent: {webhook_result}")


def example_error_handling():
    """Example with error handling and retries"""
    print("\n" + "=" * 60)
    print("Example 4: Error Handling with Retries")
    print("=" * 60)

    logger = setup_logger("example_retry", level="INFO")

    try:
        news_gen = NewsGenerator()
        config = Config()

        # Use retry mechanism
        news = news_gen.generate_with_retry(
            topics=config.news_topics,
            prompt_template=config.news_prompt_template,
            max_retries=3
        )

        logger.info("News generated successfully with retry protection")
        print(f"\nNews preview: {news[:200]}...")

    except Exception as e:
        logger.error(f"Failed to generate news after retries: {e}")


def example_config_access():
    """Example of accessing configuration"""
    print("\n" + "=" * 60)
    print("Example 5: Configuration Access")
    print("=" * 60)

    config = Config()

    print(f"\nNews topics ({len(config.news_topics)} topics):")
    for i, topic in enumerate(config.news_topics, 1):
        print(f"  {i}. {topic}")

    print(f"\nLog level: {config.log_level}")
    print(f"Notification methods: {config.notification_methods}")

    # Access custom config values
    custom_value = config.get("news.topics", default=[])
    print(f"\nCustom config access: {len(custom_value)} topics")


def main():
    """Run all examples"""
    import sys

    print("\n" + "=" * 60)
    print("AI News Bot - Usage Examples")
    print("=" * 60)
    print("\nThese examples demonstrate various features of the bot.")
    print("Note: Some examples require proper API keys and configuration.\n")

    examples = [
        ("Basic Usage", example_basic_usage),
        ("Custom Topics", example_custom_topics),
        ("Notifications", example_notifications),
        ("Error Handling", example_error_handling),
        ("Configuration", example_config_access),
    ]

    # Show menu
    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  0. Run all examples")

    try:
        choice = input("\nSelect example (0-5): ").strip()

        if choice == "0":
            for name, func in examples:
                try:
                    func()
                except Exception as e:
                    print(f"\n✗ Error in {name}: {str(e)}")
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            idx = int(choice) - 1
            examples[idx][1]()
        else:
            print("Invalid choice")
            return 1

        print("\n" + "=" * 60)
        print("Examples completed!")
        print("=" * 60)

        return 0

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
        return 130
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
