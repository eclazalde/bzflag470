from UtilityFunctions import UtilityFunctions
import time

uf = UtilityFunctions()
start = time.time()
uf.loadFile()
#print uf.getNGramDictionary()
uf.calculateNGramProbabilities()
#print uf.getNGramDictionary()
print (time.time() - start), "second(s) to load", uf.getFilePath()

start = time.time()
uf.setFilePath("./training_dataset.txt")
uf.loadFile()
#print uf.getNGramDictionary()
uf.calculateNGramProbabilities()
#print uf.getNGramDictionary()
print (time.time() - start), "second(s) to load", uf.getFilePath()

print uf.optimizeNGramDictionary()