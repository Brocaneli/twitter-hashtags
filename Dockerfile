FROM python:3.8

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY get_info.py /app

CMD python get_info.py && sleep 3000