from string import *
from numpy import random

class UtilityFunctions:
    
    _filepath = None
    _nGramDict = None
    
    def __init__(self, FilePath="./training_dataset_small.txt"):
        self._filepath = FilePath
        self._nGramDict = dict()
    
    def setFilePath(self, FilePath):
        ''' Set the path of the file to parse '''
        self._filepath = FilePath
    
    def loadFile(self, getTags=False):
        ''' Loads the file into memory and builds an n-gram dictionary '''
        if (getTags):
            print "NOT YET IMPLEMENTED"
            return
        else:
            self._nGramDict = dict()
            f = open(self._filepath, 'r')
            for f_line in f:
                f_line_parts = split(f_line, sep=None)
                w_previous = None
                for w in f_line_parts:
                    w_parts = split(w, sep='_')
                    w_next = w_parts[0]
                    if (w_previous): # skip the first word
                        if w_previous in self._nGramDict:
                            d = self._nGramDict.get(w_previous)
                            v = 0 # number of occurrences
                            if w_next in d:
                                v = d.get(w_next)
                            v += 1
                            d[w_next] = v
                        else:
                            d = dict([(w_next, 1)])
                            self._nGramDict[w_previous] = d  
                    w_previous = w_next  
                      
    def getNGramDictionary(self):
        ''' Returns the full n-gram dictionary object '''
        return self._nGramDict
    
    def getFilePath(self):
        ''' Returns the path of the file to be / most recently parsed '''
        return self._filepath
        
    def calculateNGramProbabilities(self):
        ''' Convert the n-gram word counts to probabilities '''
        for k in self._nGramDict:
            v = self._nGramDict[k]
            t = 0.0 # total word count
            for w_k, w_v in v.iteritems():
                t += w_v
            for w_k, w_v in v.iteritems():
                v[w_k] = w_v / t
    
    def optimizeNGramDictionary(self):
        ''' Build an optimized n-gram dictionary with only the highest-probability words. '''
        optimized = dict()
        for k in self._nGramDict:
            v = self._nGramDict[k]
            max = 0
            max_v = ""
            for w_k, w_v in v.iteritems():
                if (w_v > max):
                    max = w_v
                    max_v = w_k
                elif (w_v == max):
                    if (random.random() < 0.5):
                        max_v = w_k
            optimized[k] = max_v
        return optimized
