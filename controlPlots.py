##################################################
## Make Control Plots from AnalysisTop n-tuples ##
##################################################

from ROOT import TFile
from ROOT import TTree
from ROOT import TH1F
from ROOT.Math import PtEtaPhiEVector
from itertools import combinations

files = ["output-modifiedSelection.root"]
treeName = "nominal"

h_mll_OSSF = TH1F("","", 10, 0, 120)
h_nJets = TH1F("","", 6, -0.5, 5.5)
h_hadTopCandMass = TH1F("","", 20, 0, 400)



def makeZCands(lepsN, lepsP):
    print "making Z cands"
    zCands = []
    for n in range(0,len(lepsN)):
        for p in range(0,len(lepsP)):
            cand = lepsN[n] + lepsP[p]
            zCands.append(cand)
    return zCands


for filename in files:
    file = TFile(filename)
    tree = file.Get(treeName)
    
    print "N entries = " + str(tree.GetEntries())

    for iEvent in range(0, tree.GetEntries()):
        tree.GetEntry(iEvent)
        # addtional event-level selection
        if (len(tree.jet_phi) < 3):
            continue
        if ((tree.mumumu_2015 == 1) | (tree.mumumu_2016 == 1) ):
            print "Event # " + str(iEvent)
            muNs = []
            muPs = []
            for mu in range(0, len(tree.mu_phi)):
                muVec = PtEtaPhiEVector(tree.mu_pt[mu],tree.mu_eta[mu],tree.mu_phi[mu],tree.mu_e[mu])
                if (tree.mu_charge[mu] != -1):
                    muNs.append(muVec)
                else:
                    muPs.append(muVec)
        
            zCands = makeZCands(muNs,muPs)

            for zCand in zCands:
                print "zCand Mass = " + str(zCand.M())
                h_mll_OSSF.Fill(zCand.M()/1000.00)

        
        # find hadronic top candidates
        h_nJets.Fill(len(tree.jet_phi))
        
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
            print "hadTopCand mass = " + str(candVec.M())
            h_hadTopCandMass.Fill(candVec.M()/1000.00)

h_hadTopCandMass.Draw()
#h_nJets.Draw()
#h_mll_OSSF.Draw()

                        






