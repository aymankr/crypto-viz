FROM bitnami/spark:latest

WORKDIR /opt/bitnami/spark

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY submit.sh ./

COPY data/ apps/ ./
