# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KijijiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    COLLECTED_DATE = scrapy.Field()
    WEB_LINK = scrapy.Field()
    ADDRESS = scrapy.Field()
    LOCATION = scrapy.Field()
    PRICE = scrapy.Field()
    TYPE = scrapy.Field()
    BEDROOM_NB = scrapy.Field()
    BATHROOM_NB = scrapy.Field()
    UTILITIES = scrapy.Field()
    TELECOM = scrapy.Field()
    PARKING = scrapy.Field()
    AGREEMENT_TYPE = scrapy.Field()
    MOVING_DATE = scrapy.Field()
    PET_FRIENDLY = scrapy.Field()
    UNIT_SIZE = scrapy.Field()
    FURNISHED = scrapy.Field()
    APPLIANCE = scrapy.Field()
    AIR_CONDITIONING = scrapy.Field()
    PERSONAL_OUTDOOR_SPACE = scrapy.Field()
    SMOKING_PERMITTED = scrapy.Field()
    BUILDING_AMENITIES = scrapy.Field()

    pass
