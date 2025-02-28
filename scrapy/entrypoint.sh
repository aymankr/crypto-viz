#!/usr/bin/env bash

while true; do
    scrapy crawl crypto &

    sleep "${SCRAPY_SLEEP_TIME:-600}"
done
