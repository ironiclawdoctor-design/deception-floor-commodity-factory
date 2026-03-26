# Dollar Agency Dashboard
# GMRC/DE-001 — devops-engineer
# Python 3.11-slim + Flask, port 8080

FROM python:3.11-slim

# Metadata
LABEL org.opencontainers.image.title="Dollar Agency Dashboard" \
      org.opencontainers.image.description="Shannon Economy — The Economy of Accountability" \
      org.opencontainers.image.version="1.0.0"

# Set working directory
WORKDIR /app

# Install Flask (minimal, no cache)
RUN pip install --no-cache-dir flask==3.0.3

# Copy application files
COPY dashboard.html .
COPY dashboard_server.py .

# Optional: copy dollar.db if present (baked-in snapshot)
# dollar.db is expected at /app/dollar.db inside the container
# For GCP Cloud Run: mount via volume or copy at build time
COPY dollar.db .

# Expose port
EXPOSE 8080

# Environment
ENV PORT=8080 \
    PYTHONUNBUFFERED=1

# Run
CMD ["python", "dashboard_server.py"]
