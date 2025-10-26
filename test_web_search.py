#!/usr/bin/env python3
"""
Test script for web search functionality
"""
from src.web_search import WebSearchTool


def test_web_search():
    """Test the web search tool"""
    print("Testing Web Search Tool")
    print("=" * 60)

    tool = WebSearchTool()

    # Test searching for AI news
    print("\n1. Searching for 'AI news 2025'...")
    results = tool.search_news("AI news 2025", max_results=5)

    if results:
        print(f"\nFound {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   {result['snippet'][:100]}...")
            if result['url']:
                print(f"   URL: {result['url']}")
    else:
        print("No results found")

    print("\n" + "=" * 60)
    print("Test completed")


if __name__ == "__main__":
    test_web_search()
