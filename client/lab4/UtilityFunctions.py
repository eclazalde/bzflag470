from string import *

class UtilityFunctions:
    
    _filepath = None
    _nGramDict = None
    
    def __init__(self, FilePath="./training_dataset.txt"):
        self._filepath = FilePath
        self._nGramDict = dict()
        
    def loadFile(self):
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
        return self._nGramDict
        
