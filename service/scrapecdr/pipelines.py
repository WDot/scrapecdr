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
        #for key in self.diseaseDict:
        #    self.diseaseDict[key] = list(set(self.diseaseDict[key]))
        json.dump(self.diseaseDict,open(self.OUT_FILE,'w'),indent=True)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if ('state' in adapter) and ('disease' in adapter):
            disease = adapter['disease']
            disease = disease.replace('μ','micro') #annoying hack due to uri encoding
            diseaseDict = {'disease' : disease}
            if ('contactMethod' in adapter):
                diseaseDict['contactMethod'] = adapter['contactMethod']
            if('contactTiming' in adapter):
                diseaseDict['contactTiming'] = adapter['contactTiming']
            if adapter['state'] in self.diseaseDict:
                self.diseaseDict[adapter['state']].append(diseaseDict)
            else:
                self.diseaseDict[adapter['state']] = [diseaseDict]
