import re
import json
import scrapy
from scrapy import Request
from datetime import datetime
from ..items import RemaxQuebecItem


class RemexQuebec(scrapy.Spider):
    name = 'remax'
    start_urls = ['https://www.remax-quebec.com/en/index.rmx']

    def __init__(self, category=None, *args, **kwargs):
        super(RemexQuebec, self).__init__(*args, **kwargs)
        self.category = category

    def parse(self, response):
        url = "https://www.remax-quebec.com/en/recherche/plex/resultats.rmx#listing"
        body = f'mode=criterias&order=date_desc&query=&categorie=plex&selectItemcategorie=plex&genres={self.category}&selectItemgenres={self.category}&minPrice=0&selectItemminPrice=0&transacTypes=vente&selectItemtransacTypes=vente&caracResi7=_&caracResi1=_&caracResi4=_&caracResi8=_&caracResi2=_&caracResi12=_&caracComm4=_&caracComm2=_&caracComm5=_&caracFarm3=_&caracFarm1=_&caracLand1=_&caracResi5=_&caracResi9=_&caracResi10=_&caracResi3=_&caracResi6=_&caracResi13=_&caracComm3=_&caracComm1=_&caracFarm2=_&uls='
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.remax-quebec.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.remax-quebec.com/en/recherche/plex/index.rmx?transacTypes=vente',
            'Host': 'www.remax-quebec.com',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Upgrade-Insecure-Requests': '1',
                    'Proxy-Authorization': 'Basic LnN2QDEyMjE2NDM0O2luLjo1UjQ2TDlITWYrM3VhODJFRUxINTBPNXFndzVseSs4ZmJYWkJTOURDKzVjPQ=='
        }
        yield Request(url,
                      body=body,
                      headers=headers,
                      callback=self.listing_page,
                      meta={'cookiejar': 1},
                      method='POST',
                      )

    def listing_page(self, response):
        cookiejar = response.meta.get('cookiejar')
        url_list = response.xpath(
            './/a[@class="property-details"]/@href').getall()
        for url in url_list:
            details_url = response.urljoin(url)
            yield Request(details_url,
                          meta={'cookiejar': 1},
                          priority=-10000,
                          callback=self.detail_page
                          )

        next_page = response.xpath('.//a[@aria-label="Suivant"]/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url,
                          meta={'cookiejar': 1},
                          priority=1000,
                          callback=self.listing_page)

    def detail_page(self, response):
        item = RemaxQuebecItem()
        item['REMAX_AVAILABLE'] = 1
        name = response.xpath('.//*[@class="Caption__Name"]/text()').get()
        plex_dictonary = {
            'duplex': 2,
            'two': 2,
            'triplex': 3,
            'three': 3,
            'quardplex': 4,
            'quadruplex': 4,
            'four': 4,
        }
        for key, value in plex_dictonary.items():
            if key in name.lower():
                item['NBL'] = value

        if not item.get('NBL'):
            for num in range(5, 50):
                if str(num) in name:
                    item['NBL'] = num
                    break

        address = response.xpath(
            './/h2[@class="Description__Title"]//text()').getall()
        address = [x.strip() for x in address if x.strip()]
        address = ' '.join(address)
        item['ADDRESS'] = address

        price = response.xpath('.//*[@itemprop="price"]/@content').get()
        if price:
            price = self.strToint(price)

        item['PRICE_LISTED'] = price

        MLS_NUMBER = response.xpath(
            './/*[@class="Description__ULS"]/text()').re_first(r'([\d]+)')
        if MLS_NUMBER:
            MLS_NUMBER = int(MLS_NUMBER)
        item['MLS_NUMBER'] = MLS_NUMBER

        item['COLLECTED_DATE'] = datetime.now().strftime(
            f'%d/%m/%y %H:%M:%S_MLS=>{MLS_NUMBER}')

        year_built = response.xpath(
            './/*[contains(text(),"Year built")]/*[@class="Description__Item__Data"]/text()').get()
        if year_built:
            year_built = self.strToint(year_built)
        else:
            year_built = 'Null'
        item['YEAR_BUILT'] = year_built

        lot_area = response.xpath(
            './/*[contains(text(),"Lot area")]/*[@class="Description__Item__Data"]/*/text()').get()
        if lot_area:
            item['LOT_AREA'] = self.strToint(lot_area)
        item['REMAX_QUEBEC_LINK'] = response.url
        item['BUILDING_SIZE'] = self.property_specification(response, 'Size')

        features = {}
        features['Window Type'] = self.property_specification(
            response, 'Window Type')
        features['Windows'] = self.property_specification(response, 'Windows')
        features['Foundation'] = self.property_specification(
            response, 'Foundation')
        features['Siding'] = self.property_specification(response, 'Siding')
        features['Roofing'] = self.property_specification(response, 'Roofing')
        features['Floor Covering'] = self.property_specification(
            response, 'Floor Covering')
        features['Living area'] = self.property_specification(
            response, 'Living area')
        features['Dividing Floor'] = self.property_specification(
            response, 'Dividing Floor')
        features['Lot size'] = self.property_specification(
            response, 'Lot size')
        features['Topography'] = self.property_specification(
            response, 'Topography')
        features['Driveway'] = self.property_specification(
            response, 'Driveway')
        features['Parking'] = self.property_specification(
            response, 'Parking (total)')
        features['Zoning'] = self.property_specification(response, 'Zoning')
        features['Heating System'] = self.property_specification(
            response, 'Heating System')
        features['Heating Energy'] = self.property_specification(
            response, 'Heating Energy')
        features['Water Supply'] = self.property_specification(
            response, 'Water Supply')
        features['Sewage System'] = self.property_specification(
            response, 'Sewage System')
        features['Proximity'] = self.property_specification(
            response, 'Proximity')

        key_list = list(features.keys())
        for key in key_list:
            if not features[key]:
                features.pop(key)
        item['FEATURES'] = features

        assignment_dictionary = {}
        assignment_dictionary['YEAR Assessment'] = response.xpath(
            './/h6[contains(text(),"Assessment")]/text()').re_first(r'([\d]+)')
        assignment_dictionary['Lot assessment'] = self.finiancial_details(
            response, 'Lot assessment')
        assignment_dictionary['Building assessment'] = self.finiancial_details(
            response, 'Building assessment')
        assignment_dictionary['Municipal assessment'] = self.finiancial_details(
            response, 'Municipal assessment')

        if assignment_dictionary:
            for key, value in assignment_dictionary.items():
                if value:
                    clean_value = self.strToint(value)
                    assignment_dictionary[key] = clean_value

        item['ASSESSMENT'] = assignment_dictionary

        texes = {}
        miniciple_year = response.xpath(
            './/label[contains(text(),"Municipal")]/following-sibling::text()').getall()
        texes['Municipal Year'] = self.listTostring(miniciple_year)
        school_year = response.xpath(
            './/*[contains(text(),"School")]/following-sibling::text()').getall()
        texes['School Year'] = self.listTostring(school_year)
        texes['SCHOOL TAXE'] = response.xpath(
            './/*[contains(text(),"School")]/following-sibling::label/text()').get()
        texes['Municipal Taxes'] = response.xpath(
            './/*[contains(text(),"Taxes")]/following-sibling::ul[1]//*[contains(text(),"Municipal")]/following-sibling::label/text()').get()
        if texes:
            for key, value in texes.items():
                if value:
                    clean_value = value.replace('\t', '').replace(
                        '\n', '').replace('\r', '').replace('   ', '')
                    clean_value = self.strToint(clean_value)
                    texes[key] = clean_value

        item['TAXES'] = texes

        annual_expences_list = response.xpath(
            './/*[contains(text(),"Annual Expenses")]/following-sibling::*[1]//*[@class="Financials__Label"]/text()').getall()
        annual_expences_list = [x.strip()
                                for x in annual_expences_list if x.strip()]
        annual_expences_list = list(set(annual_expences_list))
        annual_expences_dictionaty = {}

        for expence in annual_expences_list:
            if 'snow' in expence.lower():
                snow = {}
                expence_value = self.finiancial_details(response, f'{expence}')
                if expence_value:
                    expence_value = self.strToint(expence_value)
                    snow[f'{expence}'] = expence_value
                    annual_expences_dictionaty['SNOW'] = snow

            elif 'total' in expence.lower():
                expence_value = response.xpath(
                    './/*[contains(text(),"Annual Expenses")]/following-sibling::ul[1]//*[contains(text(),"Total")]/following-sibling::label/text()'
                ).getall()
                if expence_value:
                    expence_value = self.listTostring(expence_value)
                    expence_value = self.strToint(expence_value)
                    annual_expences_dictionaty[f'{expence}'] = expence_value

            else:
                expence_value = self.finiancial_details(response, f'{expence}')
                if expence_value:
                    expence_value = self.strToint(expence_value)
                    annual_expences_dictionaty[f'{expence}'] = expence_value

        energy_expences_list = response.xpath(
            './/*[contains(text(),"Energy")]/following-sibling::*[1]//*[@class="Financials__Label"]//text()').getall()
        energy_expences_list = [x.strip()
                                for x in energy_expences_list if x.strip()]
        energy_expences_list = list(set(energy_expences_list))
        for expence in energy_expences_list:
            expence_value = self.finiancial_details(response, f'{expence}')
            if expence_value:
                expence_value = self.strToint(expence_value)
                annual_expences_dictionaty[f'{expence}'] = expence_value

        item['EXPENSES'] = annual_expences_dictionaty

        yearly_revenu_list = response.xpath(
            './/*[contains(text(),"Gross yearly revenu")]/following-sibling::*[1]//*[@class="Financials__Label"]/text()').getall()
        yearly_revenu_list = [x.strip()
                              for x in yearly_revenu_list if x.strip()]
        yearly_revenu_list = list(set(yearly_revenu_list))
        yearly_revenu_dictonary = {}
        for expence in yearly_revenu_list:
            if 'total' in expence.lower():
                yearly_revenu = response.xpath(
                    './/*[contains(text(),"Gross yearly revenu")]/following-sibling::ul[1]//*[contains(text(),"Total")]/following-sibling::label/text()'
                ).getall()
                yearly_revenu = self.listTostring(yearly_revenu)

            else:
                yearly_revenu = self.finiancial_details(response, f'{expence}')

            if yearly_revenu:
                yearly_revenu = self.strToint(yearly_revenu)
                yearly_revenu_dictonary[f'{expence}'] = yearly_revenu

        item['REVENU'] = yearly_revenu_dictonary

        yield item

    def property_specification(self, response, keyword):
        if keyword:
            detail = response.xpath(
                f'.//*[contains(text(),"{keyword}")]/following-sibling::*/text()').getall()
            detail = [x.strip() for x in detail if x.strip()]
            detail = list(set(detail))
            detail = ', '.join(detail)
            detail = detail.replace('\t', '').replace(
                '\n', '').replace('\r', '').replace('   ', '')
            return detail

    def strToint(self, string):
        try:
            str_value = re.search(r'([\d,]+)', string)
            str_value = str_value.group(1)
            str_value = str_value.replace(',', '')
            int_value = int(str_value)
            return int_value
        except Exception as e:
            print(e)

    def finiancial_details(self, response, keyword):
        if keyword:
            detail = response.xpath(
                f'.//*[contains(text(),"{keyword}")]/following-sibling::label/text()').getall()
            detail = [x.strip() for x in detail if x.strip()]
            detail = list(set(detail))
            detail = ', '.join(detail)
            detail = detail.replace('\t', '').replace(
                '\n', '').replace('\r', '').replace('   ', '')
            return detail

    def listTostring(self, res_list):
        try:
            res_list = [x.strip() for x in res_list if x.strip()]
            res_list = list(set(res_list))
            res_string = ''.join(res_list).strip()
            res_string = res_string.replace('(', '').replace(')', '')
            return res_string
        except Exception as e:
            print(e)
