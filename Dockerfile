# syntax=docker/dockerfile:1.4
ARG PYTHON_VERSION=3.12
ARG ALPINE_VERSION=3.21
ARG PORT=8000

# Stage 1: Builder
FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} AS builder
WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    mysql-dev

# Copy and install dependencies
COPY pyproject.toml /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir .[mysql]

# Copy the rest of the application code
COPY . /app

# Stage 2: Runtime (Production)
FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} AS production
WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    mysql-dev

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN rm -rf /var/cache/apt/archives /var/lib/apt/lists/*
# Copy application code
COPY --from=builder /app /app

# Expose the port defined by the build argument
EXPOSE ${PORT}

# Set up execution permissions to entrypoint
RUN chmod +x /app/entrypoint.sh
# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Stage 3: Development
FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} AS development
WORKDIR /app

# Copy application code
COPY . /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    mysql-dev

# Install development dependencies (if any)
COPY pyproject.toml /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir .[dev,mysql]

# Expose the port defined by the build argument
EXPOSE ${PORT}

# Set up execution permissions to entrypoint
RUN chmod +x /app/entrypoint.sh
# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
