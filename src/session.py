"""Session management and main exercise loop."""

import json
import random
import sys
from datetime import datetime

sys.path.insert(0, '/home/ilya/repos/frechy/src')

from db import Database
from llm import LLMClient
from models import Exercise, PracticeMode, SessionStats
from topics.base import TopicConfig
from prompts.pronouns import (
    generate_exercise_prompt,
    validate_answer_prompt,
    generate_hint_prompt
)
import display


class Session:
    """Manages a practice session with exercises and user interaction."""

    def __init__(self, db: Database, topic_config: TopicConfig, mode: PracticeMode):
        """Initialize session.

        Args:
            db: Database instance
            topic_config: Topic configuration
            mode: Practice mode (translation or word-order)
        """
        self.db = db
        self.topic_config = topic_config
        self.mode = mode
        self.llm = LLMClient()
        self.session_id = self.db.create_session(
            user_name="ilya",
            topic=topic_config.full_key,
            mode=mode.value
        )
        self.exercise_count = 0
        self.correct_first_try_count = 0
        self.start_time = datetime.now()

    def run(self):
        """Main exercise loop - runs until user quits."""
        while True:
            self.exercise_count += 1
            exercise = self.generate_exercise()
            self.db.create_exercise(exercise)

            is_correct_first_try = self.present_and_handle_exercise(exercise)
            if is_correct_first_try:
                self.correct_first_try_count += 1

    def generate_exercise(self) -> Exercise:
        """Generate exercise via LLM.

        Returns:
            New Exercise instance

        Raises:
            Exception: If LLM generation fails after retries
        """
        max_attempts = 2
        for attempt in range(max_attempts):
            try:
                prompt = generate_exercise_prompt(self.topic_config)
                response = self.llm.complete(prompt)
                data = self.llm.parse_json(response)

                # Validate required fields
                if "english" not in data or "correct_french" not in data:
                    if attempt < max_attempts - 1:
                        continue
                    raise Exception("Invalid exercise format from LLM")

                return Exercise(
                    id=None,
                    session_id=self.session_id,
                    topic=self.topic_config.full_key,
                    english_text=data["english"],
                    correct_french=data["correct_french"]
                )
            except json.JSONDecodeError:
                if attempt < max_attempts - 1:
                    continue
                raise Exception("Failed to parse exercise JSON")

        raise Exception("Failed to generate exercise")

    def present_and_handle_exercise(self, exercise: Exercise) -> bool:
        """Present exercise, get answer, handle retry/hint/show.

        Args:
            exercise: Exercise to present

        Returns:
            True if user got it correct on first try, False otherwise
        """
        if self.mode == PracticeMode.TRANSLATION:
            display.show_exercise_translation(exercise, self.exercise_count)
            shuffled_words = None
        else:
            shuffled_words = self.shuffle_words(exercise.correct_french)
            display.show_exercise_word_order(exercise, shuffled_words, self.exercise_count)

        attempt_num = 1
        hints_used = 0

        while True:
            user_input = input("> ").strip()

            # Handle empty input
            if not user_input:
                continue

            # Convert word-order input to actual sentence
            if self.mode == PracticeMode.WORD_ORDER:
                user_answer = self.reconstruct_from_indices(user_input, shuffled_words)
                if user_answer is None:
                    display.console.print("[yellow]Enter numbers like: 3 2 1[/yellow]")
                    continue
            else:
                user_answer = user_input

            # Validate answer via LLM
            is_correct, feedback = self.validate_answer(exercise, user_answer)

            # Save attempt
            self.db.create_attempt(
                exercise_id=exercise.id,
                attempt_number=attempt_num,
                user_answer=user_answer,
                is_correct=is_correct,
                hints_used=hints_used
            )

            if is_correct:
                display.show_correct()
                return attempt_num == 1
            else:
                display.show_incorrect(feedback)
                action = display.get_user_action()

                if action == "retry":
                    attempt_num += 1
                    hints_used = 0
                    continue
                elif action == "hint":
                    hint = self.generate_hint(exercise, user_answer)
                    display.show_hint(hint)
                    hints_used += 1
                    continue
                elif action == "show":
                    display.show_answer(exercise.correct_french)
                    return False
                elif action == "quit":
                    self.end()
                    sys.exit(0)

    def shuffle_words(self, sentence: str) -> list[str]:
        """Shuffle words in a sentence randomly.

        Args:
            sentence: French sentence to shuffle

        Returns:
            List of shuffled words
        """
        words = sentence.split()
        shuffled = words.copy()
        random.shuffle(shuffled)
        return shuffled

    def reconstruct_from_indices(self, user_input: str, words: list[str]) -> str | None:
        """Reconstruct sentence from user's number input.

        Args:
            user_input: User's input (e.g., "3 2 1" or "321")
            words: List of shuffled words

        Returns:
            Reconstructed sentence or None if invalid input
        """
        # Remove spaces and parse
        indices_str = user_input.replace(" ", "").replace("-", "")

        try:
            # Parse as individual digits
            indices = [int(c) for c in indices_str]

            # Validate indices
            if len(indices) != len(words):
                return None
            if any(i < 1 or i > len(words) for i in indices):
                return None

            # Reconstruct sentence (convert from 1-based to 0-based indexing)
            return " ".join(words[i - 1] for i in indices)
        except ValueError:
            return None

    def validate_answer(self, exercise: Exercise, user_answer: str) -> tuple[bool, str]:
        """Validate answer via LLM.

        Args:
            exercise: Current exercise
            user_answer: User's answer

        Returns:
            Tuple of (is_correct, feedback)
        """
        try:
            prompt = validate_answer_prompt(
                self.topic_config,
                exercise.correct_french,
                user_answer
            )
            response = self.llm.complete(prompt)
            data = self.llm.parse_json(response)
            return data.get("is_correct", False), data.get("feedback", "")
        except Exception:
            # If validation fails, fall back to exact match
            return user_answer.lower() == exercise.correct_french.lower(), ""

    def generate_hint(self, exercise: Exercise, user_answer: str) -> str:
        """Generate hint via LLM.

        Args:
            exercise: Current exercise
            user_answer: User's incorrect answer

        Returns:
            Hint text
        """
        try:
            prompt = generate_hint_prompt(
                self.topic_config,
                exercise.english_text,
                exercise.correct_french,
                user_answer
            )
            return self.llm.complete(prompt)
        except Exception:
            return "Try focusing on the word order and pronoun placement."

    def calculate_duration(self) -> int:
        """Calculate session duration in minutes.

        Returns:
            Duration in minutes
        """
        duration = datetime.now() - self.start_time
        return max(1, int(duration.total_seconds() / 60))

    def end(self):
        """End session, update DB, show summary."""
        stats = SessionStats(
            total_exercises=self.exercise_count,
            correct_first_try=self.correct_first_try_count,
            duration_minutes=self.calculate_duration()
        )
        self.db.end_session(self.session_id, stats)
        display.show_session_summary(
            stats,
            self.topic_config.full_key,
            self.mode.value
        )
