FROM python:3.9-slim

RUN mkdir -p /app/.streamlit

ENV STREAMLIT_TELEMETRY=0
ENV STREAMLIT_HOME=/app/.streamlit

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.headless=true"] 
