FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (if bcrypt / cryptography need build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list and install
COPY requirement.txt /app/requirement.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirement.txt

# Copy application code
COPY . /app

# Environment
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

