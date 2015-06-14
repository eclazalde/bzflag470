from UtilityFunctions import UtilityFunctions
import time

uf = UtilityFunctions()
uf.doTraining("./training_dataset.txt")
print uf.getTagList()
#===============================================================================
# l = uf.getTagList()
# t = 0
# for tag in l:
#     p = uf.getStart(tag)
#     t += p
#     print tag, p, t
#===============================================================================