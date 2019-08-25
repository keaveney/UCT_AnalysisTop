def makeZCands(lepsN, lepsP):
    zCands = []
    for n in range(0,len(lepsN)):
        for p in range(0,len(lepsP)):
            cand = lepsN[n] + lepsP[p]
            zCands.append(cand)
    return zCands


#def makeObs():


"""
    # find hadronic top candidates
    config.h_nJets.Fill(len(tree.jet_phi))
    
    # make list of jet 4-vectors
    jetVecs = []
    for jet in range(0, len(tree.jet_phi)):
    jetVec = PtEtaPhiEVector(tree.jet_pt[jet],tree.jet_eta[jet],tree.jet_phi[jet],tree.jet_e[jet])
    jetVecs.append(jetVec)
    
    # build all distinct tri-jet combinations
    indices = []
    indices.extend(range(0, len(tree.jet_phi)))
    comb = combinations(indices, 3)
    for c in comb:
    candVec = jetVecs[c[0]] + jetVecs[c[2]] + jetVecs[c[2]]
    config.h_hadTopCandMass.Fill(candVec.M()/1000.00, finalWeight)
    
    
    """
