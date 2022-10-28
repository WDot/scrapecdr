# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import re
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import bleach

class ScrapecdrPipeline:
    def open_spider(self, spider):
        self.diseaseDict = {}

    def close_spider(self, spider):
        for key in self.diseaseDict:
            self.diseaseDict[key] = list(set(self.diseaseDict[key]))
        json.dump(self.diseaseDict,open('communicable_disease_reporting.json','w'),indent=True)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if ('state' in adapter) and ('disease' in adapter):
            diseaseVal = bleach.clean(adapter['disease'],strip=True,strip_comments=True,tags=[],attributes={}, styles=[])
            diseaseVal = diseaseVal.replace('!','')
            diseaseVal = diseaseVal.replace('*','')
            diseaseVal = diseaseVal.strip()
            if adapter['state'] in self.diseaseDict:
                self.diseaseDict[adapter['state']].append(diseaseVal)
            else:
                self.diseaseDict[adapter['state']] = [diseaseVal]
