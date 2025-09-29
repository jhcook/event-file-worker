# Event-Driven Transfer Worker

A secure, testable Python worker that simulates cross-cloud file transfers triggered by events. Designed for DevSecOps validation with containerization, CI, and security scanning—no real cloud accounts required.

## Project Overview

This worker includes:

- Local queue and storage stubs
- Idempotency tracking via SQLite
- Retries with exponential backoff + jitter
- Dead Letter Queue (DLQ) routing
- Containerization with multi-stage build and health check
- CI pipeline with Trivy security scan

## 📦 Example Event

```json
{
  "schemaVersion": "1.0",
  "eventId": "abc123-def456",
  "correlationId": "xyz789",
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

## SLOs

SLO

Target

Successful transfer latency

< 2 seconds

Event processing reliability

≥ 99.9%

## How to Run Locally

```
# Build and run the container
docker build -t worker .
docker run --rm worker
```

## How to Run Tests

```
# Run unit tests
python -m unittest discover -s tests
```

## How to Run CI Locally (Optional)

```
# Install Trivy
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh

# Run filesystem scan
./trivy fs . --severity HIGH,CRITICAL --exit-code 1

# Build and scan Docker image
docker build -t worker .
./trivy image worker --severity HIGH,CRITICAL --exit-code 1
```

## GitHub Actions CI

The CI pipeline runs on every push and pull request to main. It includes:

Dependency install

Unit tests

Linting (flake8)

Trivy filesystem and image scan

Optional SBOM generation

## Identity & Security Posture

No long-lived credentials

Prefer STS/WIF for ephemeral access

Secrets injected via env vars or stubbed secrets manager

Least privilege enforced in stubbed access logic

## Assumptions & Unknowns

No real cloud accounts used

File transfer is simulated

DLQ is a local JSON file

Health check is stubbed (can be extended)

## ADR Summary

Key trade-offs:

Simulated queue/storage avoids cloud cost and lock-in

SQLite for idempotency is portable and testable

Trivy chosen for broad security coverage (code + container)

Multi-stage Dockerfile ensures clean, non-root runtime

CI pipeline is GitHub-native and reproducible locally
