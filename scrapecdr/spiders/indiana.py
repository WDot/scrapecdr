import scrapy
 
# importing
from scrapecdr.items import ScrapecdrItem
import bleach

class IndianaCDRSpider(scrapy.Spider):
    name = 'Indiana'
    start_urls = [
        'https://www.in.gov/health/erc/infectious-disease-epidemiology/infectious-disease-epidemiology/communicable-disease-reporting/'
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        self.logger.info(response)
        for item in response.xpath('//*[@id="content_container_373681"]/table/tbody/*/td'):
            diseaseVal = item.get()
            diseaseVal = bleach.clean(diseaseVal,strip=True,strip_comments=True,tags=[],attributes={}, styles=[])
            diseaseVal = diseaseVal.lower()
            #Default
            contactTiming = 'Within 72 hours'
            contactMethod = 'https://forms.in.gov/Download.aspx?id=5082'
            if '!' in diseaseVal:
                contactTiming = 'Immediate'
                contactMethod = '317-233-7125 (8:15 am – 4:45 pm EST) or 317-233-1325 (after hours, weekends, holidays)'
                diseaseVal = diseaseVal.replace('!','')
            elif '*' in diseaseVal:
                contactTiming = 'Within 24 hours'
                diseaseVal = diseaseVal.replace('*','')
            if ('tuberculosis' in diseaseVal):
                contactMethod = 'https://www.in.gov/health/tuberculosis/information-for-health-professionals/tb-reporting-forms/'
            elif ('chlamydia' in diseaseVal) or \
            ('syphilis' in diseaseVal) or \
            ('hiv' in diseaseVal) or \
            ('aids' in diseaseVal):
                contactMethod = 'https://www.in.gov/health/hiv-std-viral-hepatitis/forms/'
            diseaseVal = diseaseVal.strip()
            if len(diseaseVal) > 0:
                yield ScrapecdrItem(state=self.name,disease=diseaseVal,contactTiming=contactTiming,contactMethod=contactMethod)