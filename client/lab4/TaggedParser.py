from string import *

class TaggedParser:
    
    #============================================
    # Variables
    #============================================
    filepath = None
    sentences = None
    tags = None
    
    #============================================
    # Constructor
    #============================================
    def __init__(self, filepath):
        self.filepath = filepath
        self.sentences = []
        self.tags = []
        
    #============================================
    # Functions
    #============================================
    def parse(self):
        try:
            testingFile = open(self.filepath, 'r')
            for fileLine in testingFile:
                line = []
                tags = []
                fileLineParts = fileLine.split()
                # start over with each new line
                for lineWord in fileLineParts:
                    # get the "word" and tag, if any
                    wordParts = self.getParts(lineWord)
                    if (wordParts == None): # word did not parse correctly
                        continue
                    elif (wordParts['tag'] == None): # no tag provided
                        line.append(wordParts['word'])
                        tags.append('None')
                    else:
                        line.append(wordParts['word'])
                        tags.append(wordParts['tag'])
                self.sentences.append(line)
                self.tags.append(tags)
        finally:
            print "Parsing of", self.filepath,"completed."
            
    def getParts(self, word):
        p = split(word, '_')
        if (len(p) < 2):
            # no tags
            return dict([('word', p[0]), ('tag', None)])
        elif (len(p) == 2):
            # tagged
            return dict([('word', p[0]), ('tag', p[1])])
        else:
            print "Error occurred while splitting >",word,"<"
            return None