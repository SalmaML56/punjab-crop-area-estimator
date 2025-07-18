FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Create safe telemetry folder inside /tmp
RUN mkdir -p /tmp/.streamlit

# Set environment variables to redirect telemetry
ENV STREAMLIT_HOME=/tmp/.streamlit
ENV STREAMLIT_TELEMETRY=0

# Copy files
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.headless=true"]
