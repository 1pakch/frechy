"""Base classes for topic configuration."""

from dataclasses import dataclass, field

from ..models import PracticeMode


@dataclass
class TopicConfig:
    """Configuration for a grammar practice topic.

    Example:
        TopicConfig(
            category="pronouns",
            key="direct-object",
            name="Direct Object Pronouns",
            description="Practice using le, la, les in present tense",
            grammar_focus=[
                "direct object pronouns (le, la, les)",
                "present tense",
                "placement before conjugated verb"
            ],
            prompt_hints=(
                "Direct object pronouns (le, la, les) are placed directly "
                "before the conjugated verb. Example: 'Je le vois' (I see him). "
                "Remember: le/la contract to l' before vowels."
            ),
            supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER]
        )
    """

    category: str  # "pronouns", "articles", "subjunctive"
    key: str  # "direct-object", "negation-reflexive"
    name: str  # Human-readable: "Direct Object Pronouns"
    description: str  # For --list-topics display
    grammar_focus: list[str]  # Hints for LLM about what to focus on
    prompt_hints: str  # Additional context for LLM generation
    supported_modes: list[PracticeMode] = field(
        default_factory=lambda: [PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER]
    )

    @property
    def full_key(self) -> str:
        """Returns 'category.key', e.g., 'pronouns.direct-object'"""
        return f"{self.category}.{self.key}"
