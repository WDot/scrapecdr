# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapecdrItem(scrapy.Item):
    state = scrapy.Field()
    disease = scrapy.Field()
