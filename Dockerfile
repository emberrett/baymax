FROM python:3.8.19-slim


WORKDIR "/baymax"
COPY requirements.txt requirements.txt
COPY main.py main.py
COPY utils.py utils.py
COPY prompt.txt prompt.txt
COPY

RUN apt-get update
RUN apt-get install build-essential -y
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt