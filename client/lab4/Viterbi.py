class Viterbi:
    
    #============================================
    # Variables
    #============================================
    
    
    #============================================
    # Constructor
    #============================================
    def __init__(self):
        pass
        
    #============================================
    # Functions
    #============================================   
    def viterbi(self, observations, d):
        V = [{}]
        path = {}
        states = d.getTagList()
        
        # Initialize base cases (t == 0)
        for y in states:
            V[0][y] = d.getStart(y) * d.getEmission(y, observations[0])
            path[y] = [y]
     
        # Run Viterbi for t > 0
        for t in range(1, len(observations)):
            V.append({})
            newpath = {}
            for y in states:
                vlist = []
                for y0 in states:
                    calc = V[t-1][y0] * d.getTransition(y0, y) * d.getEmission(y, observations[t])
                    vlist.append([calc, y0])
                (prob,state) = max(vlist)
                V[t][y] = prob
                newpath[y] = path[state] + [y]
     
            # Don't need to remember the old paths
            path = newpath
        n = 0           # if only one element is observed max is sought in the initialization values
        if len(observations) != 1:
            n = t
        self.saveTable(V)
        vlist = []
        for y in states:
            value = V[n][y]
            vlist.append([value, y])
        (prob, state) = max(vlist)
        return (prob, path[state])
    
    def saveTable(self, V):
        f = open("table.txt","w")
        #s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
        for i in range(len(V)):
            f.write(",{}".format(i))
        f.write("\n")
        for y in V[0]:
            #s += "%.5s: " % y
            o = y
            #s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
            for v in V:
                o += ',{}'.format(v[y])
            f.write(o + "\n")
            #s += "\n"
        #print(s)
        f.close()