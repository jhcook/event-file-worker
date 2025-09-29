# ---------- Stage 1: Build ----------
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy source code and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

# ---------- Stage 2: Runtime ----------
FROM python:3.12-slim

# Create non-root user and group
RUN groupadd -r worker && useradd -r -g worker worker

# Set working directory
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy source code
COPY . .

# Set ownership and permissions
RUN chown -R worker:worker /app

# Switch to non-root user
USER worker

# Expose health check endpoint (if using HTTP server)
EXPOSE 8080

# Define health check (can be adapted to actual /healthz endpoint)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/healthz || exit 1

# Default command to run the worker
CMD ["python", "main.py"]
