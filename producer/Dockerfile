FROM python:3.8

WORKDIR /app

EXPOSE 5000

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "producer.py"]