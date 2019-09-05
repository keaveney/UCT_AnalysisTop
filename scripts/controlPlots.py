##################################################
## Make Control Plots from AnalysisTop n-tuples ##
##################################################
import os
from ROOT import TFile
from ROOT import TTree
from ROOT import THStack
from ROOT import TCanvas
from ROOT import TLegend

from ROOT.Math import PtEtaPhiEVector
from itertools import combinations

import config
import tools

for type in ["mc", "data"]:
    if type == "mc":
        samples = config.samples_mc
    else:
        samples = config.samples_data

    for sample in samples:
        path = config.pathStem
        filename = path + sample + ".root"
        file = TFile(filename)
        tree = file.Get(config.treeName)
        
        weightsTree = file.Get(config.weightsTreeName)
        runningWeightSum = 0.0
        runningEventSum = 0.0

        for iEvent in range(0, weightsTree.GetEntries()):
            weightsTree.GetEntry(iEvent)
            if (iEvent == 1):
                print "sample = " + str(sample) + " dsid = " + str(weightsTree.dsid)
            runningWeightSum = runningWeightSum + weightsTree.totalEventsWeighted
            runningEventSum = runningEventSum + weightsTree.totalEvents

        print "filename, entries, total events , total events weighted = " + str(filename) + " " + str(runningEventSum) + " " + str(tree.GetEntries()) +" "+ str(runningWeightSum)
        finalWeight =  1.0

        for iEvent in range(0, tree.GetEntries()):
            if (iEvent % config.reportEvery == 0):
                print("nEvents processed = " + str(iEvent) + "/" + str(tree.GetEntries()) + " (" + str(float(iEvent*100)/float(tree.GetEntries())) + "%)")
            tree.GetEntry(iEvent)
            if type == "mc":
                #print "sample = " + str(sample) + " xsection = " + str(config.xSections[sample]) + " lumi = " + str(config.lumi)
                normWeight = (config.xSections[sample]*config.lumi*tree.weight_mc)/(runningWeightSum)
                calibrationWeight =  tree.weight_pileup*tree.weight_leptonSF*tree.weight_jvt*tree.weight_bTagSF_MV2c10_77
                finalWeight =  normWeight*calibrationWeight
            #print "sim weight = " + str(tree.weight_mc)
            else:
                finalWeight =  1.0
                    #if (tree.runNumber < 296939) | (tree.runNumber >311481):
                    #break

            #final event selection
            #if (len(tree.jet_phi) != 1):
            #   continue
            #print "weight = " + str(finalWeight)

            #extract list of tagged statuses for jets
            nTagged = 0
            nUntagged = 0
            tags = list(tree.jet_isbtagged_MV2c10_77)
            for j in tags:
                if (j == "\x01"):
                    nTagged = nTagged+1
                else:
                    nUntagged = nUntagged+1

                #for tag in tree.jet_isbtagged_MV2c10_77:
                    #print "tag "
                #print hex(tree.jet_isbtagged_MV2c10_77[0])
                #print str(tree.jet_isbtagged_MV2c10_77)
                


            if ((tree.eemu_2015 == 1) | (tree.eemu_2016 == 1) ):
                eNs = []
                ePs = []
                for el in range(0, len(tree.el_phi)):
                    config.histoGroups["h_ptvarcone20"][sample].Fill(tree.el_ptvarcone20[el],finalWeight)
                    config.histoGroups["h_topoetcone20"][sample].Fill(tree.el_topoetcone20[el],finalWeight)
                    elVec = PtEtaPhiEVector(tree.el_pt[el],tree.el_eta[el],tree.el_phi[el],tree.el_e[el])
                    if (tree.el_charge[el] != -1):
                        eNs.append(elVec)
                    else:
                        ePs.append(elVec)
                
                zCands = tools.makeZCands(eNs,ePs)

                for zCand in zCands:                    config.histoGroups["h_mll_OSSF"][sample].Fill(zCand.M()/1000.00,finalWeight)

                config.histoGroups["h_nJets"][sample].Fill(len(tree.jet_phi),finalWeight)
                config.histoGroups["h_mu"][sample].Fill(tree.mu_actual,finalWeight)
                config.histoGroups["h_nTags"][sample].Fill(nTagged,finalWeight)
                config.histoGroups["h_MET"][sample].Fill(tree.met_met/1000.00,finalWeight)


outputFile = TFile("histos.root", "RECREATE")

for ob in config.histoGroups:
    c = TCanvas();
    leg = TLegend(0.83,0.62,0.99,0.98)
    leg.SetTextSize(0.035)
    for sample in config.samples:
        if ("data" not in sample):
            config.stacks[ob].Add(config.histoGroups[ob][sample],"HIST")
            leg.AddEntry(config.histoGroups[ob][sample], sample, "f")
        else:
            leg.AddEntry(config.histoGroups[ob][sample], sample, "E0p")
            minY = (config.histoGroups[ob][sample].GetMinimum(0.0))*config.zoomFactorMin
            maxY = (config.histoGroups[ob][sample].GetBinContent(config.histoGroups[ob][sample].GetMaximumBin()))*config.zoomFactorMax

    config.stacks[ob].SetMinimum(minY)
    config.stacks[ob].SetMaximum(maxY)
    xTitle = ob.split("_")[1]
    config.stacks[ob].Draw()
    config.histoGroups[ob]["data2016"].Draw("E0PSAME")
    config.stacks[ob].GetXaxis().SetTitle(xTitle)

    leg.Draw()
    canvasName = ob + ".pdf"
    c.SetLogy()
    c.SaveAs(canvasName)
    c.Write()
outputFile.Close()
