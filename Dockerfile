FROM python:3.9-slim

# Create root-level .streamlit folder with full write access
RUN mkdir -p /root/.streamlit && chmod -R 777 /root/.streamlit

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.headless=true"]
