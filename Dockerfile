# Use Python 3.11.9
FROM python:3.11.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional: ffmpeg for gradio/audio support)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port (Render expects 10000 or $PORT)
EXPOSE 10000

# Run your app (adjust if you use streamlit, gradio, or fastapi)
# Example for streamlit:
# CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]

# Example for FastAPI/Uvicorn:
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
