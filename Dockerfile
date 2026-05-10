# Use lightweight Python 3.12 image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for ReportLab and potentially Presidio/PyMuPDF)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast package manager)
RUN pip install uv

# Copy requirements and install
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_lg

# Copy application code
COPY . .

# Create data directories so the app doesn't fail on mount
RUN mkdir -p data/jobs data/reports data/sample_jds data/sample_resumes

# Expose port 7860 (default for Hugging Face Spaces)
EXPOSE 7860

# Define environment variables
ENV PYTHONPATH=/app
ENV HOST=0.0.0.0
ENV PORT=7860

# Run the FastAPI server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
