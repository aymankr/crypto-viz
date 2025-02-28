import time
import scrapy
import re
from datetime import datetime
from .. import settings

class CryptoSpider(scrapy.Spider):
    name = "crypto"
    start_urls = ["https://coinmarketcap.com"]

    def parse(self, response):
        rows = response.css("tbody tr")
        seen_ranks = set()  # To track already seen ranks
        count = 0

        for row in rows:
            rank_str = row.css("td:nth-child(2) p::text").get()
            if not rank_str:
                continue
            try:
                rank = int(rank_str.strip())
            except ValueError:
                continue

            if rank > 10:  # Stop after top 10
                break

            if rank in seen_ranks:  # Skip duplicates
                continue

            seen_ranks.add(rank)

            name = row.css("p.coin-item-name::text").get()
            symbol = row.css("p.coin-item-symbol::text").get()
            price = row.css("td:nth-child(4) div span::text").get()

            icon_1h = row.css("td:nth-child(5) span.icon-Caret-up, td:nth-child(5) span.icon-Caret-down::attr(class)").get()
            change_1h = row.css("td:nth-child(5) span::text").get()
            change_1h = change_1h, icon_1h

            icon_24h = row.css("td:nth-child(6) span.icon-Caret-up, td:nth-child(6) span.icon-Caret-down::attr(class)").get()
            change_24h = row.css("td:nth-child(6) span::text").get()
            change_24h = change_24h, icon_24h

            icon_7d = row.css("td:nth-child(7) span.icon-Caret-up, td:nth-child(7) span.icon-Caret-down::attr(class)").get()
            change_7d = row.css("td:nth-child(7) span::text").get()
            change_7d = change_7d, icon_7d

            market_cap = row.css("td:nth-child(8) span[data-nosnippet]::text").get()
            volume_24h = row.css("td:nth-child(9) p.font_weight_500::text").get()
            supply = row.css("td:nth-child(10) p.sc-71024e3e-0.hhmVNu::text").get()
            logo_url = row.css("td:nth-child(3) img.coin-logo::attr(src)").get()

            yield {
                "rank": rank,
                "name": name.strip() if name else None,
                "symbol": symbol.strip() if symbol else None,
                "price": price,
                "change_1h": change_1h,
                "change_24h": change_24h,
                "change_7d": change_7d,
                "market_cap": market_cap,
                "volume_24h": volume_24h,
                "circulating_supply": supply,
                "logo_url": logo_url.strip() if logo_url else None,
                "timestamp": settings.TIMESTAMP,
            }

            count += 1

        self.logger.info(f"Scraped top {count} cryptos.")

        # Wait and rescrape the URL
        time.sleep(settings.SCRAPY_SLEEP_TIME)
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            dont_filter=True  # Allow refetching the same URL
        )
