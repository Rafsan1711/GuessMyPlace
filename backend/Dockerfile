# Multi-stage Dockerfile for GuessMyPlace Backend
# Stage 1: Build C++ modules
FROM python:3.10-slim as cpp-builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    cmake \
    make \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Copy C++ source files
COPY algorithms/cpp /build/algorithms/cpp

# Build C++ modules
WORKDIR /build/algorithms/cpp
RUN mkdir -p build && cd build && \
    cmake .. && \
    make && \
    ls -la

# Stage 2: Final runtime image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libstdc++6 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy C++ compiled libraries from builder
COPY --from=cpp-builder /build/algorithms/cpp/build /app/algorithms/cpp/build

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy data files
COPY --from=cpp-builder /build/algorithms/cpp/build/*.so /app/algorithms/cpp/build/ || true

# Create necessary directories
RUN mkdir -p logs data/places data/questions

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["python", "run.py"]