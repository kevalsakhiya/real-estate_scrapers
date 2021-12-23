# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CentrisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ADDRESS = scrapy.Field()
    PRICE_LISTED = scrapy.Field()
    CENTRIS_NUMBER = scrapy.Field()
    USE_PROPERTY = scrapy.Field()
    USE_PROPERTY = scrapy.Field()
    YEAR_BUILT = scrapy.Field()
    PARKING = scrapy.Field()
    NBL = scrapy.Field()
    GROSS_REVENUE = scrapy.Field()
    CENTRIS_LINK = scrapy.Field()
    LOT_AREA = scrapy.Field()
    UNIT_SIZE = scrapy.Field()
    CENTRIS_LISTED = scrapy.Field()
    Location = scrapy.Field()
    file_urls = scrapy.Field()
    pass
