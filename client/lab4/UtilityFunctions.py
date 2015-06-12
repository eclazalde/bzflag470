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
                    if (self.discardPart(w_parts[1])):
                        continue
                    w_next = w_parts[0]
                    if (w_previous): # skip the first word
                        if w_previous in self._nGramDict:
                            d = self._nGramDict.get(w_previous)
                            d.append(w_next)
                        else:
                            d = list([w_next])
                            self._nGramDict[w_previous] = d  
                    w_previous = w_next
            f.close()
            
    def discardPart(self, tag):
        if tag in ("CC","CD","DT","EX","FW","IN","JJ","JJR","JJS","LS",
                   "MD","NN","NNP","NNPS","NNS","PDT","POS","PRP","PRP$",
                   "RB","RBR","RBS","RP","TO","UH","VB","VBD",
                   "VBG","VBN","VBP","VBZ","WDT","WP","WP$","WRB"): # "SYM" excluded
            return False
        return True
    
                      
    def getNGramDictionary(self):
        ''' Returns the full n-gram dictionary object '''
        return self._nGramDict
    
    def getFilePath(self):
        ''' Returns the path of the file to be / most recently parsed '''
        return self._filepath
           
    def performNGramTest(self, TestFilePath="./testing_dataset.txt"):
        f = open(self._filepath, 'r')
        all_lines = f.readlines()
        f.close()
        r_line = random.choice(all_lines)
        r_line_parts = split(r_line, sep=None)
        i = 0
        actual = ""
        constructed = ""
        previous_word = ""
        word_count = 0.0
        match_success = 0.0
        for w in r_line_parts:
            w_parts = split(w, sep='_')
            if (self.discardPart(w_parts[1])):
                actual += w_parts[0]
                constructed += w_parts[0]
                continue
            actual += (" " + w_parts[0])
            if (word_count > 0):
                try:
                    previous_word = random.choice(self._nGramDict[previous_word])
                except:
                    print "Error: Unable to find any matching n-grams for", previous_word
                    return
                constructed += (" " + previous_word)
                if (previous_word == w_parts[0]):
                    match_success += 1
            else:
                constructed += (" " + w_parts[0])
                previous_word = w_parts[0]
            word_count += 1
                
        #print strip(r_line)
        print "Actual: ", actual
        print "Constructed: ", constructed
        print "Match Success Rate: ", (match_success / word_count)
