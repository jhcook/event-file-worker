"""Main worker loop for processing cross-cloud file transfer events.

This script simulates an event-driven architecture using local stubs for:
- Queue ingestion
- File transfer
- Idempotency tracking
- Retry with exponential backoff
- Dead Letter Queue (DLQ) routing

It is designed for local testing and DevSecOps validation without real cloud accounts.
"""

from queue_stub import load_events, get_next_event
from storage_stub import copy_file
from idempotency import init_db, is_processed, mark_processed
from backoff import exponential_backoff
from dlq import send_to_dlq

# Maximum number of retry attempts before routing to DLQ
MAX_RETRIES = 5


def process_event(event):
    """Attempt to process a single event by copying a file.

    Retries the operation with exponential backoff and jitter.
    Returns True if successful, False if all retries fail.

    Args:
        event (dict): The event payload containing source and destination info.

    Returns:
        bool: True if the file was copied successfully, False otherwise.
    """
    for attempt in range(MAX_RETRIES):
        try:
            # Simulate the file copy operation
            copy_file(event["source"], event["destination"])
            return True
        except Exception:
            # Wait before retrying using exponential backoff
            exponential_backoff(attempt)
    return False


def run_worker():
    """Main loop for processing events from the simulated queue.

    - Loads events from a local JSON file
    - Checks idempotency to avoid duplicate processing
    - Processes each event with retry logic
    - Routes failed events to a local DLQ stub
    """
    # Load the event queue from disk
    queue = load_events()

    # Initialize SQLite database for idempotency tracking
    conn = init_db()

    # Process events one by one
    while event := get_next_event(queue):
        eid = event["eventId"]

        # Skip event if already processed
        if is_processed(conn, eid):
            print(f"Skipping duplicate event {eid}")
            continue

        # Attempt to process the event
        success = process_event(event)

        if success:
            # Mark event as processed to ensure idempotency
            mark_processed(conn, eid)
        else:
            # Route failed event to DLQ
            send_to_dlq(event)
            print(f"Event {eid} sent to DLQ")


# Entry point for standalone execution
if __name__ == "__main__":
    run_worker()
