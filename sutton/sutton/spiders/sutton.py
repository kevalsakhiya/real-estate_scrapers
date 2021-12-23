

import scrapy
from scrapy import Request
from ..items import SuttonItem
from datetime import datetime
import re
from scrapy.shell import inspect_response


class SuttonSpider(scrapy.Spider):
    name = 'sutton'
    start_urls = [
            'https://www.suttonquebec.com/en/residential-properties-for-sale-montreal-le-plateau-mont-royal-.html?municipaliteCode=66508&regionCode=06&texteRecherche=Montr%C3%A9al%20(Le%20Plateau-Mont-Royal)',

            ]

    
    def StrToNum(self,data):
        if data:
            if '.' in data:
                data = str(data)
                try:
                    f_data = re.search(r'([\d.,]+)',data)
                    f_data = f_data.group(1)
                    f_data = f_data.replace(',','').replace(' ','')
                    f_data = float(f_data)
                    f_data = round(f_data,2)
                    return f_data
                except Exception as e:
                    print(e)
                    return 0
            else:
                try:
                    i_data = re.search(r'([\d.,]+)',data)
                    i_data = i_data.group(1)
                    i_data = i_data.replace(' ','').replace(',','')
                    i_data = int(i_data)
                    return i_data
                except Exception as e:
                    print(e)
                    return 0
        return 0

    def get_clean_data(self,data):
        if data:
            data = str(data)
            data = data.replace('\t','').replace('\n','').replace('   ','').replace('\r','')
            data = data.strip()
            return data
        else :
            return ''

    def parse(self,response):
        url_list = response.xpath('.//h2/a/@href').getall()

        for url in url_list:
            url = response.urljoin(url)
            yield Request(url,callback=self.detail_page)

        next_page = response.xpath('.//a[@class="pagesuivante"]/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url,callback=self.parse)


    def detail_page(self,response):
        item = SuttonItem()

        item['COLLECTED_DATE'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        item['WEB_LINK'] = response.url
        item['AVAILABLE'] = 1

        address = response.xpath('.//p[contains(text(),"Address")]/following-sibling::p/text()').get()
        item['ADDRESS'] = self.get_clean_data(address)

        price = response.xpath('.//*[contains(text(),"Property price")]/following-sibling::*/@value').get()
        item['PRICE_LISTED'] = self.StrToNum(price)

        mls_number = response.xpath('.//*[@data-titre="Inscription"]/text()').get()
        item['MLS_NUMBER'] = self.StrToNum(mls_number)

        feature = {}
        for tr in response.xpath('.//h4[button[contains(text(),"Characteristics")]]/following-sibling::*//tr'):
            feature_name = tr.xpath('.//td/text()').get()
            feature_detail = tr.xpath('.//td[2]/text()').get()

            feature_name = self.get_clean_data(feature_name)
            feature_detail = self.get_clean_data(feature_detail)

            feature[f'{feature_name.upper()}'] = feature_detail

        item['FEATURES'] = feature

        lot_area = response.xpath('.//*[contains(text(),"Lot surface")]/following-sibling::td/text()').re_first(r'([\d]+)')
        item['LOT_AREA'] = self.StrToNum(lot_area)

        year_built = response.xpath('.//*[@data-titre="Construction"]/text()').get()
        item['YEAR_BUILT'] = self.StrToNum(year_built)
        
        assessment = {}

        total_assesment = response.xpath('.//*[@data-titre="Municipal assessment"]/text()').re_first(r'\$([\d,]+)')

        year_assessment = response.xpath('.//*[@data-titre="Municipal assessment"]/text()').re_first(r'\(([\d]+)')

        assessment['TOTAL_ASSESSMENT'] = self.StrToNum(total_assesment)
        assessment['YEAR_ASSESSMENT'] = self.StrToNum(year_assessment)

        item['ASSESSMENT'] = assessment

        income = response.xpath('.//*[contains(text(),"Income")]/following-sibling::td/text()').get()
        item['REVENUE'] = {
                'TOTAL' : self.StrToNum(income)
        }

        expense = {}
        expense_list = ['Insurance',
                        'Snow removal',
                        'Electric',
                        'Gas',
                        'Energy cost',
                        'Other']
        
        total_expense = 0
        for expense_type in expense_list:
            expense_cost = response.xpath(f'.//*[contains(text(),"{expense_type}")]/following-sibling::td/text()').get()
            expense_cost = self.StrToNum(expense_cost)
            expense[f'{expense_type.upper()}'] = expense_cost
            total_expense = total_expense+expense_cost

        expense['TOTAL'] = total_expense

        item['EXPENSES'] = expense

        taxes = {}

        municiple_taxes = response.xpath('.//*[contains(text(),"Municipal")]/following-sibling::td/text()').get()
        school_taxes = response.xpath('.//*[contains(text(),"School taxes")]/following-sibling::td/text()').get()

        taxes['MUNICIPAL_TAXE'] = self.StrToNum(municiple_taxes)
        taxes['SCHOOL_TAXE'] = self.StrToNum(school_taxes)

        item['TAXES'] = taxes

        yield item