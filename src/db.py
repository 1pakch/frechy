"""Database operations for Frechy."""

import sqlite3
from datetime import datetime

from models import Exercise, SessionStats


class Database:
    """SQLite database for session persistence."""

    def __init__(self, db_path: str = "frechy.db"):
        """Initialize database connection and create schema if needed."""
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_schema()

    def create_schema(self):
        """Create tables if they don't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL DEFAULT 'ilya',
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                topic TEXT NOT NULL,
                mode TEXT NOT NULL CHECK(mode IN ('translation', 'word-order')),
                end_time TIMESTAMP,
                total_exercises INTEGER DEFAULT 0,
                correct_first_try INTEGER DEFAULT 0
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                english_text TEXT NOT NULL,
                correct_french TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise_id INTEGER NOT NULL,
                attempt_number INTEGER NOT NULL,
                user_answer TEXT NOT NULL,
                is_correct BOOLEAN NOT NULL,
                hints_used INTEGER DEFAULT 0,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (exercise_id) REFERENCES exercises(id)
            )
        """)

        self.conn.commit()

    def create_session(self, user_name: str, topic: str, mode: str) -> int:
        """Create session, return session_id."""
        cursor = self.conn.execute(
            "INSERT INTO sessions (user_name, topic, mode) VALUES (?, ?, ?)",
            (user_name, topic, mode)
        )
        self.conn.commit()
        return cursor.lastrowid

    def create_exercise(self, exercise: Exercise) -> int:
        """Create exercise, return exercise_id."""
        cursor = self.conn.execute(
            """INSERT INTO exercises
               (session_id, topic, english_text, correct_french)
               VALUES (?, ?, ?, ?)""",
            (exercise.session_id, exercise.topic,
             exercise.english_text, exercise.correct_french)
        )
        self.conn.commit()
        exercise.id = cursor.lastrowid
        return exercise.id

    def create_attempt(self, exercise_id: int, attempt_number: int,
                      user_answer: str, is_correct: bool, hints_used: int) -> int:
        """Create attempt, return attempt_id."""
        cursor = self.conn.execute(
            """INSERT INTO attempts
               (exercise_id, attempt_number, user_answer, is_correct, hints_used)
               VALUES (?, ?, ?, ?, ?)""",
            (exercise_id, attempt_number, user_answer, is_correct, hints_used)
        )
        self.conn.commit()
        return cursor.lastrowid

    def end_session(self, session_id: int, stats: SessionStats):
        """Update session with end_time and stats."""
        self.conn.execute(
            """UPDATE sessions
               SET end_time = CURRENT_TIMESTAMP,
                   total_exercises = ?,
                   correct_first_try = ?
               WHERE id = ?""",
            (stats.total_exercises, stats.correct_first_try, session_id)
        )
        self.conn.commit()

    def get_session_start_time(self, session_id: int) -> datetime:
        """Get session start time for duration calculation."""
        cursor = self.conn.execute(
            "SELECT start_time FROM sessions WHERE id = ?",
            (session_id,)
        )
        row = cursor.fetchone()
        if row:
            return datetime.fromisoformat(row['start_time'])
        return datetime.now()
