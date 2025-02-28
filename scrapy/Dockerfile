FROM python:3.10-slim

WORKDIR /runtime/app

RUN pip install --no-cache-dir scrapy


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /runtime/app

ENTRYPOINT ["sh", "entrypoint.sh"]
