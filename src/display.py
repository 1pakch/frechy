"""Rich-based formatting and display utilities."""

import sys
sys.path.insert(0, '/home/ilya/repos/frechy/src')

from rich.console import Console
from rich.panel import Panel

from models import Exercise, SessionStats


console = Console()


def show_exercise_translation(exercise: Exercise, num: int):
    """Display translation mode exercise."""
    console.print(f"\n[bold]Exercise {num}[/bold]\n")
    console.print("Translate to French:")
    console.print(f"[cyan]{exercise.english_text}[/cyan]\n")


def show_exercise_word_order(exercise: Exercise, shuffled_words: list[str], key_mapping: dict[str, str], num: int):
    """Display word-order mode exercise with key-based selection.

    Args:
        exercise: Exercise instance with English text
        shuffled_words: List of shuffled French words (in display order)
        key_mapping: Dict mapping keys to words (e.g., {'a': 'le', 's': 'chat'})
        num: Exercise number
    """
    console.print(f"\n[bold]Exercise {num}[/bold]\n")
    console.print("Put these words in correct order:")

    # Display words with their assigned keys, in the order of shuffled_words
    # Create reverse mapping for lookup
    reverse_mapping = {word: key for key, word in key_mapping.items()}
    word_displays = [f"({reverse_mapping[word]}) {word}" for word in shuffled_words]
    console.print("  ".join(word_displays))

    console.print(f"\n[dim]English: {exercise.english_text}[/dim]")
    console.print(f"[dim]Press ? for hint, Backspace to undo[/dim]\n")


def show_word_order_preview(selected_words: list[str]):
    """Display live preview of selected words in word-order mode.

    Args:
        selected_words: List of words selected so far
    """
    if selected_words:
        preview = " ".join(selected_words) + " _"
    else:
        preview = "_"
    console.print(f"\r[cyan]Your answer: {preview}[/cyan]", end="")


def show_correct():
    """Display success message."""
    console.print("[green]✓ Correct![/green]\n")


def show_incorrect(feedback: str = ""):
    """Display failure message."""
    console.print("[red]✗ Incorrect[/red]\n")
    if feedback:
        console.print(f"[yellow]{feedback}[/yellow]\n")


def show_hint(hint: str):
    """Display hint with formatting."""
    console.print(Panel(hint, title="💡 Hint", border_style="yellow"))
    console.print()


def show_answer(correct: str):
    """Show correct answer."""
    console.print(f"The correct answer is: [green]{correct}[/green]\n")


def show_session_summary(stats: SessionStats, topic: str, mode: str):
    """Display final session summary."""
    console.print("\n[bold]Session Summary[/bold]")
    console.print("═" * 60)
    console.print(f"Topic:          {topic}")
    console.print(f"Mode:           {mode}")
    console.print(f"Duration:       {stats.duration_minutes} minutes")
    console.print(f"Total:          {stats.total_exercises} exercises")
    console.print(f"First try ✓:    {stats.correct_first_try} exercises")
    console.print(f"Accuracy:       {stats.accuracy:.1f}%")
    console.print("\nKeep practicing! 🇫🇷\n")


def get_user_action() -> str:
    """Prompt for R/H/S/Q action."""
    console.print("What would you like to do?")
    console.print("[R]etry   [H]int   [S]how answer   [Q]uit")

    while True:
        choice = input("> ").strip().lower()
        if choice in ["r", "retry"]:
            return "retry"
        elif choice in ["h", "hint"]:
            return "hint"
        elif choice in ["s", "show"]:
            return "show"
        elif choice in ["q", "quit"]:
            return "quit"
        else:
            console.print("[red]Invalid choice. Please enter R, H, S, or Q[/red]")


def display_topics(category: str | None = None):
    """Display available topics, optionally filtered by category."""
    from topics import TopicRegistry

    if category:
        topics = TopicRegistry.list_topics(category)
        if not topics:
            console.print(f"[red]No topics found in category '{category}'[/red]")
            return
        console.print(f"\n[bold]Available Topics - {category}[/bold]")
    else:
        topics = TopicRegistry.list_topics()
        console.print("\n[bold]Available Topics[/bold]")

    console.print("═" * 60)

    for topic in topics:
        console.print(f"\n[cyan]{topic.full_key}[/cyan]")
        console.print(f"  {topic.name}")
        console.print(f"  {topic.description}")
        modes_str = ", ".join(m.value for m in topic.supported_modes)
        console.print(f"  [dim]Modes: {modes_str}[/dim]")

    console.print()
