from string import *

class UntaggedParser:
    
    #============================================
    # Variables
    #============================================
    filepath = None
    sentences = None
    endingPunctuation = None
    
    #============================================
    # Constructor
    #============================================
    def __init__(self, filepath):
        self.filepath = filepath
        self.sentences = []
        self.endingPunctuation = ['.', '?','!',':',';']
        
    #============================================
    # Functions
    #============================================
    def parse(self):
        try:
            testingFile = open(self.filepath, 'r')
            for fileLine in testingFile:
                line = []
                fileLineParts = fileLine.split()
                for t in fileLineParts:
                    if t in self.endingPunctuation:
                        line.append(t)
                        if len(line) > 0:
                            self.sentences.append(line)
                        line = []
                    else:
                        line.append(t)
                if len(line) > 0:
                    self.sentences.append(line)
        finally:
            print "Parsing of", self.filepath,"completed."