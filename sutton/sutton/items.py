# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SuttonItem(scrapy.Item):
    COLLECTED_DATE = scrapy.Field()
    WEB_LINK = scrapy.Field()
    AVAILABLE = scrapy.Field()
    ADDRESS = scrapy.Field()
    PRICE_LISTED = scrapy.Field()
    MLS_NUMBER = scrapy.Field()
    FEATURES = scrapy.Field()
    LOT_AREA = scrapy.Field()
    YEAR_BUILT = scrapy.Field()
    ASSESSMENT = scrapy.Field()
    REVENUE = scrapy.Field()
    EXPENSES = scrapy.Field()
    TAXES = scrapy.Field()
    pass
