FROM python:3.8

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY app/ /app

CMD sleep 20 && python get_info.py && python app.py