# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from datetime import datetime

@dataclass
class CryptoItem:
    name: str
    symbol: str
    timestamp: datetime
    price: str
    volume_24h: str
    change_1h: str
    change_24h: str
    change_7d: str
    market_cap: str
    circulating_supply: str
    rank: str
    logo_url: str
