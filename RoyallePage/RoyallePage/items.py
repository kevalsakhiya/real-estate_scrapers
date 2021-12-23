
import scrapy


class RoyallepageItem(scrapy.Item):
    COLLECTED_DATE =  scrapy.Field()
    WEB_LINK =  scrapy.Field()
    AVAILABLE =  scrapy.Field()
    ADDRESS =  scrapy.Field()
    LOCATION =  scrapy.Field()
    PRICE_LISTED =  scrapy.Field()
    MLS_NUMBER =  scrapy.Field()
    FEATURES =  scrapy.Field()
    LOT_AREA =  scrapy.Field()
    YEAR_BUILT =  scrapy.Field()
    ASSESSMENT =  scrapy.Field()
    REVENUE =  scrapy.Field()
    EXPENSES =  scrapy.Field()
    TAXES = scrapy.Field()