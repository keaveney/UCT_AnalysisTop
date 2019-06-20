from ROOT import TH1F
from ROOT import THStack
from ROOT import TCanvas

lumi = 36.00000

samples = []
samples_mc = ["twz","wz"]
samples_data = []

pathStem = "../ntuples/mc/"

treeName = "nominal"

colours = {
    "twz": 42,
    "wz": 43,
    "ttzee": 44
}

h_mll_OSSF = TH1F("","", 10, 0, 120)
h_nJets = TH1F("","", 6, -0.5, 5.5)
h_hadTopCandMass = TH1F("","", 50, 0, 400)

st_mll_OSSF = THStack()

histos_mll_OSSF = {
    "twz": TH1F("","", 10, 0, 120),
    "wz": TH1F("","", 10, 0, 120),
    "ttzee": TH1F("","", 10, 0, 120)
}

for sample in samples_mc:
    print "setting colour " + str(colours[sample])
    histos_mll_OSSF[sample].SetFillColor(colours[sample])




