FROM python:3.13.11-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8765" ]

