from ROOT import TH1F
from ROOT import THStack
from ROOT import TCanvas

#job progress (the numner of processed Events will be reported in multiples of reportEvery)
reportEvery = 1000

#lumi = 3219.56
lumi = 32988.1
gridEff = 0.97
lumi = lumi*gridEff

samples = []
samples_mc = ["www", "tz", "zz", "twz", "tt", "ttw", "ttzee", "wz"]
#samples_mc = ["wz"]

signal =  "twz"
samples_data = ["data2016"]
samples = samples_data + samples_mc

pathStem = "../ntuples/"

treeName = "nominal"
weightsTreeName = "sumWeights"

zoomFactorMax = 5.0
zoomFactorMin = 0.1

colours = {
    "twz": 1,
    "tz": 4,
    "tt": 2,
    "wz": 3,
    "ttw": 5,
    "zz": 6,
    "www": 7,
    "ttzee": 44,
    "data2015": 1,
    "data2016": 1
}

#xsections from ATLAS DSIDs
xSections = {
"tz": 0.029584,
"tt": 87.63,
"twz": 0.016046,
"www": 0.00757,
"wz": 4.5,
"zz": 1.269,
"ttw": 0.603,
"ttzee": 0.0413
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

st_mll_OSSF = THStack()

obs = {
"h_mll_OSSF": TH1F("","", 15, 0, 120),
"h_nJets": TH1F("","", 6, -0.5, 5.5),
"h_nTags": TH1F("","", 6, -0.5, 5.5),
"h_mu": TH1F("","", 60, 0.0, 60),
"h_MET": TH1F("","", 40, 0.0, 300)
}

stacks = {}
histoGroups = {}

for ob in obs:
    stacks[ob] = THStack()
    histoGroups[ob] = {}
    for sample in samples:
        hist = obs[ob].Clone()
        hist.SetLineColor(colours[sample])
        hist.SetFillColor(colours[sample])
        histoGroups[ob][sample] = hist
