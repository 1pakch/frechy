"""Session management and main exercise loop."""

import json
import random
import sys
from datetime import datetime

sys.path.insert(0, '/home/ilya/repos/frechy/src')

try:
    import termios
    import tty
except ImportError:
    termios = None
    tty = None

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
            key_mapping = None
            shuffled_words = None
        else:
            shuffled_words = self.shuffle_words(exercise.correct_french)
            key_mapping = self.create_key_mapping(shuffled_words)
            display.show_exercise_word_order(exercise, shuffled_words, key_mapping, self.exercise_count)

        attempt_num = 1
        total_hints_used = 0

        while True:
            # Get user input
            if self.mode == PracticeMode.WORD_ORDER:
                user_answer, hints_requested = self.get_word_order_input(key_mapping, exercise)

                # If user requested hint
                if user_answer is None:
                    hint = self.generate_hint(exercise, "")
                    display.show_hint(hint)
                    total_hints_used = hints_requested
                    # Show exercise again and continue
                    display.show_exercise_word_order(exercise, shuffled_words, key_mapping, self.exercise_count)
                    continue
            else:
                user_input = input("> ").strip()
                if not user_input:
                    continue
                user_answer = user_input
                hints_requested = 0

            # Validate answer via LLM
            is_correct, feedback = self.validate_answer(exercise, user_answer)

            # Save attempt
            self.db.create_attempt(
                exercise_id=exercise.id,
                attempt_number=attempt_num,
                user_answer=user_answer,
                is_correct=is_correct,
                hints_used=total_hints_used
            )

            if is_correct:
                display.show_correct()
                return attempt_num == 1
            else:
                display.show_incorrect(feedback)
                action = display.get_user_action()

                if action == "retry":
                    attempt_num += 1
                    total_hints_used = 0
                    # Show exercise again for word-order mode
                    if self.mode == PracticeMode.WORD_ORDER:
                        display.show_exercise_word_order(exercise, shuffled_words, key_mapping, self.exercise_count)
                    continue
                elif action == "hint":
                    hint = self.generate_hint(exercise, user_answer)
                    display.show_hint(hint)
                    total_hints_used += 1
                    # Show exercise again for word-order mode
                    if self.mode == PracticeMode.WORD_ORDER:
                        display.show_exercise_word_order(exercise, shuffled_words, key_mapping, self.exercise_count)
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

    def create_key_mapping(self, words: list[str]) -> dict[str, str]:
        """Create randomized key mapping for words using home row keys.

        Args:
            words: List of words to map

        Returns:
            Dict mapping keys to words (e.g., {'a': 'le', 's': 'chat'})
        """
        # Home row keys, then top row if needed
        available_keys = list('asdfghjkl;') + list('qwertyuiop')

        if len(words) > len(available_keys):
            raise ValueError(f"Too many words ({len(words)}), max supported is {len(available_keys)}")

        # Shuffle keys and assign to words
        keys = available_keys[:len(words)]
        random.shuffle(keys)

        return {key: word for key, word in zip(keys, words)}

    def get_char(self) -> str:
        """Get a single character from stdin without echo.

        Returns:
            Single character string
        """
        if termios is None or tty is None:
            # Fallback for systems without termios (Windows)
            return sys.stdin.read(1)

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char

    def get_word_order_input(self, key_mapping: dict[str, str], exercise: Exercise) -> tuple[str | None, int]:
        """Interactive word-order input with live preview.

        Args:
            key_mapping: Dict mapping keys to words
            exercise: Current exercise

        Returns:
            Tuple of (user_answer, hints_used). user_answer is None if user requested hint.
        """
        selected_words = []
        hints_used = 0
        reverse_mapping = {word: key for key, word in key_mapping.items()}

        # Show initial preview
        display.show_word_order_preview(selected_words)

        while True:
            char = self.get_char()

            # Handle special characters
            if char == '\x7f' or char == '\x08':  # Backspace/Delete
                if selected_words:
                    selected_words.pop()
                    display.show_word_order_preview(selected_words)
            elif char == '?':
                # Request hint
                print()  # New line after preview
                return None, hints_used + 1
            elif char == '\r' or char == '\n':  # Enter
                # Submit answer
                if len(selected_words) == len(key_mapping):
                    print()  # New line after preview
                    return " ".join(selected_words), hints_used
            elif char == '\x03':  # Ctrl+C
                print()
                self.end()
                sys.exit(0)
            elif char in key_mapping:
                # Valid key pressed - add word if not already selected
                word = key_mapping[char]
                if word not in selected_words:
                    selected_words.append(word)
                    display.show_word_order_preview(selected_words)

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
