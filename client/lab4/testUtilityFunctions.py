from UtilityFunctions import UtilityFunctions
import time

uf = UtilityFunctions()
#start = time.time()
#uf.loadFile(getTags=False)
#print uf.getNGramDictionary()
#uf.calculateNGramProbabilities()
#print uf.getNGramDictionary()
#print (time.time() - start), "second(s) to load", uf.getFilePath()

#start = time.time()
uf.setFilePath("./training_dataset.txt")
uf.loadFile(getTags=False)
#uf.calculateNGramProbabilities()
#print (time.time() - start), "second(s) to load", uf.getFilePath()

#start = time.time()
#uf.optimizeNGramDictionary()
#print (time.time() - start), "second(s) to optimize", uf.getFilePath()

uf.performNGramTest(TestFilePath="./training_dataset.txt")
uf.performNGramTest(TestFilePath="./testing_dataset.txt")