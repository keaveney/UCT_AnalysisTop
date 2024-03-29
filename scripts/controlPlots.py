##################################################
## Make Control Plots from AnalysisTop n-tuples ##
##################################################
import os
from ROOT import TFile
from ROOT import TTree
from ROOT import THStack
from ROOT import TCanvas
from ROOT import TLegend
from ROOT import TLatex

from ROOT.Math import LorentzVector

from ROOT.Math import PtEtaPhiEVector
from ROOT.Math import PtEtaPhiMVector
from itertools import combinations

import config
import tools

for channel in config.channels:
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

            print "channel ,filename, entries, total events , total events weighted =  " + str(channel)+ " " + str(filename) + " " + str(runningEventSum) + " " + str(tree.GetEntries()) +" "+ str(runningWeightSum)
            finalWeight =  1.0

            #make hashtable
            if ("data" not in sample):
                #truthTree = tools.makeHashTable(filename, config.truthTreeName)
                #truthTree = file.Get(config.truthTreeName)
                truthTree = file.Get(config.truthTreeName)
                if (truthTree.BuildIndex("runNumber", "eventNumber") >= 0):
                    print("hash table successfully built, with " + str(truthTree.BuildIndex("runNumber", "eventNumber")) + " entries")
            
            for iEvent in range(0, tree.GetEntries()):
                if (iEvent % config.reportEvery == 0):
                    print("nEvents processed = " + str(iEvent) + "/" + str(tree.GetEntries()) + " (" + str(float(iEvent*100)/float(tree.GetEntries())) + "%)")
                tree.GetEntry(iEvent)
                if type == "mc":
                    #print "sample = " + str(sample) + " xsection = " + str(config.xSections[sample]) + " lumi = " + str(config.lumi)
                    normWeight = (config.xSections[sample]*config.lumi*tree.weight_mc)/(runningWeightSum)
                    calibrationWeight =  tree.weight_pileup*tree.weight_globalLeptonTriggerSF*tree.weight_leptonSF*tree.weight_jvt*tree.weight_bTagSF_MV2c10_77
                    finalWeight =  normWeight*calibrationWeight
                else:
                    finalWeight =  1.0

                #apply 'pre-selection' on the basis of nutple flag
                #check what channel we are processing first
                preSel = 0
                lepsPhi = []
                lepsPt = []
                lepsEta = []
                lepsE = []

                if ((channel == "eemu") & (tree.eemu_2016 == 1)):
                    preSel = 1
                    lepsPhi = tree.el_phi
                    lepsEta = tree.el_eta
                    lepsPt = tree.el_pt
                    lepsE = tree.el_e
                elif ((channel == "eee") & (tree.eee_2016 == 1)):
                    preSel = 1
                    lepsPhi = tree.el_phi
                    lepsEta = tree.el_eta
                    lepsPt = tree.el_pt
                    lepsE = tree.el_e
                elif ((channel == "mumue") & (tree.mumue_2016 == 1)):
                    preSel = 1
                    lepsPhi = tree.mu_phi
                    lepsEta = tree.mu_eta
                    lepsPt = tree.mu_pt
                    lepsE = tree.mu_e
                elif ((channel == "mumumu") & (tree.mumumu_2016 == 1)):
                    preSel = 1
                    lepsPhi = tree.mu_phi
                    lepsEta = tree.mu_eta
                    lepsPt = tree.mu_pt
                    lepsE = tree.mu_e
                    
                if (preSel == 1):
                    #make z->ll candidates
                    lepsN = []
                    lepsP = []
                    for lep in range(0, len(lepsPhi)):
                        lepVec = PtEtaPhiEVector(lepsPt[lep],lepsEta[lep],lepsPhi[lep],lepsE[lep])
                        if ((channel == "eemu") | (channel == "eee")):
                            if (tree.el_charge[lep] != -1):
                               lepsN.append(lepVec)
                            else:
                               lepsP.append(lepVec)
                        elif ((channel == "mumue") | (channel == "mumumu")):
                            if (tree.mu_charge[lep] != -1):
                                lepsN.append(lepVec)
                            else:
                                lepsP.append(lepVec)

                    zCands = tools.makeZCands(lepsN,lepsP)
                    zCandsPP = tools.makeZCands(lepsP,lepsP)
                    zCandsNN = tools.makeZCands(lepsN,lepsN)

                    #extract list of tagged statuses for jets
                    nTagged = 0
                    nUntagged = 0
                    tags = list(tree.jet_isbtagged_MV2c10_77)
                    bTaggedJets = []
                    unTaggedJets = []
                    jets = []
                    trueWDecParts = []
                    trueWParts = []
                    
                    for j in range(0, len(tags)):
                        jetVec = PtEtaPhiEVector(tree.jet_pt[j],tree.jet_eta[j],tree.jet_phi[j],tree.jet_e[j])
                        if (tags[j] == "\x01"):
                            nTagged = nTagged+1
                            bTaggedJets.append(jetVec)
                            jets.append(jetVec)
                        else:
                            nUntagged = nUntagged+1
                            unTaggedJets.append(jetVec)
                            jets.append(jetVec)

                        if "data" not in str(sample):
                            for k in range(0, len(tags)):
                                if (j != k):
                                    jetVec2 = PtEtaPhiEVector(tree.jet_pt[k],tree.jet_eta[k],tree.jet_phi[k],tree.jet_e[k])
                                    jjVec = jetVec + jetVec2
                                        #if (tree.jet_truthflav[j] < 5 ) & (tree.jet_truthflav[k] < 5):
                                        #config.histoGroups[channel]["h_mjj_W"][sample].Fill(jjVec.M()/1000.00,finalWeight)
                                        #else:
                                        #config.histoGroups[channel]["h_mjj_nonW"][sample].Fill(jjVec.M()/1000.00,finalWeight)

                    #calculate "global" variables
                    #HT
                    ht = 0.0
                    for j in range(0, len(tree.jet_phi)):
                        ht += tree.jet_pt[j]

                    #make t-> l,b candidates (todo generalise for other channels)
                    lepbCands = []
                    nonZlepsPhi = []
                    nonZlepsPt = []
                    nonZlepsEta = []
                    nonZlepsE = []
                    if ((channel == "eemu") | (channel == "mumumu")):
                        nonZlepsPhi = tree.mu_phi
                        nonZlepsEta = tree.mu_eta
                        nonZlepsPt = tree.mu_pt
                        nonZlepsE = tree.mu_e
                    if ((channel == "mumue") | (channel == "eee")):
                        nonZlepsPhi = tree.el_phi
                        nonZlepsEta = tree.el_eta
                        nonZlepsPt = tree.el_pt
                        nonZlepsE = tree.el_e
                    
                    #need to remove leptons that were used to make Z from the nonZleps collection
                    for lep in range(0, len(nonZlepsPhi)):
                        for bTag in range(0, len(bTaggedJets)):
                            lepVec = PtEtaPhiEVector(nonZlepsPt[lep], nonZlepsEta[lep], nonZlepsPhi[lep], nonZlepsE[lep])
                            btagVec = PtEtaPhiEVector(bTaggedJets[bTag].pt(), bTaggedJets[bTag].eta(), bTaggedJets[bTag].phi(), bTaggedJets[bTag].e())
                            lepbVec = lepVec + btagVec
                            lepbCands.append(lepbVec)
                    lepbCands.sort(key=lambda x: x.pt())

                    #make W -> jj candidates
                    jjCands = []
                    for i in range(0, len(unTaggedJets)):
                        for j in range(0, len(unTaggedJets)):
                            if (i != j):
                                jjVec = unTaggedJets[i] + unTaggedJets[j]
                                jjCands.append(jjVec)
                    jjCands.sort(key=lambda x: x.pt())

                    #match jj cands to MC Ws
                    if "data" not in str(sample):
                        #print("n Wdecparts =" + str(len(trueWDecParts)) + " n jets = " + str(len(jets)))
                        #for wd in range(0, len(trueWDecParts)):
                        #    for j in range(0, len(lepsP)):
                        #        delR = tools.deltaR(trueWDecParts[wd], lepsP[j])
                        #        config.histoGroups[channel]["h_delRj_Wdec"][sample].Fill(delR,finalWeight)
                        #truthTree.GetEntry(iEvent)
                        truthTree.GetEntryWithIndex(tree.runNumber, tree.eventNumber)
                        
                        WFromTPhi = truthTree.MC_W_from_t_phi
                        WFromTEta = truthTree.MC_W_from_t_eta
                        WFromTPt = truthTree.MC_W_from_t_pt
                        WFromTM = truthTree.MC_W_from_t_m
    
                        #print("test W phi " + str(WFromTPhi))
                        WFromTBarPhi = truthTree.MC_W_from_tbar_phi
                        WFromTBarEta = truthTree.MC_W_from_tbar_eta
                        WFromTBarPt = truthTree.MC_W_from_tbar_pt
                        WFromTBarM = truthTree.MC_W_from_tbar_m
                        
                        wFromT = PtEtaPhiMVector(WFromTPt,WFromTEta,WFromTPhi,WFromTM)
                        wFromTBar = PtEtaPhiMVector(WFromTBarPt,WFromTBarEta,WFromTBarPhi,WFromTBarM)

                        trueWParts.append(wFromT)
                        trueWParts.append(wFromTBar)

                        for i in range(0, len(jjCands)):
                            dR1 = tools.deltaR(trueWParts[0],jjCands[i])
                            dR2 = tools.deltaR(trueWParts[1],jjCands[i])
                            config.histoGroups[channel]["h_delRjj_W1"][sample].Fill(dR1,finalWeight)
                            config.histoGroups[channel]["h_delRjj_W1"][sample].Fill(dR2,finalWeight)
                            if ((dR1 < 0.5) | (dR2 < 0.5)):
                                config.histoGroups[channel]["h_mjj_W"][sample].Fill(jjCands[i].M()/1000.00,finalWeight)
                            else:
                                config.histoGroups[channel]["h_mjj_nonW"][sample].Fill(jjCands[i].M()/1000.00,finalWeight)

                    #make t -> Wb -> jjb candidates
                    jjbCands = []
                    if (len(jjCands) > 0):
                        for i in range(0, len(jjCands)):
                            for j in range(0, len(bTaggedJets)):
                                jjbVec = jjCands[i] + bTaggedJets[j]
                                jjbCands.append(jjbVec)
                    jjbCands.sort(key=lambda x: x.pt())

                    #angular variables
                    #delr lb-Z
                    if ((len(zCands) != 0) &(len(lepbCands) != 0)):
                        delRmubZ = ((((lepbCands[0].eta() - zCands[0].eta())**2) + ((lepbCands[0].phi() - zCands[0].phi())**2))**0.5)

                    #make z selection (require highest pt dilepton to be close to Z mass, possibly not optimal)
                    if(len(zCands) != 0):
                        #if (((zCands[0].mass()/1000.00) > 70.0 ) | ((zCands[0].mass()/1000.00) > 110.0 )):
                        if(len(zCands) !=0): config.histoGroups[channel]["h_mll_OSSF"][sample].Fill(zCands[0].M()/1000.00,finalWeight)
                        if(len(zCandsPP)!=0): config.histoGroups[channel]["h_mll_SSSF"][sample].Fill(zCandsPP[0].M()/1000.00,finalWeight)
                        if(len(zCandsNN)!=0): config.histoGroups[channel]["h_mll_SSSF"][sample].Fill(zCandsNN[0].M()/1000.00,finalWeight)
                        if(len(zCandsPP)!=0): config.histoGroups[channel]["h_mll_PPSF"][sample].Fill(zCandsPP[0].M()/1000.00,finalWeight)
                        if(len(zCandsNN)!=0): config.histoGroups[channel]["h_mll_NNSF"][sample].Fill(zCandsNN[0].M()/1000.00,finalWeight)

                        config.histoGroups[channel]["h_nJets"][sample].Fill(len(tree.jet_phi),finalWeight)
                        config.histoGroups[channel]["h_mu"][sample].Fill(tree.mu_actual,finalWeight)
                        config.histoGroups[channel]["h_nTags"][sample].Fill(len(bTaggedJets),finalWeight)
                        config.histoGroups[channel]["h_MET"][sample].Fill(tree.met_met/1000.00,finalWeight)
                        config.histoGroups[channel]["h_HT"][sample].Fill(ht/1000.00,finalWeight)
                        if ((((zCands[0].mass()/1000.00) < 80.0 ) | ((zCands[0].mass()/1000.00) > 100.0 )) & (nTagged >1)):
                            config.histoGroups[channel]["h_HT_ttcntrl"][sample].Fill(ht/1000.00,finalWeight)
                        config.histoGroups[channel]["h_mlb"][sample].Fill(lepbCands[0].M()/1000.00,finalWeight)
                        config.histoGroups[channel]["h_ptlb"][sample].Fill(lepbCands[0].pt()/1000.00,finalWeight)
                        if(len(jjCands) !=0): config.histoGroups[channel]["h_mjj"][sample].Fill(jjCands[0].M()/1000.00,finalWeight)
                        if(len(jjbCands) !=0): config.histoGroups[channel]["h_mjjb"][sample].Fill(jjbCands[0].M()/1000.00,finalWeight)
                        if((len(lepbCands) !=0)& (len(zCands) !=0) ): config.histoGroups[channel]["h_delRmubZ"][sample].Fill(delRmubZ,finalWeight)

for channel in config.channels:
    outputFileName = "histos" + channel + ".root"
    outputFile = TFile(outputFileName, "RECREATE")
    for ob in config.obs:
        c = TCanvas();
        leg = TLegend(0.75,0.62,0.99,0.98)
        leg.SetTextSize(0.035)
        for sample in config.samples:
            name = sample + "truemw"
            config.h_trueMw.Write(name)
            histName = ob + "_" + sample
            if ("data" not in sample):
                config.histoGroups[channel][ob][sample].SetDirectory(outputFile)
                config.histoGroups[channel][ob][sample].Write(histName)
                config.stacks[channel][ob].Add(config.histoGroups[channel][ob][sample],"HIST")
                leg.AddEntry(config.histoGroups[channel][ob][sample], sample, "f")
            else:
                config.histoGroups[channel][ob][sample].SetDirectory(outputFile)
                config.histoGroups[channel][ob][sample].Write(histName)
                sampleStr = sample + " " + str(config.histoGroups[channel][ob][sample].Integral()) + " events"
                leg.AddEntry(config.histoGroups[channel][ob][sample], sampleStr, "E0p")
                minY = (config.histoGroups[channel][ob][sample].GetMinimum(0.0))*config.zoomFactorMin
                maxY = (config.histoGroups[channel][ob][sample].GetBinContent(config.histoGroups[channel][ob][sample].GetMaximumBin()))*config.zoomFactorMax

        config.stacks[channel][ob].SetMinimum(minY)
        config.stacks[channel][ob].SetMaximum(maxY)
        xTitle = ob.split("_")[1]
        config.stacks[channel][ob].Draw()
        config.histoGroups[channel][ob]["data2016"].Draw("E0PSAME")
        config.stacks[channel][ob].GetXaxis().SetTitle(xTitle)
        leg.Draw()
        latex = TLatex()
        latex.SetTextSize(0.06)
        latex.SetTextAlign(13)
        latex.DrawLatexNDC(0.2,0.85,channel)
        
        canvasName = "../plots/" + channel + "/" + ob + "_" + channel + ".pdf"
        #c.SetLogy()
        c.SaveAs(canvasName)
        canvasTitle = channel + "/" + ob + "_" + channel
        c.Write(canvasTitle)
        config.h_delR.Write()

    outputFile.Close()
