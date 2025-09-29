# Event Schema Design
This is the JSON payload that triggers the worker. It should be compact, versioned, and support idempotency and traceability.

## Required Fields
```json
{
  "schemaVersion": "1.0",
  "eventId": "abc123-def456",         // UUID for idempotency
  "correlationId": "xyz789",          // For tracing across systems
  "timestamp": "2025-09-29T00:00:00Z",
  "source": {
    "provider": "aws",
    "bucket": "source-bucket",
    "key": "path/to/file.txt"
  },
  "destination": {
    "provider": "gcp",
    "bucket": "target-bucket",
    "key": "path/to/file.txt"
  }
}
```

## Compatibility & Failure Rules
Versioning: schemaVersion must be non-breaking unless explicitly deprecated.

Retries: Use exponential backoff with jitter; max 5 attempts.

DLQ: Failed events after retries go to a Dead Letter Queue (local stub).

Idempotency: eventId ensures no duplicate transfers.

Deprecation: Add "deprecated": true in future versions with fallback logic.

## Identity & Auth Posture
No long-lived keys: Prefer short-lived credentials via STS or WIF.

Least privilege: Source/destination access scoped to specific buckets.

Secrets: Injected via env vars or local stubbed secrets manager.

## Run Profile
Logging: Structured JSON logs with eventId, correlationId, and severity.

Metrics: Emit counters for success, failure, retries, DLQ.

Health: /healthz endpoint returns 200 OK if worker is ready.

Traceability: Include correlationId in all logs and metrics.

## Example SLOs
SLO	Target
Successful transfer latency	< 2 seconds

Event processing reliability ≥ 99.9%
