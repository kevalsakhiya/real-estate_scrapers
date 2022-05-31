import json
import re
import scrapy
from datetime import datetime
from scrapy import Request
from ..items import CentrisItem


class Centris(scrapy.Spider):
    name = 'centris'
    start_urls = [
        'https://www.centris.ca/en/multi-family-properties~for-sale?view=Thumbnail']

    def parse(self, response):

        result_count = response.xpath(
            './/*[@class="resultCount"]//text()').get()
        page_count = int(result_count.replace(',', ''))/20
        page_count = round(page_count)

        startPosition = 0
        # this code send request for all the page available
        for i in range(1, page_count+1):
            url = "https://www.centris.ca/Property/GetInscriptions"
            body = "{startPosition:"f'{startPosition}'"}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.centris.ca/en/multi-family-properties~for-sale?view=Thumbnail&uc=2',
                'Content-Type': 'application/json; charset=utf-8',
                'cache-control': 'no-cache',
                'X-CENTRIS-UC': '0',
                'X-CENTRIS-UCK': '880c3bf8-aaa2-4995-9e63-1eac36ec8c9d',
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://www.centris.ca',
                'Connection': 'keep-alive',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Length': f'{len(body)}',
                'Host': 'www.centris.ca',
                'TE': 'Trailers',
            }
            startPosition += 20
            yield Request(url,
                          body=body,
                          headers=headers,
                          method='POST',
                          dont_filter=True,
                          priority=10001,
                          callback=self.listing)

    # collect all the urls from the listing page
    def listing(self, response):
        data = json.loads(response.body)
        html_response = data.get('d').get('Result').get('html')
        response = response.replace(body=html_response)

        url_list = response.xpath(
            './/*[@data-summaryurl="SummaryUrl"]/@href').getall()
        # calling every detail_page url we collected from listing page
        for url in url_list:
            url = response.urljoin(url)
            yield Request(url,
                          priority=-10000,
                          callback=self.detail_page)

    def detail_page(self, response):
        # making calculation and saving the data
        item = {}
        item['ADDRESS'] = response.xpath(
            '(.//*[@itemprop="address"]/text())[1]').get()
        price_listed = response.xpath(
            '(.//*[@id="BuyPrice"]/text())[1]').get()
        item['PRICE_LISTED'] = self.strToint(price_listed)

        centris_number = response.xpath('.//*[@itemprop="sku"]/text()').get()
        item['CENTRIS_NUMBER'] = self.strToint(centris_number)

        item['USE_PROPERTY'] = self.xpath_data(response, 'Use of property')
        item['USE_PROPERTY'] = self.xpath_data(response, 'Building style')

        year_built = self.xpath_data(response, 'Year built')
        item['YEAR_BUILT'] = self.strToint(year_built)

        item['PARKING'] = self.xpath_data(response, 'Parking (total)')
        NBL = self.xpath_data(response, 'Number of units')
        nbl_dict = {}
        if NBL:
            NBL = NBL.split(',')
            for unit_type in NBL:
                unit_type = unit_type.split()
                unit_type = [x.strip() for x in unit_type if x.strip()]
                value = int(unit_type[-1].replace('(', '').replace(')', ''))
                nbl_dict[f'{unit_type[0]}'] = value

        item['NBL'] = nbl_dict

        gross_revenue = self.xpath_data(response, 'Potential gross revenue')
        item['GROSS_REVENUE'] = self.strToint(gross_revenue)

        item['CENTRIS_LINK'] = response.url
        lot_area = self.xpath_data(response, 'Lot area')
        if lot_area:
            lot_area = lot_area.replace('sqft', '').strip()
            item['LOT_AREA'] = self.strToint(lot_area)

        unit_size = self.xpath_data(response, 'Residential units')
        unit_dict = {'0_BEDROOM': 0,
                     '1_BEDROOM': 0,
                     '2_BEDROOM': 0,
                     '3_BEDROOM': 0,
                     '4_BEDROOM': 0,
                     '4p_BEDROOM': 0
                     }

        if unit_size:
            unit_size_list = unit_size.split(',')
            for value in unit_size_list:
                value = value.split('x')
                if '7' in value[-1] or '8' in value[-1] or '9' in value[-1] or '10' in value[-1] or 'other' in value[-1].lower():
                    unit_dict['4p_BEDROOM'] = unit_dict['4p_BEDROOM'] + \
                        int(value[0])
                elif '1' in value[-1] or '2' in value[-1]:
                    unit_dict['0_BEDROOM'] = unit_dict['0_BEDROOM'] + \
                        int(value[0])
                elif '3' in value[-1]:
                    unit_dict['1_BEDROOM'] = unit_dict['1_BEDROOM'] + \
                        int(value[0])
                elif '4' in value[-1]:
                    unit_dict['2_BEDROOM'] = unit_dict['2_BEDROOM'] + \
                        int(value[0])
                elif '5' in value[-1]:
                    unit_dict['3_BEDROOM'] = unit_dict['3_BEDROOM'] + \
                        int(value[0])
                elif '6' in value[-1]:
                    unit_dict['4_BEDROOM'] = unit_dict['4_BEDROOM'] + \
                        int(value[0])

        unit_dict_keys = list(unit_dict.keys())
        for key in unit_dict_keys:
            if not unit_dict[key]:
                unit_dict.pop(key)

        item['UNIT_SIZE'] = unit_dict

        item['CENTRIS_LISTED'] = 1

        coordinate_string = response.xpath(
            './/*[contains(@class,"onmap")]/@onclick').get()
        item['Location'] = self.location(coordinate_string)

        images_script_tag = response.xpath(
            './/article[@id="overview"]//div/script/text()').get()
        images = images_script_tag.replace(
            'window.MosaicPhotoUrls =', '').replace(';', '').strip()
        image_urls = json.loads(images)

        file_urls = []
        for c, url in enumerate(image_urls, 1):
            file_urls.append((url, f'{centris_number}_{c}.jpg',))

        item['file_urls'] = file_urls

        yield item

    def xpath_data(self, response, keyword):
        data = response.xpath(
            f'.//*[*[contains(text(),"{keyword}")]]/div/span/text()').get()
        if data:
            data = data.strip()
        return data

    def location(self, coordinate_string):
        if coordinate_string:
            try:
                separate_coordinate = re.search(
                    r'q=([\d.]+),([.\d-]+)', coordinate_string)
                Lattitude = separate_coordinate.group(1)
                Longitude = separate_coordinate.group(2)

                coordinate_dictonary = {
                    'Lattitude': Lattitude,
                    'Longitude': Longitude
                }

                return coordinate_dictonary
            except Exception:
                pass

    def strToint(self, string):
        if string:
            try:
                str_value = re.search(r'([\d,]+)', string)
                str_value = str_value.group(1)
                str_value = str_value.replace(',', '')
                int_value = int(str_value)
                return int_value
            except Exception as e:
                pass
