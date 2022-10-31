import scrapy
 
# importing
from scrapecdr.items import ScrapecdrItem

class IndianaCDRSpider(scrapy.Spider):
    name = 'Indiana'
    start_urls = [
        'https://www.in.gov/health/erc/infectious-disease-epidemiology/infectious-disease-epidemiology/communicable-disease-reporting/'
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        self.logger.info(response)
        for item in response.xpath('//*[@id="content_container_373681"]/table/tbody/*/td'):
            yield ScrapecdrItem(state=self.name,disease=item.get())