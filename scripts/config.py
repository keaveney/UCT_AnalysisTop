from ROOT import TH1F
from ROOT import TH2F

from ROOT import THStack
from ROOT import TCanvas
from ROOT import TFile


#job progress (the numner of processed Events will be reported in multiples of reportEvery)
reportEvery = 10000

#lumi = 3219.56
lumi = 32988.1
gridEff = 0.97
lumi = lumi*gridEff

samples = []
#samples_mc = ["zzz4l","wwz4l","wzz3l","www", "tz", "zz", "twz", "tt", "ttw","zee","zmumu", "ttz_incl", "wz", "ttWW" "ttH", "tttt"]
#samples_mc = ["zzz4l","wwz4l","wzz3l","www", "tz", "zz", "twz", "tt", "ttw","zee","zmumu", "ttz_incl", "VVlll", "ttWW","ttH", "tttt"]

samples_mc = ["ttz_incl"]

signal =  "twz"
samples_data = ["data2016"]
samples = samples_data + samples_mc

pathStem = "../ntuples/"

epochs = ["2016"]
channels = ["eemu"]
#channels = ["eemu", "eee", "mumue", "mumumu"]

treeName = "nominal"
weightsTreeName = "sumWeights"
truthTreeName = "truth"

#zoomFactorMax = 5.0
#zoomFactorMin = 0.1

zoomFactorMax = 1.3
zoomFactorMin = 0.0

colours = {
    "twz": 1,
    "tz": 4,
    "tt": 2,
    "wz": 3,
    "ttw": 5,
    "zz": 6,
    "www": 7,
    "wwz4l": 8,
    "zzz4l": 11,
    "wzz3l": 12,
    "zmumu": 13,
    "VVlll": 14,
    "ttWW": 15,
    "tttt": 16,
    "ttH": 9,
    "zee": 10,
    "ttzee": 44,
    "ttzmumu": 46,
    "ttz_incl": 47,
    "data2015": 1,
    "data2016": 1
}

#xsections from ATLAS DSIDs
xSections = {
"tz": 0.029584,
"tt": 87.63,
"zee": 1950.63,
"zmumu": 1950.63,
"twz": 0.016046,
"www": 0.00757,
"wwz4l": 0.0017966,
"zzz4l": 0.0000863731512,
"wzz3l": 0.000747635474,
#"wz": 4.5,
"wz": 6.615, # assuming 1.47 (data/nlo) scale factor as seen in ATL-COM-PHYS-2016
"zz": 1.269,
"ttw": 0.603,
"ttzee": 0.0413,
"ttzmumu": 0.0413,
"ttz_incl": 0.1239,
"ttH": 0.05343,
#"VVlll": 4.5832,
# assuming 1.47 (data/nlo) scale factor as seen in ATL-COM-PHYS-2016
"VVlll": 6.737,
"ttWW": 0.0099,
"tttt": 0.0092
}

    #xSections = {
    #"tz": 0.240,# sigma nlo 0.6993,BR Z->ll 0.1011 (0.6993*0.101)
    #"tt": 87.62, # sigma nnlo 831.76, BR W->lnu = 0.33 (831.76*.33*.33)
    #"twz": 0.016046,
    #"www": 0.00757,  # sigma nlo 0.2109, BR W->lnu = 0.33 (0.2109*0.33*0.33*0.33)
    #"wz": 4.5,     # sigma nlo = 44.87, BR W->lnu = 0.33, BR Z->ll 0.1011 = (44.87*0.33*0.1011)
    #"zz": 0.1446,  # sigma nlo = 14.15, BR Z->ll 0.1011 (14.15*0.1011*0.1011)
    #"ttw": 0.603, #sigma nlo 0.566, BR W->lnu = 0.33. (0.566*0.33*0.33*0.33)
#"ttzee": 0.041 #sigma nlo 0.759, BR W->lnu = 0.33. (0.759*0.33*0.33*0.0335)
#}

#st_mll_OSSF = THStack()

obs = {
"h_mll_OSSF": TH1F("","", 15, 0, 120),
"h_mll_SSSF": TH1F("","", 5, 0, 120),
"h_mll_PPSF": TH1F("","", 5, 0, 120),
"h_mll_NNSF": TH1F("","", 5, 0, 120),
"h_nJets": TH1F("","", 6, -0.5, 5.5),
"h_nTags": TH1F("","", 6, -0.5, 5.5),
"h_mu": TH1F("","", 60, 0.0, 60),
"h_mlb": TH1F("","", 20, 0.0, 1000),
"h_ptlb": TH1F("","", 20, 0.0, 500),
"h_mjj": TH1F("","", 40, 0.0, 500),
"h_mjj_W": TH1F("","", 30, 0.0, 400),
"h_mjj_nonW": TH1F("","", 30, 0.0, 400),
"h_delRj_Wdec": TH1F("","", 60, 0.0, 10),
"h_delRjj_W1": TH1F("","", 20, 0.0, 10),
"h_delRjj_W2": TH1F("","", 20, 0.0, 10),
"h_mjjb": TH1F("","", 20, 0.0, 500),
"h_delRmubZ": TH1F("","", 15, -6.5, 6.5),
"h_MET": TH1F("","", 25, 0.0, 300),
"h_HT": TH1F("","", 25, 0.0, 300),
"h_HT_ttcntrl": TH1F("","", 25, 0.0, 300)
}


#make special (non-control plot) histos
h_delR = TH2F("","",  20, 0.0, 500,20, 0.0, 10 )
h_trueMw = TH1F("","",  30, 0.0,100 )

stacks = {}
histoGroups = {}

for channel in channels:
    stacks[channel] = {}
    histoGroups[channel] = {}
    for ob in obs:
        stacks[channel][ob] = THStack()
        histoGroups[channel][ob] = {}
        for sample in samples:
            hist = obs[ob].Clone()
            hist.SetLineColor(colours[sample])
            hist.SetFillColor(colours[sample])
            histoGroups[channel][ob][sample] = hist

