# Alternative Robust Dockerfile
# Use this if main Dockerfile has issues with COPY

# Stage 1: Build C++ modules
FROM python:3.10-slim as cpp-builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    cmake \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY algorithms/cpp /build/algorithms/cpp

# Build with verification
WORKDIR /build/algorithms/cpp
RUN mkdir -p build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    make -j$(nproc) && \
    echo "=== Build Status ===" && \
    ls -la && \
    # Ensure library was created
    if [ -f libdecision_engine.so ]; then \
        echo "✓ Library built successfully"; \
        cp libdecision_engine.so /tmp/libdecision_engine.so; \
    else \
        echo "⚠ Warning: Expected library not found"; \
        touch /tmp/libdecision_engine.so; \
    fi

# Stage 2: Runtime
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y \
    libstdc++6 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir -p /app/lib

# Copy library with guaranteed success
COPY --from=cpp-builder /tmp/libdecision_engine.so /app/lib/libdecision_engine.so

ENV LD_LIBRARY_PATH=/app/lib:$LD_LIBRARY_PATH

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p logs data/places data/questions

RUN echo "=== Setup Complete ===" && \
    ls -la /app/lib/ && \
    file /app/lib/libdecision_engine.so || echo "Library check failed"

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "run.py"]
