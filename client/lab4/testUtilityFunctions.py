from UtilityFunctions import UtilityFunctions
import time

uf = UtilityFunctions()
uf.doTraining("./training_dataset.txt")
print uf.getTagList()

uf.performNGramTest(TestFilePath="./testing_dataset.txt", numberOfTests=100, verbose=False)
#===============================================================================
# l = uf.getTagList()
# t = 0
# for tag in l:
#     p = uf.getStart(tag)
#     t += p
#     print tag, p, t
#===============================================================================

#===============================================================================
# l1 = uf.getTagList()
# l2 = uf.getTagList()
# 
# for t1 in l1:
#     for t2 in l2:
#         print t1,"->",t2,"=",uf.getTransition(t1, t2)
#===============================================================================

#===============================================================================
# l = uf.getTagList()
# o = ['this', 'is', 'a', 'rather', 'boring', 'sentence']
# for tag in l:
#     for word in o:
#         print tag,"->",word,"=",uf.getEmission(tag, word)
#===============================================================================