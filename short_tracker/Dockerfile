FROM python:3.10-slim

WORKDIR /app

COPY short_tracker/requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY ./short_tracker .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]