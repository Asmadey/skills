FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed for Playwright, networking, and Git (for pip dependencies from GitHub)
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY agent_system/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy configuration and source code
COPY agent_system/pyproject.toml .
COPY agent_system/src/ ./src/

# Install the package itself
RUN pip install --no-cache-dir .

# Install Playwright browsers
RUN python -m playwright install --with-deps chromium

EXPOSE 8000

# Using direct module path as 'src' is now in the working directory
CMD ["uvicorn", "src.api.app:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]