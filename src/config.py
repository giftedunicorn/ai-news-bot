"""
Configuration management for AI News Bot
"""
import os
import yaml
from typing import Dict, List, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from .logger import setup_logger


logger = setup_logger(__name__)


class Config:
    """Application configuration manager"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to config.yaml file. If None, searches for it in default locations
        """
        # Load environment variables from .env file
        load_dotenv()

        # Find and load YAML config
        self.config_path = self._find_config_file(config_path)
        self.config_data = self._load_yaml_config()

        logger.info(f"Configuration loaded from {self.config_path}")

    def _find_config_file(self, config_path: Optional[str] = None) -> Path:
        """
        Find the configuration file.

        Args:
            config_path: Explicit path to config file

        Returns:
            Path to configuration file

        Raises:
            FileNotFoundError: If config file cannot be found
        """
        if config_path:
            path = Path(config_path)
            if path.exists():
                return path
            raise FileNotFoundError(f"Config file not found: {config_path}")

        # Search in default locations
        search_paths = [
            Path("config.yaml"),
            Path("config.yml"),
            Path(__file__).parent.parent / "config.yaml",
            Path(__file__).parent.parent / "config.yml",
        ]

        for path in search_paths:
            if path.exists():
                return path

        raise FileNotFoundError(
            "Config file not found. Searched: " + ", ".join(str(p) for p in search_paths)
        )

    def _load_yaml_config(self) -> Dict[str, Any]:
        """
        Load YAML configuration file.

        Returns:
            Configuration dictionary
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config or {}
        except Exception as e:
            logger.error(f"Failed to load config file: {str(e)}")
            return {}

    @property
    def news_topics(self) -> List[str]:
        """Get list of news topics to cover"""
        return self.config_data.get("news", {}).get("topics", [
            "Latest AI developments and breakthroughs"
        ])

    @property
    def news_prompt_template(self) -> str:
        """Get the prompt template for news generation"""
        default_template = """You are an AI news curator. Please provide a concise daily digest of AI news and developments.

Focus on these topics:
{topics}

Requirements:
1. Provide 3-5 key news items or developments
2. Each item should include a brief description (2-3 sentences)
3. Focus on significant developments from the past 24-48 hours
4. Include context about why each item is important
5. Use a professional but accessible tone

Format your response as a structured news digest with clear sections."""

        return self.config_data.get("news", {}).get("prompt_template", default_template)

    @property
    def log_level(self) -> str:
        """Get logging level"""
        return self.config_data.get("logging", {}).get("level", "INFO")

    @property
    def log_format(self) -> str:
        """Get logging format"""
        return self.config_data.get("logging", {}).get(
            "format",
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    @property
    def notification_methods(self) -> List[str]:
        """Get enabled notification methods from environment"""
        methods_str = os.getenv("NOTIFICATION_METHODS", "")
        if not methods_str:
            return []
        return [m.strip().lower() for m in methods_str.split(",")]

    @property
    def ai_response_language(self) -> str:
        """Get the language for AI-generated content"""
        return os.getenv("AI_RESPONSE_LANGUAGE", "en").strip().lower()

    @property
    def enable_web_search(self) -> bool:
        """Get whether to enable web search for fetching current news"""
        env_value = os.getenv("ENABLE_WEB_SEARCH", "true").strip().lower()
        return env_value in ("true", "1", "yes", "on")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.

        Args:
            key: Dot-separated key path (e.g., "news.topics")
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config_data

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value
