import scrapy
import json
# importing
from scrapecdr.items import ScrapecdrItem

#This one is tricky: The tabular data is stored in a JSON blob in the HTML, then rendered with Javascript
class OhioCDRSpider(scrapy.Spider):
    name = 'Ohio'
    start_urls = [
        'https://odh.ohio.gov/know-our-programs/infectious-disease-control-manual/section3'
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        self.logger.info(response)
        jsonText = json.loads(response.xpath('//*[@id="js-placeholder-json-data"]/text()')[0].get())
        count = 0
        for item in jsonText['data']:
            self.logger.info(item)
            if count < 2:
                count += 1
            elif len(item) >= 4:
                if item[3] == 'A':
                    contactTiming = 'Immediately'
                    contactMethod = 'Local Health Department Phone'
                else:
                    contactTiming = 'By the End of Next Business Day'
                    contactMethod = 'https://odh.ohio.gov/wps/wcm/connect/gov/8a5539e9-f823-480d-a2c7-a30e80c33d62/form-confidential-reportable-disease.pdf?MOD=AJPERES&CONVERT_TO=url&CACHEID=ROOTWORKSPACE.Z18_K9I401S01H7F40QBNJU3SO1F56-8a5539e9-f823-480d-a2c7-a30e80c33d62-mR0PC0i'
                yield ScrapecdrItem(state=self.name,disease=item[2],contactTiming=contactTiming,contactMethod=contactMethod)