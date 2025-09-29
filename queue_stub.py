"""Simulated event queue loader and iterator.

This module provides functions to load events from a local JSON file
and retrieve them one by one, mimicking a message queue.
"""

import json


def load_events(path="events.json"):
    """Load events from a JSON file.

    Args:
        path (str): Path to the JSON file containing event list.

    Returns:
        list: List of event dictionaries.
    """
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {path} not found. Using empty queue.")
        return []


def get_next_event(queue):
    """Retrieve the next event from the queue.

    Args:
        queue (list): List of event dictionaries.

    Returns:
        dict or None: The next event, or None if queue is empty.
    """
    return queue.pop(0) if queue else None
