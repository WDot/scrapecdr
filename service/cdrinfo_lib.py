from sys import gettrace
import numpy as np
import random
from scipy.special import softmax
import scipy.sparse
import random
import json
import time
import pandas as pd
import requests
import subprocess
from mrconso import MRCONSO
import logging
#from vdxmapper import VisualDxConcepts
#import editdistance

class CDRInfo:
    def __init__(self):
    
        self.mrconso = MRCONSO(['SNOMEDCT_US'])
        self.stateData = json.load(open('communicable_disease_reporting.json'))
        for state in self.stateData:
            for item in self.stateData[state]:
                jsonData = self.getTreatmentMetamapJson(item['disease'])
                cur_cuis, cur_cuinames = self.JsonToCuis(jsonData)
                cuiMapping = self.mrconso.CuisToMRCONSO(cur_cuis)
                logging.info(cuiMapping)
                


    def getTreatmentMetamapJson(self,text):
    
        command = "echo \"{0}\" | ./public_mm/bin/metamap20 --JSONn -R SNOMEDCT_US".format(text)
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=None,
            shell=True)
        
        output = (proc.communicate())[0].decode('utf-8')

        #ps = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=None)
        #output = ps.communicate()[0].decode('utf-8')
        #print(output)
        jsonoutput = output.split("--lexicon db -Z 2020AA --JSONn -R SNOMEDCT_US\n")[1]
        #return jsonoutput
        return json.loads(jsonoutput)
    
    def JsonToCuis(self,jsonVal):
        #print(json)
        documents = jsonVal['AllDocuments']
        cuis = []
        cpreferred = []
        for i in range(len(documents)):
            utterances = documents[i]['Document']['Utterances']
            for j in range(len(utterances)):
                phrases = utterances[j]['Phrases']
                for k in range(len(phrases)):
                    subcuis = []
                    subcpreferred = []
                    mappings = phrases[k]['Mappings']
                    for l in range(len(mappings)):
                        candidates = mappings[l]['MappingCandidates']
                        for candidate in candidates:
                            #print('{0} {1} {2} {3}'.format(i,j,candidate['CandidateCUI'],candidate['Negated']))
                            if int(candidate['Negated']) > 0:
                                subcuis.append('-' + candidate['CandidateCUI'])
                                subcpreferred.append(candidate['CandidatePreferred'])
                                #print('Negation!')
                            else:
                                subcuis.append(candidate['CandidateCUI'])
                                subcpreferred.append(candidate['CandidatePreferred'])
                    #cuis.extend(list(set(subcuis)))
                    #cpreferred.extend(list(set(subcpreferred)))
                    cuis.extend(subcuis)
                    cpreferred.extend(subcpreferred)

        return (cuis,cpreferred)

    '''
    def autocomplete(self,searchVal,K):
        distances = []
        for key in self.terms:
            distances.append(editdistance.eval(searchVal.lower(),key.lower()))
            #print(distances)
        distances = np.array(distances)
        #print(distances.shape)
        min_distances = np.argpartition(distances,K)
        best_keys = sorted([self.terms[i] for i in sorted(min_distances[:K])])
        return best_keys
    '''
        
if __name__ == "__main__":
    drugInfo = CDRInfo()