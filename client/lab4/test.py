from TaggedParser import TaggedParser
from UntaggedParser import UntaggedParser
from UtilityFunctions import UtilityFunctions
from Viterbi import Viterbi

#============================================
# Test for the tagged parser
#============================================

fileName1 = './small_test.txt'

data1 = TaggedParser(fileName1)

data1.parse()

#for s in range(0, len(data1.sentences)):
#    print data1.sentences[s]
#    print data1.tags[s]

#============================================
# Test for the untagged parser
#============================================
'''
fileName2 = './small_test2.txt'

data2 = UntaggedParser(fileName2)

data2.parse()

for s in data2.sentences:
    print s
'''
#============================================
# Test for the Viterbi class
#============================================
fileName3 = './training_dataset.txt'

data = UtilityFunctions()
vit = Viterbi()

data.doTraining(fileName3)

print 'Sentence to be tagged'
print data1.sentences[0]

result = vit.viterbi(data1.sentences[0], data)

print 'Viterbi result'
print result[1]

print 'Actual Tags'
print data1.tags[0]