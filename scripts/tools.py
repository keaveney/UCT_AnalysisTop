def makeZCands(lepsN, lepsP):
    zCands = []
    for n in range(0,len(lepsN)):
        for p in range(0,len(lepsP)):
            cand = lepsN[n] + lepsP[p]
            zCands.append(cand)
    return zCands
