FROM python:3.9-slim

ENV STREAMLIT_TELEMETRY=0

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.headless=true"]
