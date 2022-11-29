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
import editdistance

class CDRInfo:
    def __init__(self):
    
        self.mrconso = MRCONSO(['SNOMEDCT_US'])
        self.stateData = json.load(open('communicable_disease_reporting.json'))
        for state in self.stateData:
            for i in range(len(self.stateData[state])):
                diseaseName = self.stateData[state][i]['disease'].encode(encoding='ascii',errors='ignore').decode('ascii')
                jsonData = self.getTreatmentMetamapJson(diseaseName)
                cur_cuis, cur_cuinames = self.JsonToCuis(jsonData)
                cuiMapping = self.mrconso.CuisToMRCONSO(cur_cuis)
                #conceptIdVals,conceptIdNames,snomeds,confidences = self.vdxmapper.getConceptIds(cuiMapping,0.9)
                #if len(confidences) > 0:
                #    maxind = np.argmax(confidences)
                #    self.stateData[state][i]['snomed'] = snomeds[maxind]
                #    self.stateData[state][i]['vdxconcept'] = conceptIdVals[maxind]
                #    self.stateData[state][i]['vdxname'] = conceptIdNames[maxind]
                minDistance = 100000
                minSnomed = None
                minSnomedName = None
                for key in cuiMapping:
                    for mapCode,mapStr in cuiMapping[key]:
                        curDistance = editdistance.eval(diseaseName,mapStr)
                        if curDistance < minDistance:
                            minDistance = curDistance
                            minSnomed = mapCode
                            minSnomedName = mapStr
                self.stateData[state][i]['snomed'] = minSnomed
                self.stateData[state][i]['snomedname'] = minSnomedName

                logging.info(self.stateData[state][i])                


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