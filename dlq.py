"""Dead Letter Queue (DLQ) stub for failed events.

This module appends failed events to a local JSON file for inspection.
"""

import json


def send_to_dlq(event, path="dlq.json"):
    """Append a failed event to the DLQ file.

    Args:
        event (dict): The event that failed processing.
        path (str): Path to the DLQ JSON file.
    """
    try:
        with open(path, "r") as f:
            dlq = json.load(f)
    except FileNotFoundError:
        dlq = []

    dlq.append(event)

    with open(path, "w") as f:
        json.dump(dlq, f, indent=2)
