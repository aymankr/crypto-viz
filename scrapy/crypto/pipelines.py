import json
from quixstreams import Application
import logging
from . import settings

logging.basicConfig(level=logging.INFO)

app = Application(
    broker_address=settings.KAFKA_BROKER_URL,
    loglevel="DEBUG"
)

class CryptoPipeline:
    def __init__(self):
        self.items = []

    def send_items_to_kafka(self, items):
        logging.info(items)
        with app.get_producer() as producer:
            producer.produce(
                topic=settings.KAFKA_TOPIC,
                key="crypto",
                value=json.dumps(items)
            )
        self.items.clear()

    def process_item(self, item, spider):
        if item is None:
            settings.logging.warning("Item is None")
            return

        self.items.append(item)
        if len(self.items) < settings.SCRAPY_BUFFER_SIZE:
            settings.logging.warning(
                f"Less than {settings.SCRAPY_BUFFER_SIZE} items in pipeline"
            )
            return

        self.send_items_to_kafka(self.items)
        return item

    def close_spider(self, spider):
        if len(self.items) > 0:
            self.send_items_to_kafka(self.items)
