"""
Web Search Tool for fetching real-time news
"""
import os
import requests
from typing import List, Dict, Optional
from .logger import setup_logger


logger = setup_logger(__name__)


class WebSearchTool:
    """Tool for searching the web to fetch current AI news"""

    def __init__(self):
        """Initialize the web search tool"""
        # Using DuckDuckGo's API as a free alternative
        # Could also integrate with Google Custom Search, Brave Search, etc.
        self.search_api_url = "https://api.duckduckgo.com/"
        logger.info("WebSearchTool initialized")

    def search_news(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Search for news articles related to the query.

        Args:
            query: Search query string
            max_results: Maximum number of results to return

        Returns:
            List of search results with title, snippet, and url
        """
        try:
            logger.info(f"Searching for: {query}")

            # Use DuckDuckGo instant answer API
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1,
                't': 'ai-news-bot'
            }

            response = requests.get(self.search_api_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = []

            # Extract related topics if available
            if 'RelatedTopics' in data:
                for topic in data['RelatedTopics'][:max_results]:
                    if isinstance(topic, dict) and 'Text' in topic:
                        result = {
                            'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' '),
                            'snippet': topic.get('Text', ''),
                            'url': topic.get('FirstURL', '')
                        }
                        if result['snippet']:
                            results.append(result)

            # If we have an abstract, add it as the first result
            if data.get('Abstract'):
                results.insert(0, {
                    'title': data.get('Heading', query),
                    'snippet': data['Abstract'],
                    'url': data.get('AbstractURL', '')
                })

            logger.info(f"Found {len(results)} search results")
            return results[:max_results]

        except Exception as e:
            logger.error(f"Search failed: {str(e)}", exc_info=True)
            return []

    def search_ai_news(self, max_results: int = 15) -> str:
        """
        Search for recent AI news and format results.

        Args:
            max_results: Maximum number of results

        Returns:
            Formatted string with search results
        """
        # Search queries for different aspects of AI news
        queries = [
            "artificial intelligence news 2025",
            "AI breakthroughs 2025",
            "machine learning updates 2025",
            "AI product launches 2025",
            "OpenAI ChatGPT news 2025"
        ]

        all_results = []

        for query in queries:
            results = self.search_news(query, max_results=3)
            all_results.extend(results)

        if not all_results:
            logger.warning("No search results found")
            return "No recent news found via web search."

        # Format results
        formatted = "Recent AI News from Web Search:\n\n"
        for i, result in enumerate(all_results[:max_results], 1):
            formatted += f"{i}. {result['title']}\n"
            formatted += f"   {result['snippet']}\n"
            if result['url']:
                formatted += f"   Source: {result['url']}\n"
            formatted += "\n"

        return formatted


def get_search_tool_definition() -> Dict:
    """
    Get the tool definition for Claude API tool calling.

    Returns:
        Tool definition dict for Anthropic API
    """
    return {
        "name": "web_search",
        "description": "Search the web for current AI news and information. Use this tool to find the most recent AI-related news, breakthroughs, product launches, and developments from 2025. This is essential for getting up-to-date information beyond the model's training data.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to find relevant AI news. Examples: 'AI news 2025', 'OpenAI GPT updates', 'machine learning breakthroughs'"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of search results to return (default: 10)",
                    "default": 10
                }
            },
            "required": ["query"]
        }
    }
