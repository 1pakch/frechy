"""CLI entry point for Frechy."""

import argparse
import sys
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Add src to path for imports
sys.path.insert(0, '/home/ilya/repos/frechy/src')

from db import Database
from models import PracticeMode
from session import Session
from topics import TopicRegistry
import display

# Import topics modules to trigger registration
import topics.pronouns


def parse_args():
    """Parse command line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Frechy - French grammar practice CLI"
    )
    parser.add_argument(
        "-t", "--topic",
        help="Topic to practice (e.g., pronouns.direct-object)"
    )
    parser.add_argument(
        "-m", "--mode",
        choices=[m.value for m in PracticeMode],
        help="Practice mode"
    )
    parser.add_argument(
        "--list-topics",
        nargs="?",
        const="",
        metavar="CATEGORY",
        help="List available topics (optionally filter by category)"
    )
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Handle --list-topics
    if args.list_topics is not None:
        category = args.list_topics if args.list_topics else None
        display.display_topics(category)
        return

    # Validate required arguments
    if not args.topic or not args.mode:
        print("Error: --topic and --mode are required")
        print("Run with --list-topics to see available topics")
        sys.exit(1)

    # Validate topic exists
    topic_config = TopicRegistry.get_topic(args.topic)
    if not topic_config:
        print(f"Error: Unknown topic '{args.topic}'")
        print("\nRun with --list-topics to see available topics")
        sys.exit(1)

    # Validate mode is supported
    mode = PracticeMode(args.mode)
    if mode not in topic_config.supported_modes:
        print(f"Error: Topic '{args.topic}' doesn't support mode '{args.mode}'")
        modes_str = ", ".join(m.value for m in topic_config.supported_modes)
        print(f"Supported modes: {modes_str}")
        sys.exit(1)

    # Initialize database
    try:
        db = Database()
    except Exception as e:
        print(f"Error: Failed to initialize database: {e}")
        sys.exit(1)

    # Create and run session
    session = Session(db, topic_config, mode)

    try:
        session.run()
    except KeyboardInterrupt:
        print("\n")
        session.end()
    except EOFError:
        print("\n")
        session.end()
    except Exception as e:
        print(f"\nError: {e}")
        session.end()
        sys.exit(1)


if __name__ == "__main__":
    main()
