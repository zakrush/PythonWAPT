# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BasicCrawler2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    comment = scrapy.Field()
    location_url=scrapy.Field()
    form = scrapy.Field()
    email = scrapy.Field()
    link_url = scrapy.Field()
    pass
