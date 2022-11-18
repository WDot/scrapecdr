import scrapy
 
# importing
from scrapecdr.items import ScrapecdrItem
import bleach

class HawaiiCDRSpider(scrapy.Spider):
    name = 'Hawaii'
    start_urls = [
        'https://health.hawaii.gov/docd/for-healthcare-providers/reporting-an-illness-for-healthcare-providers/reportable-diseases/'
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        self.logger.info(response)
        count = -1
        for item in response.xpath('//*[@id="tablepress-15"]/tbody/*/td'):
            self.logger.info(item.get())
            count += 1
            if count % 3 == 0:
                diseaseVal = item.get()
                diseaseVal = bleach.clean(diseaseVal,strip=True,strip_comments=True,tags=[],attributes={}, css_sanitizer=[])
                diseaseVal = diseaseVal.strip()
            elif count % 3 == 1:
                urgency = item.get()
                urgency = bleach.clean(urgency,strip=True,strip_comments=True,tags=[],attributes={}, css_sanitizer=[])
                urgency = urgency.strip()
                contactTiming = 'Unknown'
                if urgency == 'Urgent':
                    contactTiming = 'Call Immediately, then Mail/Fax a Report within 3 Days'
                elif urgency == 'Routine':
                    contactTiming = 'When convenient'
                elif urgency == 'Routine/Enteric':
                    contactTiming = 'Call immediately if the individual case is a foodhandler, direct care provider, or pre-school aged child'
                elif urgency == 'Confidential':
                    contactTiming = 'Report by phone or mail within 3 Days'
                elif urgency == 'Upon Request':
                    contactTiming = 'Report upon Request'
                else:
                    self.logger.info('Urgency {0}'.format(urgency))
            elif count % 3 == 2:
                interestedParty = item.get()
                interestedParty = bleach.clean(interestedParty,strip=True,strip_comments=True,tags=[],attributes={}, css_sanitizer=[])
                interestedParty = interestedParty.strip()
                contactMethod = 'Unknown'
                if interestedParty == 'Disease Investigation Branch':
                    contactMethod = {'contactMethods':[{'locale': 'O\'ahu','Phone': '(808) 586-4586','Fax': '(808) 586-4595','After-Hours Phone': '1-800-360-2575'},
                                     {'locale': 'Hawai\'i','Phone': '(808) 933-0912','Fax': '(808) 933-0400'},
                                     {'locale': 'Kaua\'i','Phone': '(808) 241-3563','Fax': '(808) 241-3480'},
                                     {'locale': 'Maui','Phone': '(808) 984-8213','Fax': '(808) 243-5141','After-Hours Phone': '1-800-360-2575'}
                                    ]}
                elif interestedParty == 'Tuberculosis Control Program':
                    contactMethod = {'Phone': '(808) 832-3534','Fax': '(808) 832-5624','Address': '1700 Lanakila Avenue, Ground Floor, Honolulu, HI 96817, Attn: Registry - Confidential'}
                elif interestedParty == 'STD Prevention Program':
                    contactMethod = {'Phone': '(808) 733-9281','Fax': '(808) 733-9291','Address': '3627 Kilauea Avenue, Room 304, Honolulu, HI 96816'}
                elif interestedParty == 'HIV/AIDS Surveillance Program':
                    contactMethod = {'Phone': '(808) 733-4079','Address': '3627 Kilauea Avenue, Room 306, Honolulu, HI 96816'}
                elif interestedParty == 'Hansen\'s Disease Community Program':
                    contactMethod = {'Phone': '(808) 733-9831','Fax': '(808) 733-9836','Address': '3627 Kilauea Avenue Room 102, Honolulu, HI 96816'}
                else:
                    self.logger.info('Interested Party {0}'.format(interestedParty))
                if len(diseaseVal) > 0:
                    yield ScrapecdrItem(state=self.name,disease=diseaseVal,contactTiming=contactTiming,contactMethod=contactMethod)
            
            