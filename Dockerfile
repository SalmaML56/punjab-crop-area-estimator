# Use Python base image
FROM python:3.9-slim

# Disable telemetry using environment variable
ENV STREAMLIT_TELEMETRY=False

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Run the app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860"]
