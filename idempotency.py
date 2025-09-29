"""Idempotency tracking using SQLite.

This module ensures that each event is processed only once by storing
processed event IDs in a local SQLite database.
"""

import sqlite3


def init_db(path="idempotency.db"):
    """Initialize the SQLite database and create the tracking table.

    Args:
        path (str): Path to the SQLite database file.

    Returns:
        sqlite3.Connection: Active database connection.
    """
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE IF NOT EXISTS processed_events (eventId TEXT PRIMARY KEY)")
    conn.commit()
    return conn


def is_processed(conn, event_id):
    """Check if an event has already been processed.

    Args:
        conn (sqlite3.Connection): Active database connection.
        event_id (str): Unique event identifier.

    Returns:
        bool: True if event is already processed, False otherwise.
    """
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM processed_events WHERE eventId = ?", (event_id,))
    return cur.fetchone() is not None


def mark_processed(conn, event_id):
    """Mark an event as processed by storing its ID.

    Args:
        conn (sqlite3.Connection): Active database connection.
        event_id (str): Unique event identifier.
    """
    conn.execute("INSERT INTO processed_events (eventId) VALUES (?)", (event_id,))
    conn.commit()
