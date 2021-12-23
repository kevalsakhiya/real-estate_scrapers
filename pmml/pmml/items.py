# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PmmlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    PMML_URL = scrapy.Field()
    COLLECTED_DATE = scrapy.Field()
    ADDRESS = scrapy.Field()
    PRICE = scrapy.Field()
    NBL = scrapy.Field()
    CADASTRAL_NUMBER = scrapy.Field()
    LOT_AREA = scrapy.Field()
    YEAR_BUILT = scrapy.Field()
    CONSTRUCTION_TYPE = scrapy.Field()
    FEATURES = scrapy.Field()
    ASSESSMENT = scrapy.Field()
    TAXES = scrapy.Field()
    REVENU = scrapy.Field()
    EXPENSES = scrapy.Field()
    KPI = scrapy.Field()
    LOCATION = scrapy.Field()
    UNIT_SIZE = scrapy.Field()
    PMML_AVAILABLE = scrapy.Field()
    pass
