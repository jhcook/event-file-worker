"""Exponential backoff with jitter for retry logic.

This module provides a delay mechanism to space out retries
in case of transient failures.
"""

import time
import random


def exponential_backoff(attempt, base=0.5, cap=5.0):
    """Sleep for a randomized delay based on exponential backoff.

    Args:
        attempt (int): Current retry attempt (0-indexed).
        base (float): Base delay in seconds.
        cap (float): Maximum delay cap in seconds.
    """
    delay = min(cap, base * (2 ** attempt))
    jitter = random.uniform(0, delay)
    time.sleep(jitter)
