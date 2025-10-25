"""
AI News Generator using Anthropic API
"""
import os
from typing import Dict, List, Optional
from anthropic import Anthropic
from .logger import setup_logger


logger = setup_logger(__name__)


class NewsGenerator:
    """Generate AI news digest using Anthropic's Claude API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the NewsGenerator.

        Args:
            api_key: Anthropic API key. If None, will read from ANTHROPIC_API_KEY env var

        Raises:
            ValueError: If API key is not provided and not in environment
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key must be provided or set in ANTHROPIC_API_KEY environment variable"
            )

        self.client = Anthropic(api_key=self.api_key)
        logger.info("NewsGenerator initialized successfully")

    def generate_news_digest(
        self,
        topics: List[str],
        prompt_template: str,
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 2000
    ) -> str:
        """
        Generate a news digest based on provided topics.

        Args:
            topics: List of topics to cover in the news digest
            prompt_template: Template string with {topics} placeholder
            model: Claude model to use
            max_tokens: Maximum tokens in response

        Returns:
            Generated news digest as string

        Raises:
            Exception: If API call fails
        """
        try:
            # Format topics as a bulleted list
            topics_formatted = "\n".join([f"- {topic}" for topic in topics])

            # Create the full prompt
            prompt = prompt_template.format(topics=topics_formatted)

            logger.info(f"Generating news digest with model: {model}")
            logger.debug(f"Topics: {topics}")

            # Call Anthropic API
            message = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the response text
            response_text = message.content[0].text

            logger.info("News digest generated successfully")
            logger.debug(f"Response length: {len(response_text)} characters")

            return response_text

        except Exception as e:
            logger.error(f"Failed to generate news digest: {str(e)}", exc_info=True)
            raise

    def generate_with_retry(
        self,
        topics: List[str],
        prompt_template: str,
        max_retries: int = 3,
        **kwargs
    ) -> str:
        """
        Generate news digest with retry logic.

        Args:
            topics: List of topics to cover
            prompt_template: Template string with {topics} placeholder
            max_retries: Maximum number of retry attempts
            **kwargs: Additional arguments passed to generate_news_digest

        Returns:
            Generated news digest as string

        Raises:
            Exception: If all retries fail
        """
        last_exception = None

        for attempt in range(max_retries):
            try:
                return self.generate_news_digest(topics, prompt_template, **kwargs)
            except Exception as e:
                last_exception = e
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt < max_retries - 1:
                    logger.info("Retrying...")

        logger.error(f"All {max_retries} attempts failed")
        raise last_exception
