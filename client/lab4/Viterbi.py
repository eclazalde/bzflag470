states = ('NN', 'JJS', 'VB', '.') # nouns, adjective, verb, period
 
#observations = ('home', 'tree', 'person', 'run', 'buy', 'sleep', 'big', 'wet', 'slow', '.')
observations = ('person', 'run', 'big', 'wet', 'home', '.') #This would be the input sentence to be tagged

start_probability = {'NN': 0.5, 'JJS': 0.3, 'VB': 0.2, '.': 0.0} # I'm guessing this is the probability that the first would is a given tag

transition_probability = {
   'NN' : {'NN': 0.0, 'JJS': 0.1, 'VB': 0.6, '.': 0.3},
   'JJS' : {'NN': 0.8, 'JJS': 0.2, 'VB': 0.0, '.': 0.0},
   'VB' : {'NN': 0.7, 'JJS': 0.2, 'VB': 0.0, '.': 0.1},
   '.' : {'NN': 0.7, 'JJS': 0.2, 'VB': 0.1, '.': 0.0},
   }

emission_probability = {
   'NN' : {'home': 0.3, 'tree': 0.5, 'person': 0.2, 'run': 0.0, 'buy': 0.0, 'sleep': 0.0, 'big': 0.0, 'wet': 0.0, 'slow': 0.0, '.': 0.0},
   'JJS' : {'home': 0.0, 'tree': 0.0, 'person': 0.0, 'run': 0.0, 'buy': 0.0, 'sleep': 0.0, 'big': .4, 'wet': .2, 'slow': .4, '.': 0.0},
   'VB' : {'home': 0.0, 'tree': 0.0, 'person': 0.0, 'run': 0.3, 'buy': 0.4, 'sleep': 0.3, 'big': 0.0, 'wet': 0.0, 'slow': 0.0, '.': 0.0},
   '.' : {'home': 0.0, 'tree': 0.0, 'person': 0.0, 'run': 0.0, 'buy': 0.00, 'sleep': 0.0, 'big': 0.0, 'wet': 0.0, 'slow': 0.0, '.': 1.0}
   }

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
 
    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
 
    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
 
        for y in states:
            (prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
            V[t][y] = prob
            newpath[y] = path[state] + [y]
 
        # Don't need to remember the old paths
        path = newpath
    n = 0           # if only one element is observed max is sought in the initialization values
    if len(obs) != 1:
        n = t
    print_dptable(V)
    word = ""
    for w in observations:
        word += " " + w
    print word
    (prob, state) = max((V[n][y], y) for y in states)
    return (prob, path[state])
 
# Don't study this, it just prints a table of the steps.
def print_dptable(V):
    f = open("table.txt","w")
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for i in range(len(V)):
        f.write(",{}".format(i))
    f.write("\n")
    #f.write(",".join(("%3d" % i) for i in range(len(V))) + "\n")
    for y in V[0]:
        s += "%.5s: " % y
        o = y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        for v in V:
            o += ',{}'.format(v[y])#",%.7s" % ("%f" % v[y])
        f.write(o + "\n")
        s += "\n"
    print(s)
    f.close()
    
def example():
    return viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)
print(example())