"""Unit tests for the event-driven transfer worker.

Covers:
- Successful file copy
- Idempotency tracking
- DLQ routing for failed events
"""

import unittest
import os
import json
from storage_stub import copy_file
from idempotency import init_db, is_processed, mark_processed
from dlq import send_to_dlq


class TestWorker(unittest.TestCase):
    """Test suite for worker components."""

    def test_copy_success(self):
        """Test that a file copy simulation returns True."""
        source = {"key": "file.txt"}
        dest = {"key": "file.txt"}
        result = copy_file(source, dest)
        self.assertTrue(result)

    def test_idempotency_tracking(self):
        """Test that an event is correctly marked and detected as processed."""
        conn = init_db(":memory:")  # Use in-memory DB for isolation
        eid = "test-event-123"
        self.assertFalse(is_processed(conn, eid))  # Should not be processed yet
        mark_processed(conn, eid)
        self.assertTrue(is_processed(conn, eid))   # Should now be marked

    def test_dlq_trigger(self):
        """Test that a failed event is routed to the DLQ file."""
        test_path = "test_dlq.json"
        event = {"eventId": "fail123", "source": {}, "destination": {}}

        # Ensure clean test file
        if os.path.exists(test_path):
            os.remove(test_path)

        send_to_dlq(event, path=test_path)

        # Verify DLQ file