import scrapy
from scrapy import Request
from ..items import RegistreentreprisesItem
from datetime import datetime
<<<<<<< HEAD
# import pymongo

class RegistreEntreprises(scrapy.Spider):
    name = 'reg'
    # NEQ_LIST = []
    NEQ_LIST =  [
            '1167061671'
            # '1140030355',
            # '1140030363',
            # '1140031379',
            # '1140031486',
            # '1140031510',
            # '1140031536',
            # '1140031551',
            # '1140031908',
            ]


import pymongo

class RegistreEntreprises(scrapy.Spider):
    name = 'reg'
    NEQ_LIST = []

    def __init__(self):
        try:
            makingConnection = pymongo.MongoClient(
                    'mongodb://pusher_rw:j74CMvuLPHLCxdK5yyLw@ec2-99-79-53-153.ca-central-1.compute.amazonaws.com:27017/UPKY_MONGODB_DEV')
            db = makingConnection["UPKY_MONGODB_DEV"]
            connection = db['RE_ENTREPRISE']
        except Exception as e:
            print(e)
            
        documents = connection.find({"ACTIONNAIRES" : { "$exists" : False }})

        for doc in documents:
            self.NEQ_LIST.append(doc['NEQ'])

        makingConnection.close()

        return None

    
    def start_requests(self):

        url = 'https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_19A_PIU_RechEnt_PC/PageRechSimple.aspx?T1.CodeService=S00436'
        
        headers = {
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Language': 'en-US,en;q=0.5',
                  'Content-Type': 'application/x-www-form-urlencoded',
                  'Origin': 'https://www.registreentreprises.gouv.qc.ca',
                  'Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'Accept-Encoding': 'gzip, deflate, br',

                }
        yield Request(url,
                      headers=headers,
                      meta = {'index_num' : 0},
                      dont_filter=True, 
                      callback=self.parse)


    def parse(self,response):
        index_num = response.meta.get('index_num')

        view_state_generator = response.xpath('.//*[@id="__VIEWSTATEGENERATOR"]/@value').get()
        event_validation = response.xpath('.//*[@id="__EVENTVALIDATION"]/@value').get()
        view_state = response.xpath('.//*[@id="__VIEWSTATE"]/@value').get()

        headers = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Language': 'en-US,en;q=0.5',
              'Content-Type': 'application/x-www-form-urlencoded',
              'Origin': 'https://www.registreentreprises.gouv.qc.ca',
              'Connection': 'keep-alive',
              'Upgrade-Insecure-Requests': '1',
              'Accept-Encoding': 'gzip, deflate, br',
            }
        
        formdata = {
            'ctl00$CPH_K1ZoneContenu1_Cadr$IdSectionRechSimple$IdSectionRechSimple$K1Fieldset1$ChampRecherche$_cs' : f'{self.NEQ_LIST[index_num]}',
            'ctl00$CPH_K1ZoneContenu1_Cadr$IdSectionRechSimple$IdSectionRechSimple$CondUtil$CaseConditionsUtilisation$0': 'UtilisateurAccepteConditionsUtilisation',
            'ctl00$CPH_K1ZoneContenu1_Cadr$IdSectionRechSimple$IdSectionRechSimple$KRBTRechSimple$btnRechercher': 'Search',
            'ctl00$CPH_K1ZoneContenu1_Cadr$IdSectionRechSimple$IdSectionRechSimple$K1Fieldset1$InputACauseBugIExplorer': "",
            'IdCtrlPatientez' : "CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_KRBTRechSimple_btnRechercher",
        }

        yield scrapy.FormRequest.from_response(response, 
                                               dont_filter=True, 
                                               formdata=formdata, 
                                               headers=headers, 
                                               callback=self.detail_page,
                                               )

        if index_num<len(self.NEQ_LIST)-1:
            index_num+=1
            url = 'https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_19A_PIU_RechEnt_PC/PageRechSimple.aspx?T1.CodeService=S00436'
            headers = {
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Language': 'en-US,en;q=0.5',
                  'Content-Type': 'application/x-www-form-urlencoded',
                  'Origin': 'https://www.registreentreprises.gouv.qc.ca',
                  'Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'Accept-Encoding': 'gzip, deflate, br',

                }
            yield Request(url,
                          headers=headers,
                          dont_filter=True, 
                          meta={'index_num':index_num},
                          callback=self.parse
                )
    def clean_data(self,string):
        if string:
            string = string.replace('\t','').replace(
                            '\n','').replace('   ','').replace('\r','')
            string = string.strip()

            if 'input' in string:
                return ''
            else:
                return string


    def detail_page(self,response):
        neq = response.xpath('.//*[*[*[contains(text(),"Numéro d\'entreprise du Québec (NEQ)")]]]/p/text()').get()
        cookiejar = response.meta.get('cookiejar')
        
        item = RegistreentreprisesItem()

        NEQ = response.xpath('.//*[*[contains(text(),"NEQ")]]/following-sibling::*/text()').get()
        if NEQ:
            item['NEQ'] = int(NEQ)
        actionnarie_list = []
        for fieldset in response.xpath('.//*[contains(text(),"Actionnaires")]/following-sibling::*[*[contains(text(),"actionnaire")]]'):
            Nom = fieldset.xpath('.//*[*[contains(text(),"Nom")]]/following-sibling::*/text()').get()
            adresse = fieldset.xpath('.//*[*[contains(text(),"Adresse")]]/following-sibling::*/text()').get()

            actionnarie_dict = {}
            actionnarie_dict['NOM'] = self.clean_data(Nom)
            actionnarie_dict['ADR'] = self.clean_data(adresse)

            actionnarie_list.append(actionnarie_dict)
        item['ACTIONNAIRES'] = actionnarie_list

        administrateurs_list = []
        for fieldset in response.xpath('.//*[contains(text(),"Liste des administrateurs")]/following-sibling::*[1]/fieldset'):
            administrateurs_dict = {}
            
            Nom = fieldset.xpath('.//*[*[contains(text(),"Nom")]]/following-sibling::*/text()').get()
            administrateurs_dict['NOM_FAMILLE'] = self.clean_data(Nom)
            
            date_debut = fieldset.xpath('.//*[*[contains(text(),"Date du début de la charge")]]/following-sibling::*/@value').get()
            administrateurs_dict['DATE_DEBUT'] = self.clean_data(date_debut)
            
            date_fin = fieldset.xpath('.//*[*[contains(text(),"Date de fin de la charge")]]/following-sibling::*/@value').get()
            date_debut = fieldset.xpath('.//*[*[contains(text(),"Date du début de la charge")]]/following-sibling::*/text()').get()
            administrateurs_dict['DATE_DEBUT'] = self.clean_data(date_debut)
            
            date_fin = fieldset.xpath('.//*[*[contains(text(),"Date de fin de la charge")]]/following-sibling::*/text()').get()
            administrateurs_dict['DATE_FIN'] = self.clean_data(date_fin)
            
            fonctions = fieldset.xpath('.//*[*[contains(text(),"Fonctions actuelles")]]/following-sibling::*/text()').get()
            administrateurs_dict['FONCTIONS'] = self.clean_data(fonctions)
            
            adresse = fieldset.xpath('.//*[*[contains(text(),"Adresse")]]/following-sibling::*/text()').get()
            administrateurs_dict['ADR'] = self.clean_data(adresse)
            
            prenom = fieldset.xpath('.//*[*[contains(text(),"Prénom")]]/following-sibling::*/text()').get()
            administrateurs_dict['PRENOM'] = self.clean_data(prenom)

            administrateurs_list.append(administrateurs_dict)
        item['ADMINISTRATEURS'] = administrateurs_list


        item['COLLECTED_DATE'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        yield item
