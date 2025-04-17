FROM python:3.10-alpine

WORKDIR /home/datapolicy

COPY . .

RUN pip install --no-cache-dir -r requirements.txt