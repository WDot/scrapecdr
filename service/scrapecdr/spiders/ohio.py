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
            #self.logger.info(item)
            if count < 2:
                count += 1
            elif len(item) == 3:
                yield ScrapecdrItem(state=self.name,disease=item[1])