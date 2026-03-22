"""Central registry for all available practice topics."""

import sys
sys.path.insert(0, '/home/ilya/repos/frechy/src')

from topics.base import TopicConfig


class TopicRegistry:
    """Central registry for all available practice topics."""

    _topics: dict[str, TopicConfig] = {}

    @classmethod
    def register(cls, topic: TopicConfig) -> None:
        """Register a topic. Called during module import."""
        cls._topics[topic.full_key] = topic

    @classmethod
    def get_topic(cls, full_key: str) -> TopicConfig | None:
        """Get topic by full key (e.g., 'pronouns.direct-object')"""
        return cls._topics.get(full_key)

    @classmethod
    def list_topics(cls, category: str | None = None) -> list[TopicConfig]:
        """List all topics or filter by category"""
        if category:
            return [t for t in cls._topics.values() if t.category == category]
        return list(cls._topics.values())

    @classmethod
    def list_categories(cls) -> list[str]:
        """List all available categories"""
        categories = {t.category for t in cls._topics.values()}
        return sorted(categories)
