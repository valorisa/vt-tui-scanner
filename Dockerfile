FROM python:3.11-slim as base

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY pyproject.toml .

# Set environment
ENV PYTHONPATH=/app
ENV VT_API_KEY=""

# Default command
CMD ["python", "-m", "src.main"]

# Development stage
FROM base as dev

RUN pip install --no-cache-dir pytest pytest-mock pytest-cov flake8

CMD ["pytest", "tests/"]

# Production stage
FROM base as production

USER nobody

CMD ["python", "-m", "src.main", "--headless"]
