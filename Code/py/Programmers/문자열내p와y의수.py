from collections import Counter

def numPY(s):
    c = Counter(s.lower())
    return c['y'] == c['p'] 

print(numPY("pPoooyY"))
#print( numPY("Pyy") )