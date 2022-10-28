import scrapy
 
# importing
from scrapecdr.items import ScrapecdrItem

class IndianaCDRSpider(scrapy.Spider):
    name = 'indiana'
    start_urls = [
        'https://www.in.gov/health/erc/infectious-disease-epidemiology/infectious-disease-epidemiology/communicable-disease-reporting/'
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        self.logger.info(response)
        for item in response.xpath('/html/body/div/main/article/section/table/tbody/*/td'):
            yield ScrapecdrItem(state='Indiana',disease=item.get())