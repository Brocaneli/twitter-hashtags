FROM python:3.8

WORKDIR /app

RUN apt update && \
    apt install gunicorn -y && \
    pip install --upgrade pip && \
    pip install setuptools

COPY app/ /app

RUN pip install -r requirements.txt

RUN mkdir data

CMD sleep 30 && python get_info.py && gunicorn --bind 0.0.0.0:5000 --log-config gunicorn.conf app:app
