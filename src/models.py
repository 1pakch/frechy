"""Data models for Frechy."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PracticeMode(str, Enum):
    """Practice modes for exercises.

    - TRANSLATION: User translates English to French
    - WORD_ORDER: User arranges numbered French words in correct order
    """

    TRANSLATION = "translation"
    WORD_ORDER = "word-order"


@dataclass
class Exercise:
    """Represents a single practice exercise."""

    id: int | None
    session_id: int
    topic: str
    english_text: str
    correct_french: str
    timestamp: datetime | None = None


@dataclass
class Attempt:
    """Represents a user attempt at an exercise."""

    id: int | None
    exercise_id: int
    attempt_number: int
    user_answer: str
    is_correct: bool
    hints_used: int
    timestamp: datetime | None = None


@dataclass
class SessionStats:
    """Session statistics for display at the end."""

    total_exercises: int
    correct_first_try: int
    duration_minutes: int

    @property
    def accuracy(self) -> float:
        """Calculate accuracy percentage."""
        if self.total_exercises == 0:
            return 0.0
        return self.correct_first_try / self.total_exercises * 100
