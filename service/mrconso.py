import numpy as np
import pandas as pd
from itertools import groupby
import re

class MRCONSO:
    def __init__(self,sabs):
        COL_NAMES = ['CUI',
                     'LAT',
                     'TS',
                     'LUI',
                     'STT',
                     'SUI',
                     'ISPREF',
                     'AUI',
                     'SAUI',
                     'SCUI',
                     'SDUI',
                     'SAB',
                     'TTY',
                     'CODE',
                     'STR',
                     'SRL',
                     'SUPPRESS',
                     'CVF']
        self.mrconso = pd.read_csv('MRCONSO.RRF',delimiter='|',names=COL_NAMES,dtype=str,index_col=False)
        self.sabs = sabs
        self.codeDict = {}
        #data = np.load('mrconsovectors20220706.npz')
        #strings = data['s']
        #vectors = data['v'].astype(np.float32)
        #self.vectorDict = {}
        #for i in range(len(strings)):
        #    self.vectorDict[strings[i]] = vectors[i,:]
        failures = 0
        for sab in sabs:
            curCuis = self.mrconso.loc[(self.mrconso['SAB'] == sab) &
                                   (self.mrconso['LAT'] == 'ENG')]
            self.codeDict[sab] = {}
            for i in range(curCuis.shape[0]):
                try:
                    curStr = re.sub('\([\w\d\-\. ]+\)','',str(curCuis['STR'].iloc[i]))
                    if curCuis['CUI'].iloc[i] in self.codeDict[sab]:
                        self.codeDict[sab][curCuis['CUI'].iloc[i]].append((curCuis['CODE'].iloc[i],
                                                                           curStr))
                                                                           #self.vectorDict[curStr]))
                    else:
                        self.codeDict[sab][curCuis['CUI'].iloc[i]]= [(curCuis['CODE'].iloc[i],
                                                                      curStr)]
                                                                      #self.vectorDict[curStr])]
                except KeyError:
                    failures += 1
                    print(failures)
        
    def getcode(self,cui,sab):
        try:
            return self.codeDict[sab][cui]
        except:
            return []

    def CuisToMRCONSO(self,cuis):
        cuiMappings = {}
        for cui in cuis:
            cuiMappings[cui] = []
            for code in self.sabs:
                cuiMappings[cui].extend(self.getcode(cui,code))
            cuiMappings[cui] = [next(g) for _, g in groupby(cuiMappings[cui], key=lambda x:x[1])]
            #cuiMappings[cui] = list(set(cuiMappings[cui]))
        return cuiMappings