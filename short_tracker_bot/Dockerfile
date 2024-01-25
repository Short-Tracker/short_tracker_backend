FROM python:3.9

WORKDIR /app

COPY short_tracker_bot/requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY ./short_tracker_bot .

RUN python3 short_tracker_bot/bot.py
