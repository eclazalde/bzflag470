class Viterbi:
    #============================================
    # Functions
    #============================================   
    def viterbi(self, observations, d):
        MU = [{}]
        path = {}
        states = d.getTagList()

        for tag in states:
            MU[0][tag] = d.getStart(tag) * d.getEmission(tag, observations[0])
            path[tag] = [tag]
            
        for t in range(1, len(observations)):
            MU.append({})
            newpath = {}
            for tag in states:
                muList = []
                for prevTag in states:
                    mu = d.getEmission(tag, observations[t]) * d.getTransition(prevTag, tag) *  MU[t-1][prevTag]
                    muList.append([mu, prevTag])
                [prob,preTag] = max(muList)
                MU[t][tag] = prob
                newpath[tag] = path[preTag] + [tag]
            path = newpath
        currentT = 0
        if len(observations) != 1:
            currentT = t
        self.saveTable(MU)
        #self.saveTable2(MU)
        vlist = []
        for tag in states:
            value = MU[currentT][tag]
            vlist.append([value, tag])
        [prob, curTag] = max(vlist)
        return [prob, path[curTag]]
    
    def saveTable(self, MU):
        f = open("table.txt","w")
        for obs in range(len(MU)):
            f.write(",{}".format(obs))
        f.write("\n")
        for tag in MU[0]:
            o = tag
            for mu in MU:
                o += ',{}'.format(mu[tag])
            f.write(o + "\n")
        f.close()
        
    def saveTable2(self, MU):
        f = open("Viterbi.csv",'w')
        f.write("\"Tag:\",")
        for col_no in range(len(MU)):
            f.write("\"{:0f}\",".format(col_no))
        f.write("\n")
        for tag in MU[0]:
            output = "\""+tag+"\","
            for tag2 in MU:
                val = tag2[tag]
                if (val == 0):
                    output += "\"---\","
                elif (val < 0.00001): # less than 0.001% probability
                    output += "\"< 0.001 %\","
                else:
                    output += "\"{:.3f} %\",".format(val)
            f.write(output + "\n")
        f.close()
