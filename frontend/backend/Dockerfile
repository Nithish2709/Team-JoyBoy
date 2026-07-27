# Production Dockerfile utilizing Python 3.12-slim
FROM python:3.12-slim AS builder

WORKDIR /workspace

# Install compiler libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Cache requirements installation
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Execution runner stage
FROM python:3.12-slim AS runner

WORKDIR /workspace

# Install diagnostic utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy cached site-packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/workspace

# Copy files
COPY . .

EXPOSE 8000

# Execute server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
