import scrapy
 
# importing
from scrapecdr.items import ScrapecdrItem

class HawaiiCDRSpider(scrapy.Spider):
    name = 'Hawaii'
    start_urls = [
        'https://health.hawaii.gov/docd/for-healthcare-providers/reporting-an-illness-for-healthcare-providers/reportable-diseases/'
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        self.logger.info(response)
        for item in response.xpath('//*[@id="tablepress-15"]/tbody/*/td[1]/text()'):
            #self.logger.info(item)
            yield ScrapecdrItem(state=self.name,disease=item.get())