from string import *
from numpy import random

class UtilityFunctions:
    
    #===========================================================================
    # _filepath = None
    #===========================================================================
    _nGramDictionary = None
    _tagList = None
    _startingProbabilities = None
    _startingTotal = 0.0
    _transitionProbabilities = None
    _emissionProbabilities = None
    
    def __init__(self):
        self.reset()
    
    #===========================================================================
    # def setFilePath(self, FilePath):
    #     ''' Set the path of the file to parse '''
    #     self._filepath = FilePath
    #===========================================================================
    
    def reset(self):
        self._nGramDictionary = dict()
        self._tagList = dict()
        self._startingProbabilities = dict()
        self._startingTotal = 0.0
        self._transitionProbabilities = dict()
        self._emissionProbabilities = dict()
        
    def getParts(self, word):
        p = split(word, '_')
        if (len(p) < 2):
            # no tags
            return dict([('word', p[0]), ('tag', None)])
        elif (len(p) == 2):
            # tagged
            self.updateTagList(p[1])
            return dict([('word', p[0]), ('tag', p[1])])
        else:
            print "Error occurred while splitting >",word,"<"
            return None
    
    def updateTagList(self, tag):
        e = self._tagList.get(tag, 0)
        self._tagList[tag] = (e + 1)
        
    def getTagList(self):
        return self._tagList.keys()
        
    def addNGramWord(self, word_prev, word_next):
        e = self._nGramDictionary.get(word_prev) #(word_prev)
        if (e):
            e.append(word_next)
        else:
            e = [word_next]
        self._nGramDictionary[word_prev] = e
        
    def addStart(self, tag_start):
        e = self._startingProbabilities.get(tag_start, 0)
        self._startingProbabilities[tag_start] = (e + 1.0)
        self._startingTotal += 1.0
        return
    
    def getStart(self, tag_start):
        return (self._startingProbabilities.get(tag_start, 0.0) / self._startingTotal)
    
    def addTransition(self, tag_prev, tag_next):
        e = self._transitionProbabilities.get(tag_prev)
        if (e):
            # list of two items: (total_count, dict([(tag, tag_count)])
            total_count = (e[0] + 1.0)
            d = e[1]
            g = d.get(tag_next, 0.0)
            d[tag_next] = (g + 1.0)
            self._transitionProbabilities[tag_prev] = [total_count, d]
        else:
            self._transitionProbabilities[tag_prev] = [1.0, dict([(tag_next, 1.0)])]
        return
        
    def getTransition(self, tag_prev, tag_next):
        e = self._transitionProbabilities.get(tag_prev)
        if (e):
            f = e[1].get(tag_next, 0.0)
            return (f / e[0])
        return 0.0
        
    def addEmission(self, tag, word):
        e = self._emissionProbabilities.get(tag)
        if (e):
            # list of two items: (total_count, dict([(word, word_count)])
            total_count = (e[0] + 1.0)
            d = e[1]
            g = d.get(word, 0.0)
            d[word] = (g + 1.0)
            self._emissionProbabilities[tag] = [total_count, d]
        else:
            self._emissionProbabilities[tag] = [1.0, dict([(word, 1.0)])]
        return
        
    def getEmission(self, tag, word):
        e = self._emissionProbabilities.get(tag)
        if (e):
            f = e[1].get(word, 0.0)
            return (f / e[0])
        return 0.0
        
    def doTraining(self, FilePath):
        ''' New training function for both n-gram and Markov capabilities '''
        try:
            training_file = open(FilePath, 'r')
            for file_line in training_file:
                file_line_parts = file_line.split()
                # start over with each new line
                prev_word = None
                prev_tag = None
                for line_word in file_line_parts:
                    # get the "word" and tag, if any
                    word_parts = self.getParts(line_word)
                    if (word_parts == None): # word did not parse correctly
                        continue
                    if (word_parts['tag'] == None): # no tag provided
                        if (prev_word):
                            # not the first word in the sentence
                            self.addNGramWord(prev_word, word_parts['word'])
                        prev_word = word_parts['word']    
                    else: # we have a tag
                        if (prev_word):
                            # not the first word in the sentence
                            self.addNGramWord(prev_word, word_parts['word'])
                        prev_word = word_parts['word']
                        if (prev_tag):
                            # update the transition probabilities
                            self.addTransition(prev_tag, word_parts['tag'])
                        else:
                            # update the starting probabilities
                            self.addStart(word_parts['tag'])
                        prev_tag = word_parts['tag']
                        # update the emission probabilities
                        self.addEmission(word_parts['tag'], word_parts['word'])
        finally:
            print "Training of", FilePath,"completed."
    
    #===========================================================================
    # def loadFile(self, getTags=False):
    #     ''' Loads the file into memory and builds an n-gram dictionary '''
    #     if (getTags):
    #         print "NOT YET IMPLEMENTED"
    #         return
    #     else:
    #         self._nGramDict = dict()
    #         f = open(self._filepath, 'r')
    #         for f_line in f:
    #             f_line_parts = split(f_line, sep=None)
    #             w_previous = None
    #             for w in f_line_parts:
    #                 w_parts = split(w, sep='_')
    #                 if (self.discardPart(w_parts[1])):
    #                     continue
    #                 w_next = w_parts[0]
    #                 if (w_previous): # skip the first word
    #                     if w_previous in self._nGramDict:
    #                         d = self._nGramDict.get(w_previous)
    #                         d.append(w_next)
    #                     else:
    #                         d = list([w_next])
    #                         self._nGramDict[w_previous] = d  
    #                 w_previous = w_next
    #         f.close()
    #===========================================================================
            
    #===========================================================================
    # def discardPart(self, tag):
    #     if tag in ("CC","CD","DT","EX","FW","IN","JJ","JJR","JJS","LS",
    #                "MD","NN","NNP","NNPS","NNS","PDT","POS","PRP","PRP$",
    #                "RB","RBR","RBS","RP","TO","UH","VB","VBD",
    #                "VBG","VBN","VBP","VBZ","WDT","WP","WP$","WRB"): # "SYM" excluded
    #         return False
    #     return True
    #===========================================================================
                      
    #===========================================================================
    # def getNGramDictionary(self):
    #     ''' Returns the full n-gram dictionary object '''
    #     return self._nGramDictionary
    #===========================================================================
    
    #===========================================================================
    # def getFilePath(self):
    #     ''' Returns the path of the file to be / most recently parsed '''
    #     return self._filepath
    #===========================================================================
           
    #===========================================================================
    # def performNGramTest(self, TestFilePath="./testing_dataset.txt"):
    #     f = open(self._filepath, 'r')
    #     all_lines = f.readlines()
    #     f.close()
    #     r_line = random.choice(all_lines)
    #     r_line_parts = split(r_line, sep=None)
    #     i = 0
    #     actual = ""
    #     constructed = ""
    #     previous_word = ""
    #     word_count = 0.0
    #     match_success = 0.0
    #     for w in r_line_parts:
    #         w_parts = split(w, sep='_')
    #         if (self.discardPart(w_parts[1])):
    #             actual += w_parts[0]
    #             constructed += w_parts[0]
    #             continue
    #         actual += (" " + w_parts[0])
    #         if (word_count > 0):
    #             try:
    #                 previous_word = random.choice(self._nGramDict[previous_word])
    #             except:
    #                 print "Error: Unable to find any matching n-grams for", previous_word
    #                 return
    #             constructed += (" " + previous_word)
    #             if (previous_word == w_parts[0]):
    #                 match_success += 1
    #         else:
    #             constructed += (" " + w_parts[0])
    #             previous_word = w_parts[0]
    #         word_count += 1
    #             
    #     #print strip(r_line)
    #     print "Actual: ", actual
    #     print "Constructed: ", constructed
    #     print "Match Success Rate: ", (match_success / word_count)
    #===========================================================================
