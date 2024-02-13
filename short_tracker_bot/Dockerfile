FROM python:3.9

WORKDIR /app

#COPY short_tracker_bot/requirements.txt .
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN chmod 755 .

COPY ./short_tracker_bot .

#WORKDIR /app/short_tracker_bot/
WORKDIR /app

CMD ["python3", "bot.py"]