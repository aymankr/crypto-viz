import os, re, json, requests, logging, socket
from datetime import datetime, timezone

from quixstreams import Application
from pyspark.sql import SparkSession

KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
FLASK_API_URL = os.environ["FLASK_API_URL"]
KAFKA_BROKER_URL = os.environ["KAFKA_BROKER_URL"]

app = Application(
    broker_address=KAFKA_BROKER_URL, loglevel="DEBUG", consumer_group=KAFKA_TOPIC
)

spark = (
    SparkSession.builder.appName("CryptoDataGenerator")
    .config("spark.driver.extraJavaOptions", "-Divy.home=/tmp/.ivy2")
    .getOrCreate()
)

SESSION_START = datetime.now(timezone.utc)

context = spark.sparkContext

# Set up logging
logging.basicConfig(level=logging.INFO)


def get_worker_id():
    """
    Returns the id of the Spark worker (docker hostname)
    """
    return socket.gethostname()


def send_log_to_api(
    *, issuer: str, message: str, level: str, worker_id: str | None = None
):
    """
    Send logs to the Flask API
    """
    try:
        requests.post(
            f"{FLASK_API_URL}/logs",
            json={
                "issuer": issuer,
                "message": message,
                "level": level,
                "issued_at": datetime.now(timezone.utc).isoformat(),
                "session_start": SESSION_START.isoformat(),
                "worker_id": worker_id,
            },
        )
    except requests.RequestException as e:
        logging.error(f"Error sending logs to API: {e}")

def clean_numeric(value):
    """Cleans and converts a string value to a numeric value."""
    if not value:
        return None

    if isinstance(value, list):
        value = value[0]

    value = str(value).replace('$', '').replace(',', '').strip()
    
    if value.endswith(('T', 'B', 'M')):
        value = value[:-1]

    value = re.sub(r'[^\d\.]+', '', value)

    try:
        return float(value)
    except ValueError:
        return None

def adjust_percentage(value, icon_class):
    """Adjusts a numeric value based on the presence of a specific icon class."""
    if icon_class and "Caret-down" in icon_class:
        return -abs(value) if value is not None else None
    return value

# Function to send data to Flask API
def process_and_send_to_api(item, hostname):
    try:
        if "scraped_at" not in item:
            item["scraped_at"] = datetime.utcnow().isoformat()

        # ISO-8601
        item["price"] = clean_numeric(item.get("price"))
        item["market_cap"] = clean_numeric(item.get("market_cap"))
        item["volume_24h"] = clean_numeric(item.get("volume_24h"))
        item["circulating_supply"] = clean_numeric(item.get("circulating_supply"))

        ch1 = clean_numeric(item.get("change_1h"))
        item["change_1h"] = adjust_percentage(ch1, item.get("icon_1h"))

        ch24 = clean_numeric(item.get("change_24h"))
        item["change_24h"] = adjust_percentage(ch24, item.get("icon_24h"))

        ch7 = clean_numeric(item.get("change_7d"))
        item["change_7d"] = adjust_percentage(ch7, item.get("icon_7d"))

        # we don't need to send this:
        if "icon_1h" in item:
            del item["icon_1h"]
        if "icon_24h" in item:
            del item["icon_24h"]
        if "icon_7d" in item:
            del item["icon_7d"]

        response = requests.post(f"{FLASK_API_URL}/crypto-items", json=item)
        response.raise_for_status()

    except requests.RequestException as e:
        send_log_to_api(
            issuer="SPARK_WORKER",
            message=str(e),
            level="ERROR",
            worker_id=hostname,
        )
        logging.error(f"Error sending crypto item to API: {e}")


with app.get_consumer() as consumer:
    consumer.subscribe([KAFKA_TOPIC])

    while True:
        message = consumer.poll(timeout=1)

        if message is None:
            continue

        elif message.error() is not None:
            # Send logs to the API in case of an error
            send_log_to_api(
                message=f"{message.error()}",
                issuer="SPARK_MASTER",
                level="ERROR",
                worker_id=get_worker_id(),
            )
            continue

        else:
            key = message.key().decode("utf8")
            value = json.loads(message.value())

            # Parallelize the data
            rdd = context.parallelize(value)

            # Send data to the API using foreach
            rdd.foreach(lambda item: process_and_send_to_api(item, get_worker_id()))
