import scrapy
from scrapy import Request
import json
from ..items import KijijiItem
from datetime import datetime
import re
from scrapy.shell import inspect_response


class Kijiji(scrapy.Spider):
	name = 'kijiji'

	def __init__(self, page=None, *args, **kwargs):
	        super(Kijiji, self).__init__(*args, **kwargs)
	        self.page = page

	def start_requests(self):
		if self.page:
			page_url = f'https://www.kijiji.ca/b-appartement-condo/quebec/page-{self.page}/c37l9001?ad=offering'
			yield Request(page_url, callback=self.parse)
		else:
			print('\n\nPLEASE GIVE COMMAND WITH THE PAGE NUMBER\n==> scrapy crawl kijiji -a page=1\n\n')

	def parse(self, response):
		# inspect_response(response,self)

		url_list = response.xpath('.//*[@class="title "]/@href').getall()

		for url in url_list:
			detail_page_url = response.urljoin(url)

			yield Request(detail_page_url,
                            callback=self.detail_page
                 )

	def detail_page(self, response):
		# inspect_response(response,self)
		item = KijijiItem()

		item['COLLECTED_DATE'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
		item['WEB_LINK'] = response.url

		address = response.xpath('.//*[contains(@class,"address")]/text()').get()
		item['ADDRESS'] = address

		longitude = response.xpath('.//*[@property="og:longitude"]/@content').get()
		latitude = response.xpath('.//*[@property="og:latitude"]/@content').get()

		location = {
                    'Type': 'Point',
               					'Coordinates': [longitude, latitude]
		}

		item['LOCATION'] = location

		price = response.xpath(
			'.//*[contains(@class,"priceWrapper")]/*/@content').get()
		if price:
			price = price.replace('.', '').replace(',', '')
			try:
				price = int(price)
			except:
				price = None
		item['PRICE'] = price

		type_ = response.xpath(
			'(.//*[@class="noLabelValue-3861810455"]/text())[1]').get()
		item['TYPE'] = type_

		bedroom = response.xpath(
			'(.//*[@class="noLabelValue-3861810455"]/text())[2]').re_first(r'([\d]+)')
		if bedroom:
			bedroom = bedroom.replace('Bedrooms:', '')
			try:
				bedroom = int(bedroom)
				item['BEDROOM_NB'] = bedroom

			except Exception as e:
				print(e)
				item['BEDROOM_NB'] = None

		bathroom = response.xpath(
			'(.//*[@class="noLabelValue-3861810455"]/text())[3]').re_first(r'([\d]+)')
		try:
			item['BATHROOM_NB'] = int(bathroom)
		except Exception:
			item['BATHROOM_NB'] = None
		utilities = {
                    'ELECTRICITY': False,
               					'HEATING': False,
               					'WATER': False,
		}

		electricity = response.xpath('.//*[contains(text(),"Hydro")]/@class').get()
		if electricity:
			if 'available' in electricity:
				utilities['ELECTRICITY'] = True

		heat = response.xpath('.//*[contains(text(),"Heat")]/@class').get()
		if heat:
			if 'available' in heat:
				utilities['HEATING'] = True

		water = response.xpath('.//*[contains(text(),"Water")]/@class').get()
		if water:
			if 'available' in water:
				utilities['WATER'] = True

		item['UTILITIES'] = utilities

		wifi = response.xpath(
			'.//*[contains(text(),"Wi-Fi and More")]/following-sibling::*/text()').get()
		item['TELECOM'] = wifi

		parking = response.xpath(
			'.//*[contains(text(),"Parking Included")]/following-sibling::*/text()').get()
		if parking:
			parking = parking.replace(',', '')
			try:
				int(parking)
			except Exception as e:
				print('parking', e)
		item['PARKING'] = parking

		agreement_type = response.xpath(
			'.//*[contains(text(),"Agreement Type")]/following-sibling::*/text()').get()
		item['AGREEMENT_TYPE'] = agreement_type

		moving_date = response.xpath(
			'.//*[contains(text(),"Move-In Date")]/following-sibling::*/*/text()').get()
		item['MOVING_DATE'] = moving_date

		pet_friendly = response.xpath(
			'.//*[contains(text(),"Pet Friendly")]/following-sibling::*/text()').get()
		if pet_friendly:
			if 'No' in pet_friendly:
				pet_friendly = False
			else:
				pet_friendly = True
		item['PET_FRIENDLY'] = pet_friendly

		size_sqft = response.xpath(
			'.//*[contains(text(),"Size (sqft)")]/following-sibling::*/text()').get()
		if size_sqft:
			size_sqft = size_sqft.replace(',', '')
			try:
				size_sqft = int(size_sqft)
			except Exception as e:
				print('sqft', e)

		item['UNIT_SIZE'] = size_sqft

		furnished = response.xpath(
			'.//*[contains(text(),"Furnished")]/following-sibling::*/text()').get()
		if furnished:
			if 'No' in furnished:
				furnished = False
			else:
				furnished = True
		item['FURNISHED'] = furnished

		appliance_list = []

		for li in response.xpath('.//*[contains(text(),"Appliances")]/following-sibling::*/*'):
			appliance = li.xpath('.//text()').get()
			if appliance:
				appliance_list.append(appliance)

		item['APPLIANCE'] = appliance_list

		air_condition = response.xpath(
			'.//*[contains(text(),"Air Conditioning")]/following-sibling::*//text()').get()
		if air_condition:
			if 'No' in air_condition:
				air_condition = False
			else:
				air_condition = True
		item['AIR_CONDITIONING'] = air_condition

		personal_outdoor_space = response.xpath(
			'.//*[contains(text(),"Personal Outdoor Space")]/following-sibling::*//text()').get()
		item['PERSONAL_OUTDOOR_SPACE'] = personal_outdoor_space

		smoking_permitted = response.xpath(
			'.//*[contains(text(),"Smoking Permitted")]/following-sibling::*//text()').get()
		if smoking_permitted:
			if 'No' in smoking_permitted:
				smoking_permitted = False
			else:
				smoking_permitted = True
		item['SMOKING_PERMITTED'] = smoking_permitted

		amenitie_list = []
		for li in response.xpath('.//*[contains(text(),"Amenities")]/following-sibling::*/*'):
			amenitie = li.xpath('.//text()').get()
			if amenitie:
				amenitie_list.append(amenitie)

		item['BUILDING_AMENITIES'] = amenitie_list

		if item["PRICE"]:
			yield item
