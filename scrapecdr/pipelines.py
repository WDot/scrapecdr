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
import os
import os.path
from datetime import datetime as dt
class ScrapecdrPipeline:
    def __init__(self):
        self.OUT_FILE = 'communicable_disease_reporting.json'
    def open_spider(self, spider):
        if os.path.exists(self.OUT_FILE):
            self.diseaseDict = json.load(open(self.OUT_FILE,'r'))
            #backup just in case
            json.dump(self.diseaseDict,open(self.OUT_FILE + str(dt.now()),'w'))
            #clear current state's list
            self.diseaseDict[spider.name] = []
        else:
            self.diseaseDict = {}

    def close_spider(self, spider):
        for key in self.diseaseDict:
            self.diseaseDict[key] = list(set(self.diseaseDict[key]))
        json.dump(self.diseaseDict,open(self.OUT_FILE,'w'),indent=True)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if ('state' in adapter) and ('disease' in adapter):
            diseaseVal = bleach.clean(adapter['disease'],strip=True,strip_comments=True,tags=[],attributes={}, styles=[])
            diseaseVal = diseaseVal.replace('!','')
            diseaseVal = diseaseVal.replace('*','')
            diseaseVal = diseaseVal.strip()
            if len(diseaseVal) > 0:
                if adapter['state'] in self.diseaseDict:
                    self.diseaseDict[adapter['state']].append(diseaseVal)
                else:
                    self.diseaseDict[adapter['state']] = [diseaseVal]
