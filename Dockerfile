FROM python:3.8.19-slim


WORKDIR "/baymax"
COPY requirements.txt requirements.txt
COPY main.py main.py
COPY baymax.py baymax.py
COPY model_config.json model_config.json

ADD models /baymax/models/

RUN apt-get update
RUN apt-get install build-essential -y
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt