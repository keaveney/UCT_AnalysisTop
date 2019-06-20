##################################################
## Make Control Plots from AnalysisTop n-tuples ##
##################################################
import os
from ROOT import TFile
from ROOT import TTree
from ROOT import THStack
from ROOT import TCanvas
from ROOT.Math import PtEtaPhiEVector
from itertools import combinations

import config
import tools

for sample in config.samples_mc:
    path = config.pathStem
    filename = path + sample + ".root"
    file = TFile(filename)
    tree = file.Get(config.treeName)
        
    print "filename, entries = " + str(filename) + " " + str(tree.GetEntries())

    for iEvent in range(0, tree.GetEntries()):
        tree.GetEntry(iEvent)
        if ((tree.mumumu_2015 == 1) | (tree.mumumu_2016 == 1) ):
            muNs = []
            muPs = []
            for mu in range(0, len(tree.mu_phi)):
                muVec = PtEtaPhiEVector(tree.mu_pt[mu],tree.mu_eta[mu],tree.mu_phi[mu],tree.mu_e[mu])
                if (tree.mu_charge[mu] != -1):
                    muNs.append(muVec)
                else:
                    muPs.append(muVec)
            
            zCands = tools.makeZCands(muNs,muPs)

            for zCand in zCands:
                config.histos_mll_OSSF[sample].Fill(zCand.M()/1000.00, tree.weight_mc)

            # find hadronic top candidates
            config.h_nJets.Fill(len(tree.jet_phi))
            print "filling,  " + str(filename)

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
                config.h_hadTopCandMass.Fill(candVec.M()/1000.00)
    config.histos_mll_OSSF[sample].SetFillColor(config.colours[sample])
    config.st_mll_OSSF.Add(config.histos_mll_OSSF[sample])
    config.histos_mll_OSSF[sample].SetFillColor(config.colours[sample])

outputFile = TFile("histos.root", "RECREATE")

c = TCanvas();
config.histos_mll_OSSF["twz"].Draw()
#config.st_mll_OSSF.Draw()
c.Write()
#config.st_mll_OSSF.Write()

#for s in config.samples_mc:
#    config.histos_mll_OSSF[s].Write()

outputFile.Close()

#config.h_hadTopCandMass.Draw()
#h_nJets.Draw()
#h_mll_OSSF.Draw()

                        






