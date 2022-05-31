# scrapy crawl rpl

import scrapy
from scrapy import Request
import re
import json
from datetime import datetime
from scrapy.shell import inspect_response
from ..items import RoyallepageItem


class RoyalleSpider(scrapy.Spider):
    name = 'rpl'
    start_urls = [
        'https://www.royallepage.ca/en/qc/sherbrooke/investment/properties/',
        'https://www.royallepage.ca/en/qc/montreal/investment/properties/',
        'https://www.royallepage.ca/en/qc/laval/investment/properties/',
        'https://www.royallepage.ca/en/qc/quebec/investment/properties/',
        'https://www.royallepage.ca/en/qc/gatineau/investment/properties/',
        'https://www.royallepage.ca/en/qc/Longueuil/investment/properties/',
        'https://www.royallepage.ca/en/qc/blainville/investment/properties/',
        'https://www.royallepage.ca/en/qc/Saint-Eustache/investment/properties/',
        'https://www.royallepage.ca/en/qc/brossard/investment/properties/',
        'https://www.royallepage.ca/en/qc/granby/investment/properties/',
    ]

    def StrToNum(self, data):
        if data:
            if '.' in data:
                data = str(data)
                try:
                    f_data = re.search(r'([\d.,]+)', data)
                    f_data = f_data.group(1)
                    f_data = f_data.replace(',', '').replace(' ', '')
                    f_data = float(f_data)
                    f_data = round(f_data, 2)
                    return f_data
                except Exception as e:
                    print(e)
                    return data
            else:
                try:
                    i_data = re.search(r'([\d.,]+)', data)
                    i_data = i_data.group(1)
                    i_data = i_data.replace(' ', '').replace(',', '')
                    i_data = int(i_data)
                    return i_data
                except Exception as e:
                    print(e)
                    return data
        return 0

    def parse(self, response):
        url_list = response.xpath(
            './/*[@class="card__media"]/a/@href').getall()

        for url in url_list:
            url = response.urljoin(url)
            yield Request(url, callback=self.detail_page)

        next_page = response.xpath('.//a[contains(@class,"next")]/@href').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield Request(next_page,
                          callback=self.parse)

    def detail_page(self, response):
        item = RoyallepageItem()

        item['COLLECTED_DATE'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        item['WEB_LINK'] = response.url
        item['AVAILABLE'] = 1

        address = response.xpath('.//*[@class="address-bar"]/*/text()').get()
        item['ADDRESS'] = address

        latitude = re.search(r"placesLat='([\d.]+)", response.text)
        try:
            latitude = latitude.group(1)
        except Exception:
            latitude = None

        longitude = re.search(r"placesLng='([\d.\-]+)", response.text)
        try:
            longitude = longitude.group(1)

        except Exception:
            longitude = None

        location = {
            "type": "Point",
            'coordinates': [longitude, latitude]
        }
        item['LOCATION'] = location

        price = response.xpath(
            './/*[@class="property-price-wrapper"]/span/span/text()').getall()
        price = [x.strip() for x in price if x.strip()]
        price = ''.join(price)
        item['PRICE_LISTED'] = self.StrToNum(price)

        mls_number = re.search(r"MLS® # ([\d]+)", response.text).group(1)
        item['MLS_NUMBER'] = self.StrToNum(mls_number)

        features = {}

        feature_list = response.xpath(
            './/div[@class="details-row"][1]/ul[@class="property-features-list"]/li/span[1]/text()').getall()

        for key in feature_list:
            key = key.replace(':', '')
            features[f'{key}'] = response.xpath(
                f'.//*[contains(text(),"{key}")]/following-sibling::span/text()').get()

        item['FEATURES'] = features

        lot_area = response.xpath(
            './/*[contains(text(),"Lot Size:")]/following-sibling::span/text()').re_first(r'([\d.]+)')

        item['LOT_AREA'] = self.StrToNum(lot_area)

        year_built = response.xpath(
            './/*[contains(text(),"Built in:")]/following-sibling::span/text()').get()
        item['YEAR_BUILT'] = self.StrToNum(year_built)

        assessment = {}

        lot_assessment = response.xpath(
            './/*[contains(text(),"Lot Assessment:")]/following-sibling::span/text()').get()
        building_assessment = response.xpath(
            './/*[contains(text(),"Building Assessment:")]/following-sibling::span/text()').get()
        total_assesment = response.xpath(
            './/*[contains(text(),"Total Assessment:")]/following-sibling::span/text()').get()

        assessment['LOT_ASSESSMENT'] = self.StrToNum(lot_assessment)
        assessment['BUILDING_ASSESSMENT'] = self.StrToNum(building_assessment)
        assessment['TOTAL_ASSESSMENT'] = self.StrToNum(total_assesment)

        item['ASSESSMENT'] = assessment

        revenue = {}
        residental = response.xpath(
            './/*[contains(text(),"Revenue")]/following-sibling::*//*[contains(text(),"Residential")]/following-sibling::span/text()').get()
        commercial = response.xpath(
            './/*[contains(text(),"Revenue")]/following-sibling::*//*[contains(text(),"Commercial")]/following-sibling::span/text()').get()
        parking = response.xpath(
            './/*[contains(text(),"Revenue")]/following-sibling::*//*[contains(text(),"Parking")]/following-sibling::span/text()').get()

        revenue['RESIDENTIAL'] = self.StrToNum(residental)
        revenue['COMMERCIAL'] = self.StrToNum(commercial)
        revenue['PARKING'] = self.StrToNum(parking)
        revenue['TOTAL'] = sum(
            [revenue['RESIDENTIAL'], revenue['COMMERCIAL'], revenue['PARKING']])

        item['REVENUE'] = revenue

        expenses = {}

        insurance = response.xpath(
            './/*[contains(text(),"Expenses:")]/following-sibling::*//*[contains(text(),"Insurance")]/following-sibling::span/text()').get()
        snow_removal = response.xpath(
            './/*[contains(text(),"Expenses:")]/following-sibling::*//*[contains(text(),"Snow Removal")]/following-sibling::span/text()').get()
        electric = response.xpath(
            './/*[contains(text(),"Expenses:")]/following-sibling::*//*[contains(text(),"Electric")]/following-sibling::span/text()').get()
        gas = response.xpath(
            './/*[contains(text(),"Expenses:")]/following-sibling::*//*[contains(text(),"Gas")]/following-sibling::span/text()').get()
        energy = response.xpath(
            './/*[contains(text(),"Expenses:")]/following-sibling::*//*[contains(text(),"Energy")]/following-sibling::span/text()').get()

        expenses['INSURANCE'] = self.StrToNum(insurance)
        expenses['SNOW_REMOVAL'] = self.StrToNum(snow_removal)
        expenses['ELECTRIC'] = self.StrToNum(electric)
        expenses['GAS'] = self.StrToNum(gas)
        expenses['ENERGY'] = self.StrToNum(energy)

        expenses['TOTAL'] = sum([expenses['INSURANCE'],
                                 expenses['SNOW_REMOVAL'],
                                 expenses['ELECTRIC'],
                                 expenses['GAS'],
                                 expenses['ENERGY'],
                                 ])

        item['EXPENSES'] = expenses

        taxes = {}

        municiple_tax = response.xpath(
            './/*[contains(text(),"Municipal Tax:")]/following-sibling::span/text()').get()
        school_tax = response.xpath(
            './/*[contains(text(),"School Tax:")]/following-sibling::span/text()').get()

        taxes['MUNICIPAL_TAXE'] = self.StrToNum(municiple_tax)
        taxes['SCHOOL_TAXE'] = self.StrToNum(school_tax)

        item['TAXES'] = taxes

        yield item
