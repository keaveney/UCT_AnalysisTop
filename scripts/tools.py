from ROOT import TFile


def makeZCands(lepsN, lepsP):
    zCands = []
    for n in range(0,len(lepsN)):
        for p in range(0,len(lepsP)):
            if(lepsN[n] != lepsP[p]):
                cand = lepsN[n] + lepsP[p]
                zCands.append(cand)
    #order by pt
    zCands.sort(key=lambda x: x.pt())
    return zCands


def deltaR(vec1, vec2):
    #print " vec 1 eta = " + str(vec1.eta()) + " vec 2 eta = " + str(vec2.eta())
    dr = ( (vec1.eta() - vec2.eta())**2 + (vec1.phi() - vec2.phi())**2)**(0.5)
    return dr

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

def makeHashTable(fileName, truthTreeName):
    file = TFile(fileName)
    truthTree = file.Get(truthTreeName)
    truthTree.GetEvent(1)
    testEvN = truthTree.eventNumber
    testRunN = truthTree.runNumber

    if (truthTree.BuildIndex("runNumber", "eventNumber") >= 0):
        truthTree.GetEntryWithIndex(testEvN, testRunN)
        print("hash table successfully built, with " + str(truthTree.BuildIndex("runNumber", "eventNumber")) + " entries")
        print("testW phi = " + str(truthTree.MC_W_from_tbar_phi))
    return truthTree


    
    
    
    
    
    
    
    """
    decW1FromTPhi = truthTree.MC_Wdecay1_from_t_phi
    decW1FromTEta = truthTree.MC_Wdecay1_from_t_eta
    decW1FromTPt = truthTree.MC_Wdecay1_from_t_pt
    decW1FromTM = truthTree.MC_Wdecay1_from_t_m
        
    decW2FromTPhi = truthTree.MC_Wdecay1_from_t_phi
    decW2FromTEta = truthTree.MC_Wdecay1_from_t_eta
    decW2FromTPt = truthTree.MC_Wdecay1_from_t_pt
    decW2FromTM = truthTree.MC_Wdecay1_from_t_m
    
    decW1FromTBarPhi = truthTree.MC_Wdecay2_from_tbar_phi
    decW1FromTBarEta = truthTree.MC_Wdecay2_from_tbar_eta
    decW1FromTBarPt = truthTree.MC_Wdecay2_from_tbar_pt
    decW1FromTBarM = truthTree.MC_Wdecay2_from_tbar_m
    
    decW2FromTBarPhi = truthTree.MC_Wdecay2_from_tbar_phi
    decW2FromTBarEta = truthTree.MC_Wdecay2_from_tbar_eta
    decW2FromTBarPt = truthTree.MC_Wdecay2_from_tbar_pt
    decW2FromTBarM = truthTree.MC_Wdecay2_from_tbar_m
    
    WFromTPhi = truthTree.MC_W_from_t_phi
    WFromTEta = truthTree.MC_W_from_t_eta
    WFromTPt = truthTree.MC_W_from_t_pt
    WFromTM = truthTree.MC_W_from_t_m
    
    WFromTBarPhi = truthTree.MC_W_from_tbar_phi
    WFromTBarEta = truthTree.MC_W_from_tbar_eta
    WFromTBarPt = truthTree.MC_W_from_tbar_pt
    WFromTBarM = truthTree.MC_W_from_tbar_m
    
    trueWDecParts.append(PtEtaPhiMVector(decW1FromTPt,decW1FromTEta,decW1FromTPhi,decW1FromTM))
    trueWDecParts.append(PtEtaPhiMVector(decW2FromTPt,decW2FromTEta,decW2FromTPhi,decW2FromTM))
    trueWDecParts.append(PtEtaPhiMVector(decW1FromTBarPt,decW1FromTBarEta,decW1FromTBarPhi,decW1FromTBarM))
    trueWDecParts.append(PtEtaPhiMVector(decW2FromTBarPt,decW2FromTBarEta,decW2FromTBarPhi,decW2FromTBarM))
    
    wFromTDec1=PtEtaPhiMVector(decW1FromTPt,decW1FromTEta,decW1FromTPhi,decW1FromTM)
    wFromTDec2=PtEtaPhiMVector(decW2FromTPt,decW2FromTEta,decW2FromTPhi,decW2FromTM)
    
    wFromT = PtEtaPhiMVector(WFromTPt,WFromTEta,WFromTPhi,WFromTM)
    wFromTBar = PtEtaPhiMVector(WFromTBarPt,WFromTBarEta,WFromTBarPhi,WFromTBarM)
    trueWParts.append(wFromT)
    trueWParts.append(wFromTBar)
    
    wFromTDec1=PtEtaPhiMVector(decW1FromTPt,decW1FromTEta,decW1FromTPhi,decW1FromTM)
    wFromTDec2=PtEtaPhiMVector(decW2FromTPt,decW2FromTEta,decW2FromTPhi,decW2FromTM)
    
    wFromTBarDec1=PtEtaPhiMVector(decW1FromTBarPt,decW1FromTBarEta,decW1FromTBarPhi,decW1FromTBarM)
    wFromTBarDec2=PtEtaPhiMVector(decW2FromTBarPt,decW2FromTBarEta,decW2FromTBarPhi,decW2FromTBarM)
    
    wFromTDec = wFromTDec1+wFromTDec2
    wFromTBarDec = wFromTBarDec1+wFromTBarDec2
    
    #print("mW1 = " + str(wFromT.M()) + " mW2 = " + str(wFromTBar.M()))
    #config.h_trueMw.Fill(wFromT.M())
    #config.h_trueMw.Fill(wFromTBar.M())
    config.h_trueMw.Fill(decW1FromTM)

    
"""
