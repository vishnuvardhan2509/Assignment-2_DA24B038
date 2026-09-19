# Dockerfile
# Multi-stage build for Question 1.
# Stage 1 (builder) installs dependencies into a temp prefix.
# Stage 2 (runtime) copies only the installed packages, not build tools.

# ---------- Stage 1: builder ----------
FROM python:3.11-slim AS builder

WORKDIR /build

# Install only what's needed to build wheels (gcc, etc.).
# This stays in the builder stage and is NOT copied to runtime.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies into an isolated prefix so we can copy them wholesale.
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.11-slim

WORKDIR /app

# Copy ONLY the installed Python packages from the builder.
# Build tools, caches, and the pip wheel build directory stay behind.
COPY --from=builder /install /usr/local

# Copy only the app files we actually need at runtime.
COPY main.py .
COPY model.joblib .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]