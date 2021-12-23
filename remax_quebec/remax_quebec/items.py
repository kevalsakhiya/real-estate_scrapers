# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RemaxQuebecItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    COLLECTED_DATE = scrapy.Field()
    NBL = scrapy.Field()
    ADDRESS = scrapy.Field()
    PRICE_LISTED = scrapy.Field()
    MLS_NUMBER = scrapy.Field()
    YEAR_BUILT = scrapy.Field()
    REMAX_QUEBEC_LINK = scrapy.Field()
    BUILDING_SIZE = scrapy.Field()
    FEATURES = scrapy.Field()
    ASSESSMENT = scrapy.Field()
    TAXES = scrapy.Field()
    EXPENSES = scrapy.Field()
    REVENU = scrapy.Field()
    LOT_AREA = scrapy.Field()
    REMAX_AVAILABLE = scrapy.Field()
    pass
