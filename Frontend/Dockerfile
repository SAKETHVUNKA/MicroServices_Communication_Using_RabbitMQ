FROM python:3.8

WORKDIR /app

EXPOSE 8000

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "app.py"]