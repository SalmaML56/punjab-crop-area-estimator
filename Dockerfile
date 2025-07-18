FROM python:3.9-slim

# Create non-root user
RUN useradd -m -u 1000 user

# Switch to non-root user
USER user

# Set environment path
ENV PATH="/home/user/.local/bin:$PATH"

# Create safe .streamlit folder
WORKDIR /app
RUN mkdir -p /app/.streamlit

# Set telemetry folder
ENV STREAMLIT_HOME=/app/.streamlit
ENV STREAMLIT_TELEMETRY=0

# Copy files
COPY --chown=user . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.headless=true"]