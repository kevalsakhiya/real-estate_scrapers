import scrapy
from scrapy import Request
from ..items import DuproprioItem
from datetime import datetime
import re

class Duproprio(scrapy.Spider):
    name = 'duproprio'
    start_urls = [
        'https://duproprio.com/en/search/list?search=true&type%5B0%5D=multiplex']
    page = 2

    def parse(self,response):
        detail_page_url_list = response.xpath(
            './/a[@class="search-results-listings-list__item-image-link "]/@href').getall()

        for url in detail_page_url_list:
            detail_page_url = response.urljoin(url)
            yield Request(detail_page_url,
                          callback = self.detail_page,
            )
        
        next_page = response.xpath('.').re_first(r'"nextLinkActive":([a-z]+)')
        if 'true' in next_page:
            pagination_url = f'https://duproprio.com/en/search/list?search=true&type%5B0%5D=multiplex&is_for_sale=1&with_builders=1&parent=1&pageNumber={self.page}&sort=-published_at'
            self.page+=1
            yield Request(pagination_url,
                          callback=self.parse,
                          )

    def detail_page(self,response):
        item = DuproprioItem()
        currunt_date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        item ['COLLECTED_DATE'] = currunt_date
        item['DUPROPRIO_AVAILABLE'] = 1
        address = response.xpath(
            './/*[@class="listing-location__address"]//text()').getall()
        if address:
            address = [x.strip() for x in address if x.strip()]
            address = list(set(address))
            item['ADDRESS'] = ', '.join(address)

        price = response.xpath('.//*[@class="listing-price__amount"]//text()').get()
        item['PRICE_LISTED'] = self.strToint(price)

        duproprio_number = response.xpath('.//*[@class="listing-location__code"]//text()').get()
        item['DUPROPRIO_NUMBER'] = self.strToint(duproprio_number)

        NBL = response.xpath('.//*[@class="listing-location__title"]/a/text()').get()
        plex_dictonary = {
            'duplex': '2',
            'triplex': '3',
            'quadruplex': '4',
            'quintuplex':'5',
            '6 units or more':'6+'
        }
        for key, value in plex_dictonary.items():
            if key in NBL.lower():
                value = self.strToint(value)
                item['NBL'] = value

        lot_area = response.xpath('.//*[contains(@class,"number--dimensions")]/text()').get()
        item['LOT_AREA'] = self.strToint(lot_area)

        year_built = response.xpath(
            './/*[contains(text(),"Year of construction")]/following-sibling::*[2]/text()').get()
        item['YEAR_BUILT'] = self.strToint(year_built)

        features = {}
        building_dimension = self.get_data(response,'Building dimensions')
        features['BUILDING_DIMENSION'] = self.strToint(building_dimension)

        general_condition = self.get_data(response, 'General condition')
        features['GENERAL_CONDITION'] = general_condition

        occupation_rate = self.get_data(response, 'Occupation rate')
        features['OCCUPATION_RATE'] = occupation_rate

        certificate_of_location = self.get_data(
                                response, 'Certificate of Location')
        features['CERTIFICATE_LOCATION'] = certificate_of_location

        parking = self.get_data(response, 'Number of parkings')
        features['NUMBER_OF_PARKING'] = parking

        features['FLOOR_COVERING'] = self.get_features(response, 'Floor coverings:')
        features['WINDOWS'] = self.get_features(response, 'Windows:')
        features['NEAR_COMMERCE'] = self.get_features(
                                        response, 'Near Commerce:')
        features['KITCHEN'] = self.get_features(response, 'Kitchen:')
        features['NEAR_EDUCATIONAL_SERVICES'] = self.get_features(
                                            response, 'Near Educational Services:')
        features['BATHROOM'] = self.get_features(response,'Bathroom:')
        features['PARKING'] = self.get_features(
                                    response, 'Parking / Driveway:')
        features['LOCATION'] = self.get_features(response, 'Location:')
        features['NEAR_RECREATIO_SERVICE'] = self.get_features(
                                            response, 'Near Recreational Service:')
        features['LOT_DESCRIPTION'] = self.get_features(response,'Lot description:')
        features['ROOF'] = self.get_features(response, 'Roof:')
        features['ELECTRIC_SYSTEM'] = self.get_features(
                                            response, 'Electric system:')
        features['HEATING_SYSTEM'] = self.get_features(
                                            response, 'Heating source:')

        item['FEATURES'] = features

        assessment = {}

        year_assessment = self.get_data(response, "Municipal evaluation\'s date")
        year_assessment = response.xpath(
            './/*[contains(text(),"Municipal evaluation\'s date")]/following-sibling::*[2]/text()').get()
        assessment['YEAR_ASSESSMENT'] = self.strToint(year_assessment)

        lot_assessment = response.xpath(
            './/*[contains(text(),"Lot\'s municipal evaluation")]/following-sibling::*[2]/text()').get()
        assessment['LOT_ASSESSMENT'] = self.strToint(lot_assessment)

        building_assessment = response.xpath(
                './/*[contains(text(),"Building\'s municipal evaluation")]/following-sibling::*[2]/text()').get()
        assessment['BUILDING_ASSESSMENT'] = self.strToint(building_assessment)

        item['ASSESSMENT'] = assessment
        unit_size ={}

        unit_list = response.xpath(
            './/*[@class="listing-box__dotted-row"]/*[contains(text()," Bedroom")]/text()').getall()
        unit_list = [x.strip() for x in unit_list if x.strip()]
        for unit in unit_list:
            unit_data = self.get_data(response,unit)
            unit_size[unit] = self.strToint(unit_data)

        item['UNIT_SIZE'] = unit_size

        if item['NBL']>5:
            bedroom_quantity = 0
            for bedroom, quanity in unit_size.items():
                bedroom_quantity = bedroom_quantity + quanity

            item['NBL'] = bedroom_quantity

        
        taxes = {}
        municiple_year = self.get_data(response, 'Taxes year')
        taxes['MUNICIPLE_YEAR'] = self.strToint(municiple_year)
        
        municiple_taxes = self.get_data(response, 'Municipal taxes')
        taxes['MUNICIPLE_TAXES'] = self.strToint(municiple_taxes)

        school_taxes = self.get_data(response, 'School taxes')
        taxes['SCHOOL_TAXES'] = self.strToint(school_taxes)

        item['TAXES'] = taxes


        revenue = {}
        annual_revenue = self.get_data(response, 'Annual income')
        revenue['TOTAL'] = self.strToint(annual_revenue)

        item['REVENUE'] = revenue

        expenses = {}

        electricity = response.xpath(
            './/*[contains(text(),"Electricity")]/following-sibling::*[contains(@class,"yearly-costs")]/text()').get()
        expenses['ELECTRICITY'] = self.strToint(electricity)

        maintenance_fees = response.xpath(
                './/*[contains(text(),"Maintenance fees")]/following-sibling::*[contains(@class,"yearly-costs")]/text()').get()
        expenses['MAINTENANCE_FEES'] = self.strToint(maintenance_fees)

        insurance = response.xpath(
                './/*[contains(text(),"Insurance")]/following-sibling::*[contains(@class,"yearly-costs")]/text()').get()
        expenses['INSURANCE'] = self.strToint(insurance)

        item['EXPENSES'] = expenses

        location = {}
        location['latitude'] = response.xpath('.').re_first(r'"latitude":([\d.-]+)')
        location['longitude'] = response.xpath('.').re_first(r'"longitude":([\d.-]+)')

        item['LOCATION'] = location
        yield item


    def strToint(self,string):
        if string:
            if 'x' in string:
                try:
                    string_list = string.split()
                    area = string_list[0].split('x')
                    x = re.search(r'([\d,]+)', area[0]).group(1)
                    y = re.search(r'([\d,]+)', area[1]).group(1)
                    lot_area = int(x)*int(y)
                    return lot_area
                except Exception:
                    pass
            else:
                try:
                    str_value = string.replace(' ', '')
                    str_value = re.search(r'([\d,]+)', str_value)
                    str_value = str_value.group(1)
                    str_value = str_value.replace(',', '')
                    int_value = int(str_value)
                    return int_value
                except Exception as e:
                    print(e)    

    def get_clean_data(self,string):
        if string:
            string = string.replace('\t','').replace(
                            '\n','').replace('   ','').replace('\r','')
            string = string.strip()
            return string
        else :
            return ''

    def get_data(self,response,keyword):
        keyword = keyword.replace("'",'')
        data = response.xpath(f'.//*[contains(text(),"{keyword}")]/following-sibling::*[2]/text()').get()
        data = self.get_clean_data(data)
        return data

    def get_features(self,response,keyword):
        feature_list = response.xpath(
            f'.//*[contains(text(),"{keyword}")]/following-sibling::*/li/text()').getall()
        feature_list = [x.strip() for x in feature_list if x.strip()]
        
        if len(feature_list)>1:
            feature_dictionary = {}
            for count,feature in enumerate(feature_list,1):
                feature_dictionary[f'FEATURE_{count}'] = feature
            return feature_dictionary
        else:
            feature = ''.join(feature_list)
            return feature


