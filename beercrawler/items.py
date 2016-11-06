# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class BeercrawlerItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     url = scrapy.Field()
#     html = scrapy.Field()
#     pass

class Beer(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    brewery = scrapy.Field()
    style = scrapy.Field()
    rating = scrapy.Field()
    abv = scrapy.Field()
    state = scrapy.Field()
    country = scrapy.Field()