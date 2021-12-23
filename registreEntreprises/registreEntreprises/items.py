# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RegistreentreprisesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    NEQ = scrapy.Field()
    ACTIONNAIRES = scrapy.Field()
    ADMINISTRATEURS = scrapy.Field()
    COLLECTED_DATE = scrapy.Field()
    pass
