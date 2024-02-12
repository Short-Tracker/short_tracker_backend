FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN chmod 755 .

COPY ./short_tracker_bot .

# RUN python3 short_tracker_bot/bot.py
WORKDIR /app

CMD ["python3", "bot.py"]