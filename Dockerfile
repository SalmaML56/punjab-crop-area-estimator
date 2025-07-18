FROM python:3.9-slim

# Create .streamlit folder at root level to prevent telemetry crash
RUN mkdir -p /.streamlit && chmod -R 777 /.streamlit

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.headless=true"]
