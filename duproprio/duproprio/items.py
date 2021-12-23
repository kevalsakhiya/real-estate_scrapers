# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DuproprioItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    COLLECTED_DATE = scrapy.Field()
    ADDRESS = scrapy.Field()
    PRICE_LISTED = scrapy.Field()
    DUPROPRIO_NUMBER = scrapy.Field()
    NBL = scrapy.Field()
    LOT_AREA = scrapy.Field()
    YEAR_BUILT = scrapy.Field()
    FEATURES = scrapy.Field()
    TAXES = scrapy.Field()
    ASSESSMENT = scrapy.Field()
    REVENUE = scrapy.Field()
    EXPENSES = scrapy.Field()
    UNIT_SIZE = scrapy.Field()
    LOCATION = scrapy.Field()
    DUPROPRIO_AVAILABLE = scrapy.Field()
    pass

