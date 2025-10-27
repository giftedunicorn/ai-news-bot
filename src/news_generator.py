"""
AI News Generator using Anthropic API
"""
import os
from typing import Dict, List, Optional
from anthropic import Anthropic
from .logger import setup_logger
from .web_search import WebSearchTool, get_search_tool_definition
from .news_fetcher import NewsFetcher


logger = setup_logger(__name__)


class NewsGenerator:
    """Generate AI news digest using Anthropic's Claude API"""

    def __init__(self, api_key: Optional[str] = None, enable_web_search: bool = False):
        """
        Initialize the NewsGenerator.

        Args:
            api_key: Anthropic API key. If None, will read from ANTHROPIC_API_KEY env var
            enable_web_search: Whether to enable web search tool for fetching current news

        Raises:
            ValueError: If API key is not provided and not in environment
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key must be provided or set in ANTHROPIC_API_KEY environment variable"
            )

        self.client = Anthropic(api_key=self.api_key)
        self.enable_web_search = enable_web_search
        self.search_tool = WebSearchTool() if enable_web_search else None
        self.news_fetcher = NewsFetcher()
        logger.info(f"NewsGenerator initialized successfully (web_search: {enable_web_search})")

    def generate_news_digest(
        self,
        topics: List[str],
        prompt_template: str,
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 2000,
        language: str = "en"
    ) -> str:
        """
        Generate a news digest based on provided topics.
        Uses web search tool to fetch current news when enabled.

        Args:
            topics: List of topics to cover in the news digest
            prompt_template: Template string with {topics} placeholder
            model: Claude model to use
            max_tokens: Maximum tokens in response
            language: Language code for the response (e.g., 'en', 'zh', 'es', 'fr', 'ja')

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

            # Add web search instruction if enabled
            if self.enable_web_search:
                prompt += "\n\nIMPORTANT: Use the web_search tool to find the most recent AI news from 2025. You can search 3-5 times with different queries to gather diverse news. After gathering news, create a comprehensive digest based on what you found."

            # Add language instruction if not English
            language_names = {
                "zh": "Chinese (中文)",
                "es": "Spanish (Español)",
                "fr": "French (Français)",
                "ja": "Japanese (日本語)",
                "de": "German (Deutsch)",
                "ko": "Korean (한국어)",
                "pt": "Portuguese (Português)",
                "ru": "Russian (Русский)",
                "ar": "Arabic (العربية)",
                "hi": "Hindi (हिन्दी)",
                "it": "Italian (Italiano)",
                "nl": "Dutch (Nederlands)",
            }

            if language and language.lower() != "en":
                language_name = language_names.get(language.lower(), language.upper())
                prompt += f"\n\nIMPORTANT: Please respond entirely in {language_name}."

            logger.info(f"Generating news digest with model: {model}, language: {language}, web_search: {self.enable_web_search}")
            logger.debug(f"Topics: {topics}")

            # Prepare messages and tools
            messages = [{"role": "user", "content": prompt}]
            tools = [get_search_tool_definition()] if self.enable_web_search else None

            # Agentic loop for tool use
            response_text = None
            max_iterations = 8  # Limit iterations to prevent excessive searches
            search_count = 0
            max_searches = 6  # Limit total number of searches

            for iteration in range(max_iterations):
                # Call Anthropic API
                if tools:
                    message = self.client.messages.create(
                        model=model,
                        max_tokens=max_tokens,
                        messages=messages,
                        tools=tools
                    )
                else:
                    message = self.client.messages.create(
                        model=model,
                        max_tokens=max_tokens,
                        messages=messages
                    )

                logger.debug(f"Iteration {iteration + 1}: stop_reason = {message.stop_reason}")

                # Check if we got a final response
                if message.stop_reason == "end_turn":
                    # Extract text from content blocks
                    for block in message.content:
                        if block.type == "text":
                            response_text = block.text
                            break
                    break

                # Check if Claude wants to use a tool
                elif message.stop_reason == "tool_use":
                    # Add assistant's response to messages
                    messages.append({
                        "role": "assistant",
                        "content": message.content
                    })

                    # Process tool calls
                    tool_results = []
                    for block in message.content:
                        if block.type == "tool_use":
                            tool_name = block.name
                            tool_input = block.input

                            logger.info(f"Tool call: {tool_name} with input: {tool_input}")

                            # Execute the tool
                            if tool_name == "web_search" and self.search_tool:
                                search_count += 1

                                # Check if we've exceeded max searches
                                if search_count > max_searches:
                                    result_text = "Maximum number of searches reached. Please create the digest based on the information gathered so far."
                                else:
                                    query = tool_input.get("query", "AI news 2025")
                                    max_results = tool_input.get("max_results", 10)
                                    search_results = self.search_tool.search_news(query, max_results)

                                    # Format search results
                                    if search_results:
                                        result_text = f"Search results for '{query}':\n\n"
                                        for i, result in enumerate(search_results, 1):
                                            result_text += f"{i}. {result['title']}\n"
                                            result_text += f"   {result['snippet']}\n"
                                            if result['url']:
                                                result_text += f"   URL: {result['url']}\n"
                                            result_text += "\n"
                                    else:
                                        result_text = f"No results found for '{query}'. Try a different query or proceed with the information you have."

                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": result_text
                                })

                    # Add tool results to messages
                    if tool_results:
                        messages.append({
                            "role": "user",
                            "content": tool_results
                        })
                    else:
                        # No valid tool results, break
                        break

                    # Force generation after max searches
                    if search_count >= max_searches:
                        logger.info(f"Reached max searches ({max_searches}), forcing final generation")
                        # Add a message to prompt Claude to generate final output
                        messages.append({
                            "role": "user",
                            "content": "You have gathered enough information. Please now create a comprehensive news digest based on all the search results you've collected."
                        })
                else:
                    # Unexpected stop reason
                    break

            # If we didn't get a response through the loop, extract from last message
            if response_text is None:
                for block in message.content:
                    if block.type == "text":
                        response_text = block.text
                        break

            if response_text is None:
                raise Exception("No text response received from Claude")

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

    def generate_news_digest_from_sources(
        self,
        prompt_template: str,
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 4000,
        language: str = "en",
        include_chinese: bool = True,
        max_items_per_source: int = 5
    ) -> str:
        """
        Fetch real-time news and generate a digest based on actual news articles.

        Args:
            prompt_template: Template for summarization instructions
            model: Claude model to use
            max_tokens: Maximum tokens in response
            language: Language code for the response
            include_chinese: Whether to include Chinese news sources
            max_items_per_source: Maximum items to fetch per source

        Returns:
            Generated news digest as string

        Raises:
            Exception: If fetching or generation fails
        """
        try:
            # Fetch real-time news
            logger.info("Fetching real-time AI news from sources...")
            news_data = self.news_fetcher.fetch_recent_news(
                include_chinese=include_chinese,
                max_items_per_source=max_items_per_source
            )

            if not news_data['international'] and not news_data['domestic']:
                logger.warning("No news items fetched, falling back to general news generation")
                # Fallback to the original method
                return self.generate_news_digest(
                    topics=["AI industry news"],
                    prompt_template=prompt_template,
                    model=model,
                    max_tokens=max_tokens,
                    language=language
                )

            # Format news for summarization
            formatted_news = self.news_fetcher.format_news_for_summary(news_data)

            # Create summarization prompt
            summarization_prompt = f"""Based on the following recent AI news articles, create a well-organized news digest.

{formatted_news}

Instructions:
{prompt_template}

IMPORTANT:
- Summarize and organize the ACTUAL news items provided above
- Focus on the most significant and recent developments
- Maintain accuracy - only include information from the provided articles
- Format the output in clean, readable markdown
- Include source attributions where appropriate
"""

            # Add language instruction if not English
            language_names = {
                "zh": "Chinese (中文)",
                "es": "Spanish (Español)",
                "fr": "French (Français)",
                "ja": "Japanese (日本語)",
                "de": "German (Deutsch)",
                "ko": "Korean (한국어)",
                "pt": "Portuguese (Português)",
                "ru": "Russian (Русский)",
                "ar": "Arabic (العربية)",
                "hi": "Hindi (हिन्दी)",
                "it": "Italian (Italiano)",
                "nl": "Dutch (Nederlands)",
            }

            if language and language.lower() != "en":
                language_name = language_names.get(language.lower(), language.upper())
                summarization_prompt += f"\n\nIMPORTANT: Please respond entirely in {language_name}."

            logger.info(f"Generating summary from {len(news_data['international']) + len(news_data['domestic'])} news items")

            # Call Anthropic API
            message = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": summarization_prompt}
                ]
            )

            # Extract the response text
            response_text = message.content[0].text

            logger.info("News digest generated successfully from real sources")
            logger.debug(f"Response length: {len(response_text)} characters")

            return response_text

        except Exception as e:
            logger.error(f"Failed to generate news digest from sources: {str(e)}", exc_info=True)
            raise
