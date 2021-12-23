import scrapy
from scrapy import Request
import json
from ..items import PmmlItem
from datetime import datetime
import re

class PMML(scrapy.Spider):
    name = 'pmml'
    start_urls = ['https://pmml.ca/api/proprietes/avendre?sTypeLogement=iMultilogement']

    def parse(self,response):
        json_data = json.loads(response.body)
        for data in json_data:
            param = data.get('sLien')
            url = f'https://pmml.ca/api/proprietes/avendre/{param}'
            yield Request(url,meta={'param':param},callback=self.detail_page)

# i stands for int 
    def strToint(self,data):
        if data:
            try:
                i_data = str(data)
                i_data = re.search(r'([\d. ,]+)',i_data)
                i_data = i_data.group(1)
                i_data = i_data.replace(' ','')
                i_data = int(i_data)
                return i_data
            except Exception as e:
                print(e)
                return data
    
    def strTofloat(self,data):
        if data:
            try:
                f_data = str(data)
                f_data = re.search(r'([\d. ,]+)',f_data)
                f_data = f_data.group(1)
                f_data = f_data.replace(',','').replace(' ','')
                f_data = float(f_data)
                f_data = round(f_data,2)
                return f_data
            except Exception as e:
                print(e)
                return data


    def detail_page(self,response):
        param = response.meta.get('param')
        json_data = json.loads(response.body)
        data = json_data
        item = PmmlItem()

        item['COLLECTED_DATE'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        address1 = data.get('sNumeroCivique','').strip()
        address2 = data.get('sRue','').strip()
        address3 = data.get('sNomVille','').strip()

        item['PMML_URL'] = f'https://pmml.ca/en/{param}'
        item['PMML_AVAILABLE'] = 1

        item['ADDRESS'] = f'{address1} {address2} {address3}'
        price = data.get('fPrixDemande')
        item['PRICE'] = self.strToint(price)

        unit = data.get('iUnitesTotal')
        item['NBL'] = self.strToint(unit)
        
        feature_data = data['Traduction']

        cadastral_num = feature_data.get('sCadastre')
        item['CADASTRAL_NUMBER'] = cadastral_num

        land_area = data.get('fSuperficieTerrain')
        item['LOT_AREA'] = self.strTofloat(land_area)

        year_built = data.get('iAnneeConstruction')
        item['YEAR_BUILT'] = self.strToint(year_built)

        item['CONSTRUCTION_TYPE'] = data.get('sTypeConstruction')

        features = {}
        features['HEATING_SYSTEM'] = feature_data.get('sSysChauffage')
        features['HOT_WATER_SYSTEM'] = feature_data.get('sRespChaufeEau')
        features['ELECTRICAL_PANELS'] = feature_data.get('sPaneauElectrique')
        features['PLUMBING'] = feature_data.get('sPlomberie')
        features['CONDITION_OF_THE_KITCHENS'] = feature_data.get('sEtatCuisines')
        features['CONDITION_OF_THE_BATHROOMS'] = feature_data.get('sEtatCB')
        features['CONDITION_OF_FLOORING'] = feature_data.get('sPlanchers')
        features['ENVIRONMENTAL_STUDY'] = feature_data.get('sEtudeEnviro')
        features['CONDITION_OF_ROOF'] = feature_data.get('sAnneeToit')
        features['SIDING'] = feature_data.get('sRevetementExt')
        features['CONDITION_OF_BALCONIES'] = feature_data.get('sBalcons')
        features['CONDITION_OF_DOORS'] = feature_data.get('sTypePortes')
        features['CONDITION_OF_WINDOWS'] = feature_data.get('sFenetres')
        features['PARKING_SURFACE'] = feature_data.get('sRevetStationnement')
        features['INTERCOM_SYSTEM'] = feature_data.get('sSonette')
        features['FIRE_ALARM_SYSTEM'] = feature_data.get('sSysIncendie')
        features['JANITOR_AGREEMENT'] = feature_data.get('sAutre4')
        features['NUMBER_OF_PARKINGS'] = feature_data.get('sStationnements')
        features['RESPONSIBILITY_FOR_HEATING'] = feature_data.get('sRespElectricite')
        features['RESPONSIBILITY_FOR_HOT_WATER'] = feature_data.get('sRespEauChaude')
        features['RESPONSIBILITY_FOR_APPLIANCES'] = feature_data.get('sRespElectros')
        features['WASHER_AND_DRYER_OUTLET'] = feature_data.get('sLaveuseSecheuse')
        features['LAUNDRY'] = feature_data.get('sBuanderie')

        item['FEATURES'] = features

        assessment = {}
        lot_assment = feature_data.get('sEvaluationMunicipaleTerrain')
        assessment['LOT_ASSESSMENT'] = self.strToint(lot_assment)

        building_assessment = feature_data.get('sEvaluationMunicipaleBatiment')
        assessment['BUILDING_ASSESSMENT'] = self.strToint(building_assessment)

        item['ASSESSMENT'] = assessment

        unit_dict = {}
        unit = feature_data.get('sRepartition')
        if unit:
            unit_list = unit.split('+')
            
            for unit in unit_list:
                if 'X' in unit:
                    value = unit.split('X')
                else:
                    value = unit.split('x')

                if '1.5' in value[-1] or '2.5' in value[-1]:
                        unit_dict['0_BEDROOM'] = int(value[0])
                elif '3.5' in value[-1]:
                    unit_dict['1_BEDROOM'] = int(value[0])
                elif '4.5' in value[-1]:
                    unit_dict['2_BEDROOM'] = int(value[0])
                elif '5.5' in value[-1]:
                    unit_dict['3_BEDROOM'] = int(value[0])
                elif '6.5' in value[-1]:
                    unit_dict['4_BEDROOM'] = int(value[0])
                elif '7.5' in value[-1] or '8.5' in value[-1] or '9.5' in value[-1]:
                    unit_dict['5_BEDROOM'] = int(value[0])
        
        item['UNIT_SIZE'] = unit_dict

        taxes = {}
        municiple_taxe = data.get('fTaxesMunicipales')
        taxes['MUNICIPAL_TAXE'] = self.strToint(municiple_taxe)

        school_taxe = data.get('fTaxesScolaires')
        taxes['SCHOOL_TAXE'] = self.strToint(school_taxe)

        item['TAXES'] = taxes
        
        revenue = {}
        residential = data.get('fRevenusRes')
        revenue['RESIDENTIAL'] = self.strToint(residential)

        parking = data.get('fRevenusStationnement')
        revenue['PARKING'] = self.strToint(parking)

        laundry = data.get('fRevenusBuanderie')
        revenue['LAUNDRY'] = self.strToint(laundry)

        storage = data.get('fRevenusLockers')
        revenue['STORAGE'] = self.strToint(storage)

        commercial = data.get('fRevenusComm')
        revenue['COMMERCIAL'] = self.strToint(commercial)

        item['REVENU'] = revenue 
        
        expences = {}
        electricity = data.get('fElectricite')
        expences['ELECTRICITY'] = self.strToint(electricity)
        heating = data.get('fChauffage')
        expences['HEATING'] = self.strToint(heating)
        insurance = data.get('fAssurances')
        expences['INSURANCE'] = self.strToint(insurance)
        snow_removal = data.get('fDeneigement')
        expences['SNOW REMOVAL'] = self.strToint(snow_removal)
        equipment_rental = data.get('fGazon')
        expences['EQUIPMENT_RENTAL'] = self.strToint(equipment_rental)
        elevator = data.get('fAscenceur')
        expences['ELEVATOR'] = self.strToint(elevator)

        item['EXPENSES'] = expences

        kpi = {}
        price_per_unit = data.get('fCPL')
        kpi['PRICE_PER_UNIT'] = self.strTofloat(price_per_unit)
        gim = data.get('fMRB')
        kpi['GIM'] = self.strTofloat(gim)
        nim = data.get('fMRN')
        kpi['NIM'] = self.strTofloat(nim)
        cap = data.get('fTGA')
        kpi['CAP'] = self.strTofloat(cap)

        item['KPI'] = kpi

        location = {'type':'Point'}
        latitude = float(data.get('dPosLat'))
        longitude = float(data.get('dPosLong'))
        location['coordinates'] = [longitude,latitude]

        item['LOCATION'] = location

        yield item