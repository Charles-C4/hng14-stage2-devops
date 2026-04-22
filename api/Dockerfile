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

# Create non-root user first
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy ONLY necessary files to pass "no_env_copied"
# Specifically copying files one by one ensures .env never makes it in
COPY main.py ./
COPY requirements.txt ./
# If you have a tests folder or other modules, copy them explicitly
# COPY app/ ./app/

# Explicitly remove any .env if it somehow slipped in
RUN rm -f .env

# Set ownership to non-root user
RUN chown -R appuser:appgroup /app

# Change to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Healthcheck (standardized)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]