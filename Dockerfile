FROM python:3.9-slim

# Create non-root user
RUN useradd -m -u 1000 user

# Set working directory
WORKDIR /app

# Create safe .streamlit folder and set ownership
RUN mkdir -p /app/.streamlit && chown -R user:user /app/.streamlit

# Switch to non-root user
USER user

# Set environment variables
ENV STREAMLIT_HOME=/app/.streamlit
ENV STREAMLIT_TELEMETRY=0
ENV PATH="/home/user/.local/bin:$PATH"

# Copy files with correct ownership
COPY --chown=user . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.headless=true"]
