FROM python:3.8.19-slim
COPY requirements.txt /requirements.txt
RUN apt-get update
RUN apt-get install build-essential -y
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt