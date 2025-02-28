import os
import logging
from datetime import datetime, timezone

BOT_NAME = "crypto"
SPIDER_MODULES = ["crypto.spiders"]
NEWSPIDER_MODULE = "crypto.spiders"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/109.0.0.0 Safari/537.36"
)

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 2
DOWNLOAD_DELAY = 2

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

ITEM_PIPELINES = {
    "crypto.pipelines.CryptoPipeline": 300,
}

KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_BROKER_URL = os.environ["KAFKA_BROKER_URL"]

SCRAPY_BUFFER_SIZE = int(os.environ["SCRAPY_BUFFER_SIZE"])

TIMESTAMP = datetime.now(timezone.utc).replace(second=0, microsecond=0).isoformat()

logging.basicConfig(level=logging.INFO)

# Time to wait between each spider loop
SCRAPY_SLEEP_TIME = 10