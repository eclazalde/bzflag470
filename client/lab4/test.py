from TaggedParser import TaggedParser
from UntaggedParser import UntaggedParser
from UtilityFunctions import UtilityFunctions
from Viterbi import Viterbi
import math

#============================================
# Test for the tagged parser
#============================================

fileName1 = './testing_dataset.txt'

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
# Test functions
#============================================
def compare(gen, act):
    correct = 0.0
    count = 0
    for s in gen:
        if s == act[count]:
            correct += 1
        count += 1
    return correct / len(gen)
#============================================
# Test for the Viterbi class
#============================================
fileName3 = './training_dataset.txt'

data = UtilityFunctions()
vit = Viterbi()

data.doTraining(fileName3)
print "Tagging..."
fi = open("tagquality.txt", 'w')
op = open("moreninty.txt", 'w')
te = open("lessfifty.txt", 'w')
count = 0
average = 0
print len(data1.sentences)
for f in data1.sentences:
    result = vit.viterbi(f, data)
    #print result[1]
    #print data1.tags[count]
    percent =  compare(result[1], data1.tags[count])
    fi.write('{},{}\n'.format(count, percent))
    if percent > 0.9:
        op.write('{}~{}~{}~{}\n'.format(percent, f,result[1], data1.tags[count]))
    if percent < 0.5:
        te.write('{}~{}~{}~{}\n'.format(percent, f,result[1], data1.tags[count]))
    #print percent
    #if count > 0 and count % 100 == 0:
    #    print average / count
    average += percent
    count += 1
#print average / len(data1.sentences)

fi.close()
op.close()
te.close()
print "Tagging completed."
#print 'Sentence to be tagged'
#print data1.sentences[0]
#
#result = vit.viterbi(data1.sentences[0], data)
#
#print 'Viterbi result'
#print result[1]
#
#print 'Actual Tags'
#print data1.tags[0]