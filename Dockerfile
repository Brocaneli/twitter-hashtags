FROM python:3.8

WORKDIR /app

COPY requirements.txt /app

RUN apt update && \
    apt install gunicorn -y

RUN pip install -r requirements.txt

COPY app/ /app

RUN mkdir data

CMD sleep 30 && python get_info.py && gunicorn --bind 0.0.0.0:5000 --log-config gunicorn.conf app:app