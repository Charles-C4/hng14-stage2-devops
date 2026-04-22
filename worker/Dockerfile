# Stage 1: Build
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Stage 2: Production
FROM python:3.11-slim AS runner

# Install procps for pgrep (essential for worker healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends procps && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy ONLY worker code and requirements
COPY worker.py ./
COPY requirements.txt ./

# Safety: Explicitly remove any .env file
RUN rm -f .env

# Set ownership
RUN chown -R appuser:appgroup /app

# Change to non-root user
USER appuser

# Healthcheck - using pgrep to ensure the process is alive
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD pgrep -f "python worker.py" || exit 1

# Run the worker
CMD ["python", "worker.py"]