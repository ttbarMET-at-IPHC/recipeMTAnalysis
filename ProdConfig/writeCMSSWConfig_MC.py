#
#  SUSY-PAT configuration file
#
#  PAT configuration for the SUSY group - 53X series
#  More information here:
#  https://twiki.cern.ch/twiki/bin/view/CMS/SusyPatLayer1DefV12
#

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

#-- Meta data to be logged in DBS ---------------------------------------------
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.3 $'),
    name = cms.untracked.string('$Source: /local/reps/CMSSW/UserCode/TTbarMETIPHC/Alex/ProdConfig/writeCMSSWConfig_MC.py,v $'),
    annotation = cms.untracked.string('SUSY pattuple definition')
)

#-- Message Logger ------------------------------------------------------------
process.MessageLogger.categories.append('PATSummaryTables')
process.MessageLogger.cerr.PATSummaryTables = cms.untracked.PSet(
    limit = cms.untracked.int32(-1),
    reportEvery = cms.untracked.int32(1)
    )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

#-- VarParsing ----------------------------------------------------------------
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('standard')

options.output = "SUSYPAT.root"
options.maxEvents = 100
#  for SusyPAT configuration
options.register('GlobalTag', "", VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "GlobalTag to use (if empty default Pat GT is used)")
options.register('mcInfo', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "process MonteCarlo data") # False for data
options.register('jetCorrections', 'L1FastJet', VarParsing.VarParsing.multiplicity.list, VarParsing.VarParsing.varType.string, "Level of jet corrections to use: Note the factors are read from DB via GlobalTag")
options.jetCorrections.append('L2Relative')
options.jetCorrections.append('L3Absolute')
#options.jetCorrections.append('L2L3Residual') # !! This sould be disabled for MC and enabled for data
options.register('hltName', 'HLT', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "HLT menu to use for trigger matching")
options.register('mcVersion', '', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "Currently not needed and supported")
options.register('jetTypes', '', VarParsing.VarParsing.multiplicity.list, VarParsing.VarParsing.varType.string, "Additional jet types that will be produced (AK5Calo and AK5PF, cross cleaned in PF2PAT, are included anyway)")
options.register('hltSelection', '', VarParsing.VarParsing.multiplicity.list, VarParsing.VarParsing.varType.string, "hlTriggers (OR) used to filter events")
options.register('doValidation', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "Include the validation histograms from SusyDQM (needs extra tags)")
options.register('doExtensiveMatching', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "Matching to simtracks (needs extra tags)")
options.register('doSusyTopProjection', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "Apply Susy selection in PF2PAT to obtain lepton cleaned jets (needs validation)")
options.register('doType1MetCorrection', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Apply Type1 MET correction in PF2PAT")
options.register('doType0MetCorrection', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Apply Type0 MET correction in PF2PAT")
options.register('addKeep', '', VarParsing.VarParsing.multiplicity.list, VarParsing.VarParsing.varType.string, "Additional keep and drop statements to trim the event content")
options.register('useExtraJetColls', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Write extra jet collections for substructure studies")
options.register ('usePythia8', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Use status codes from Pythia8 rather than Pythia6")
options.register ('usePythia6andPythia8', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Use status codes from Pythia8 and Pythia6")
# Switch this to false for MC and true for data ? 
options.register ('useData', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, 'Run this on real data')

#---parse user input
options.parseArguments()
options._tagOrder =[]

#-- Input Source --------------------------------------------------------------
if options.files:
    process.source.fileNames = cms.untracked.vstring (options.files)
#process.source.fileNames = [
#     '/store/relval/CMSSW_3_7_0_pre5/RelValProdTTbar/GEN-SIM-RECO/MC_37Y_V4-v1/0023/BA92C6D3-8863-DF11-B3AF-002618943939.root'
#    ]

process.maxEvents.input = options.maxEvents
# Due to problem in production of LM samples: same event number appears multiple times
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

#-- Calibration tag -----------------------------------------------------------
if options.GlobalTag:
    process.GlobalTag.globaltag = options.GlobalTag

############################# START SUSYPAT specifics ####################################
from PhysicsTools.Configuration.SUSY_pattuple_cff import addDefaultSUSYPAT, getSUSY_pattuple_outputCommands
#Apply SUSYPAT
addDefaultSUSYPAT(process,options.mcInfo,options.hltName,options.jetCorrections,options.mcVersion,options.jetTypes,options.doValidation,options.doExtensiveMatching,options.doSusyTopProjection,options.doType1MetCorrection,options.doType0MetCorrection)
SUSY_pattuple_outputCommands = getSUSY_pattuple_outputCommands( process )
############################## END SUSYPAT specifics ####################################

#-- TimeReport and TrigReport after running ----------------------------------
process.options.wantSummary = False

#-- HLT selection ------------------------------------------------------------
import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
if options.hltSelection:
    process.hltFilter = hlt.hltHighLevel.clone(
        HLTPaths = cms.vstring(options.hltSelection),
        TriggerResultsTag = cms.InputTag("TriggerResults","",options.hltName),
        throw = False
    )
    process.susyPatDefaultSequence.replace(process.eventCountProducer, process.eventCountProducer * process.hltFilter)

#-- Output module configuration -----------------------------------------------
process.out.fileName = options.output

# Custom settings
process.out.splitLevel = cms.untracked.int32(99)  # Turn on split level (smaller files???)
process.out.overrideInputFileSplitLevels = cms.untracked.bool(True)
process.out.dropMetaData = cms.untracked.string('DROPPED')   # Get rid of metadata related to dropped collections
if options.hltSelection:
    process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
if options.addKeep:
    process.out.outputCommands.extend(options.addKeep)











# #############################################################################
# #       Additionnal stuff/modifications from Alex@Strasbourg/IPHC           #
# #############################################################################








# Change correction factors used
process.patJetCorrFactorsPF.payload = cms.string('AK5PF')
process.pfJetMETcorrPF.offsetCorrLabel = cms.string('ak5PFL1Fastjet')
process.pfJetMETcorrPF.jetCorrLabel = cms.string('AK5PFchsCombinedCorrector')
process.pfNoTauPF.bottomCollection = cms.InputTag("ak5PFJets")

# #################################################
# #              MET filter/tagging               #
# #################################################

# from PhysicsTools.PatAlgos.patTemplate_cfg import *

## The good primary vertex filter ____________________________________________||
process.primaryVertexFilter = cms.EDFilter(
    "VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2"),
    filter = cms.bool(True)
)

## The beam scraping filter __________________________________________________||
process.noscraping = cms.EDFilter(
    "FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
    debugOn = cms.untracked.bool(False),
    numtrack = cms.untracked.uint32(10),
    thresh = cms.untracked.double(0.25)
)

## The iso-based HBHE noise filter ___________________________________________||
#process.load('CommonTools.RecoAlgos.HBHENoiseFilter_cfi')

## The CSC beam halo tight filter ____________________________________________||
# process.load('RecoMET.METAnalyzers.CSCHaloFilter_cfi')

## The HCAL laser filter _____________________________________________________||
process.load("RecoMET.METFilters.hcalLaserEventFilter_cfi")
process.hcalLaserEventFilter.vetoByRunEventNumber=cms.untracked.bool(False)
process.hcalLaserEventFilter.vetoByHBHEOccupancy=cms.untracked.bool(True)

## The ECAL dead cell trigger primitive filter _______________________________||
process.load('RecoMET.METFilters.EcalDeadCellTriggerPrimitiveFilter_cfi')

## The EE bad SuperCrystal filter ____________________________________________||
process.load('RecoMET.METFilters.eeBadScFilter_cfi')

## The ECAL laser correction filter
process.load('RecoMET.METFilters.ecalLaserCorrFilter_cfi')

## The Good vertices collection needed by the tracking failure filter ________||
process.goodVertices = cms.EDFilter(
          "VertexSelector",
          filter = cms.bool(False),
          src = cms.InputTag("offlinePrimaryVertices"),
          cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.rho < 2")
)

## The tracking failure filter _______________________________________________||
process.load('RecoMET.METFilters.trackingFailureFilter_cfi')


process.METfiltersSeq = cms.Sequence(
           process.primaryVertexFilter *
           process.noscraping *
           #process.HBHENoiseFilter *
           #process.CSCTightHaloFilter *
           process.hcalLaserEventFilter *
           process.EcalDeadCellTriggerPrimitiveFilter *
           process.goodVertices * process.trackingFailureFilter *
           process.eeBadScFilter *
           process.ecalLaserCorrFilter
)



# #################################################
# # Rho for rho-corrected isolation for electrons #
# #################################################

from RecoJets.JetProducers.kt4PFJets_cfi import *
process.kt6PFJetsForIsolation2011 = kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
process.kt6PFJetsForIsolation2011.Rho_EtaMax = cms.double(2.5)

# #################################################
# #            Produce trigger infos              #
# #################################################

process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
from PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cfi import *
from PhysicsTools.PatAlgos.triggerLayer1.triggerEventProducer_cfi import *
process.patTrigger = patTrigger.clone()
process.patTriggerEvent = patTriggerEvent.clone()

# #################################################
# #                Misc stuff                     #
# #################################################

from RecoJets.Configuration.RecoPFJets_cff import *
process.kt6PFJetsForRhoComputationVoronoi = kt6PFJets.clone(doRhoFastjet = True, voronoiRfact = 0.9);

# Use to produce conversion information for conversion veto later
process.patConversions = cms.EDProducer("PATConversionProducer",
   electronSource = cms.InputTag("selectedPatElectronsPF")  
)

# offlinePrimaryVertices production
process.load("RecoVertex.Configuration.RecoVertex_cff")


process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")

# #################################################
# #           Disable top projection              #
# #################################################

getattr(process,"pfNoPileUp"  ).enable = True
getattr(process,"pfNoMuon"    ).enable = False
getattr(process,"pfNoElectron").enable = False
getattr(process,"pfNoTau"     ).enable = False
getattr(process,"pfNoJet"     ).enable = False

postfix='PF'
getattr(process,"pfNoPileUp"  +postfix).enable = True
getattr(process,"pfNoMuon"    +postfix).enable = False
getattr(process,"pfNoElectron"+postfix).enable = False
getattr(process,"pfNoTau"     +postfix).enable = False
getattr(process,"pfNoJet"     +postfix).enable = False

# change the cone size of electron isolation to 0.3 as default.
process.pfIsolatedElectronsPF.isolationValueMapsCharged = cms.VInputTag(cms.InputTag("elPFIsoValueCharged03PFIdPF"))
process.pfIsolatedElectronsPF.deltaBetaIsolationValueMap = cms.InputTag("elPFIsoValuePU03PFIdPF")
process.pfIsolatedElectronsPF.isolationValueMapsNeutral = cms.VInputTag(cms.InputTag("elPFIsoValueNeutral03PFIdPF"), cms.InputTag("elPFIsoValueGamma03PFIdPF"))

process.pfElectronsPF.isolationValueMapsCharged  = cms.VInputTag(cms.InputTag("elPFIsoValueCharged03PFIdPF"))
process.pfElectronsPF.deltaBetaIsolationValueMap = cms.InputTag("elPFIsoValuePU03PFIdPF" )
process.pfElectronsPF.isolationValueMapsNeutral  = cms.VInputTag(cms.InputTag( "elPFIsoValueNeutral03PFIdPF"), cms.InputTag("elPFIsoValueGamma03PFIdPF"))

process.patElectronsPF.isolationValues = cms.PSet(
        pfChargedHadrons = cms.InputTag("elPFIsoValueCharged03PFIdPF"),
        pfChargedAll = cms.InputTag("elPFIsoValueChargedAll03PFIdPF"),
        pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU03PFIdPF"),
        pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral03PFIdPF"),
        pfPhotons = cms.InputTag("elPFIsoValueGamma03PFIdPF")
    )

# (depends of postfix / here, postfix = PF)
process.pfIsolatedElectronsPF.combinedIsolationCut = cms.double(9999.)

# change the cone size of muons isolation to 0.3 as default.
process.pfIsolatedMuonsPF.isolationValueMapsCharged = cms.VInputTag( cms.InputTag( 'muPFIsoValueCharged03PF' ) )
process.pfIsolatedMuonsPF.isolationValueMapsNeutral = cms.VInputTag( cms.InputTag( 'muPFIsoValueNeutral03PF' ), cms.InputTag( 'muPFIsoValueGamma03PF' ) )
process.pfIsolatedMuonsPF.deltaBetaIsolationValueMap = cms.InputTag( 'muPFIsoValuePU03PF' )
process.patMuonsPF.isolationValues.pfNeutralHadrons = cms.InputTag( 'muPFIsoValueNeutral03PF' )
process.patMuonsPF.isolationValues.pfPhotons = cms.InputTag( 'muPFIsoValueGamma03PF' )
process.patMuonsPF.isolationValues.pfChargedHadrons = cms.InputTag( 'muPFIsoValueCharged03PF' )
process.patMuonsPF.isolationValues.pfPUChargedHadrons = cms.InputTag( 'muPFIsoValuePU03PF' )
process.pfIsolatedMuonsPF.combinedIsolationCut = cms.double(9999.)

process.pfIsolatedMuonsPF.isolationCut = cms.double(9999.)
process.pfIsolatedElectronsPF.isolationCut = cms.double(9999.) 

# ###########################
# #   CA8 jet collection    #
# ###########################

process.load("ExoDiBosonResonances.PATtupleProduction.PAT_ca8jets_cff")

process.patJetsCA8CHSpruned.addGenJetMatch = cms.bool(False)
process.patJetsCA8CHSpruned.addGenPartonMatch = cms.bool(False)
process.patJetsCA8CHSpruned.embedGenPartonMatch = cms.bool(False)

process.selectedPatJetsCA8CHSprunedwithNsub = process.selectedPatJetsCA8CHSwithNsub.clone(
    src = cms.InputTag("selectedPatJetsCA8CHSpruned"),
        )

process.CA8prunedJets = cms.Sequence( process.ca8PFJetsCHSpruned
                                     +process.patJetCorrFactorsCA8CHSpruned
                                     +process.patJetsCA8CHSpruned
                                     +process.selectedPatJetsCA8CHSpruned
                                     +process.selectedPatJetsCA8CHSprunedwithNsub)

# #################################################
# #                  PUT Jet Id                   #
# #################################################

from CMGTools.External.puJetIDAlgo_cff import *
from CMGTools.External.pujetidproducer_cfi import *

full_53x.tmvaWeights = cms.string("CMGTools/External/data/TMVAClassificationCategory_JetID_53X_Dec2012.weights.xml")
full_53x.label = cms.string("full53x")
full_5x.label = cms.string("full5x")
        
process.puJetId = pileupJetIdProducer.clone(
    produceJetIds = cms.bool(True),
    jetids = cms.InputTag(""),
    runMvas = cms.bool(False),
    jets = cms.InputTag("selectedPatJetsPF"),
    vertexes = cms.InputTag("offlinePrimaryVertices"),
    algos = cms.VPSet(cutbased)
)
               
process.puJetMva = pileupJetIdProducer.clone(
    produceJetIds = cms.bool(False),
    jetids = cms.InputTag("puJetId"),
    runMvas = cms.bool(True),
    jets = cms.InputTag("selectedPatJetsPF"),
    vertexes = cms.InputTag("offlinePrimaryVertices"),
    algos = cms.VPSet(full_53x, full_5x)
)
# #################################################
# #             Quark-gluon tagging               #
# #################################################

process.load('QuarkGluonTagger.EightTeV.QGTagger_RecoJets_cff') 

process.QGTagger.srcJets  = cms.InputTag("selectedPatJetsPF")
process.QGTagger.dataDir  = cms.untracked.string("QuarkGluonTagger/EightTeV/data/")
process.QGTagger.isPatJet = cms.untracked.bool(True)

# #################################################
# #              MiniTree Skimmer                 #
# #################################################

process.MiniTreeSkimming = cms.EDFilter('MiniTreeSkimmer',

        verbose             = cms.uint32(0), 
        
        electron_collection = cms.InputTag("selectedPatElectrons"),
        electron_cutPt      = cms.double(20),
        electron_cutEta     = cms.double(10),
        
        muon_collection     = cms.InputTag("selectedPatMuons"),
        muon_cutPt          = cms.double(20),
        muon_cutEta         = cms.double(10),
        
        minNumberOfLeptons  = cms.uint32(1),

        jets_collection     = cms.InputTag("selectedPatJetsPF"),
        jets_cutPt          = cms.double(25),
        jets_cutEta         = cms.double(3.0),
        
        minNumberOfJets     = cms.uint32(3)

)

# #################################################
# #                   MiniTree                    #
# #################################################

process.MiniTreeProduction = cms.EDProducer('MiniTreeProducer',

        # Dataformat / Minitree version : RiverSong-pre0

# ---------------------- General info -------------------------------
        verbose             = cms.uint32(0), 
        isAOD               = cms.bool(True),    # Working with AOD 
        isData              = cms.bool(False),    # Monte-Carlo files
# ----------------------   Trigger    -------------------------------
        doTrigger           = cms.bool(True),    # Enabled
        saveAllTriggers     = cms.bool(True),
        triggerList         = cms.vstring(""),
# ----------------------  Electrons   -------------------------------
        doElectrons         = cms.bool(True),    # Enabled
        electron_cut_pt     = cms.double(10),
        electron_cut_eta    = cms.double(2.5),
        electron_saveAllID  = cms.bool(True),
        electron_IDlist     = cms.vstring(""),
        electronHLTmatching = cms.vstring(""),
        electronProducer    = cms.VInputTag(cms.InputTag("selectedPatElectrons")),
        electron_Isolist    = cms.vstring("RA4","rho","Aeff"),
        electron_rhoCorrSrc = cms.vstring("kt6PFJetsForIsolation2011","GammaAndNeutralHadronIso03","Data2012"),
        doElectronMatch     = cms.InputTag("selectedPatElectronsPF"),
# ----------------------   Photons    -------------------------------
        doPhotons           = cms.bool(False),    # Disabled
        photon_cut_pt       = cms.double(10),
        photon_cut_eta      = cms.double(2.5), 
        photonHLTmatching      = cms.vstring(""),
        photonProducer      = cms.VInputTag(cms.InputTag("selectedPatPhotonsPF2PAT")),
# -----------------------   Muons     -------------------------------
        doMuons             = cms.bool(True),    # Enabled
        muon_cut_pt         = cms.double(10),
        muon_cut_eta        = cms.double(2.5), 
        muon_cut_keepStandaloneMu  = cms.bool(True),
        muon_cut_keepTrackerMu     = cms.bool(True),
        muon_cut_keepCaloMu        = cms.bool(True),
        muon_cut_keepGlobalMu      = cms.bool(True),
        muon_IDlist                = cms.vstring("GlobalMuonPromptTight"),
        muonHLTmatching     = cms.vstring(""),
        muonProducer        = cms.VInputTag(cms.InputTag("selectedPatMuons")),
        muon_Isolist        = cms.vstring("PF03"),
        doMuonMatch         = cms.InputTag("selectedPatMuonsPF"),
# -----------------------   Taus   ---------------------------------- 
        doTaus              = cms.bool(True),    # Enabled
        tau_cut_pt          = cms.double(10),
        tau_cut_eta         = cms.double(5),
        tau_saveAllID       = cms.bool(True),
        tau_IDlist          = cms.vstring(""),
        tauHLTmatching      = cms.vstring(""),
        tauProducer         = cms.VInputTag(cms.InputTag("selectedPatTaus")),
# -----------------------   Tracks  --------------------------------- 
        doTracks            = cms.bool(False),    # Disabled
        track_cut_pt        = cms.double(-0.1),
        track_cut_eta       = cms.double(2.6),
        trackProducer       = cms.VInputTag(cms.InputTag("generalTracks")),
# -----------------------   PFCandidates  --------------------------------- 
        doPFCandidates      = cms.bool(True),    # Enabled
        pfcandidate_cut_dR  = cms.double(0.3),
        pfcandidate_cut_dz  = cms.double(0.05),
        pfcandidate_cut_minPt    = cms.double(4.0),
        pfcandidate_VertexTag     = cms.VInputTag(cms.InputTag("offlinePrimaryVertices")),
        pfcandidate_InputTag      = cms.VInputTag(cms.InputTag("particleFlow")),
# -----------------------  Vertices --------------------------------- 
        doVertices          = cms.bool(True),    # Enabled 
          saveAllVertex       = cms.bool(True),
        vertexProducer      = cms.VInputTag(cms.InputTag("goodVertices")),
# -----------------------  BeamSpot --------------------------------- 
        doBeamSpot          = cms.bool(True),    # Enabled
        beamSpotProducer    = cms.InputTag("offlineBeamSpot"),
# -----------------------   JetMet ---------------------------------- 
        doJetMet            = cms.bool(True),    # Enabled
        doMuonCorrection    = cms.bool(True),
        jet_cut_pt          = cms.double(5),
        jet_cut_eta         = cms.double(4.7), 
        jetIDList           = cms.vstring("LOOSE","TIGHT"),
        jetBTagList         = cms.vstring("trackCountingHighEffBJetTags","trackCountingHighPurBJetTags","simpleSecondaryVertexBJetTags","simpleSecondaryVertexHighEffBJetTags","simpleSecondaryVertexHighPurBJetTags","softMuonBJetTags","jetProbabilityBJetTags","jetBProbabilityBJetTags","combinedSecondaryVertexBJetTags"),
        jetHLTmatching      = cms.vstring(""),
        jetmetProducer      = cms.VPSet(
                    cms.PSet( jet = cms.untracked.string("selectedPatJetsPF"),
                              met = cms.untracked.string("patMETsPF"),
							  pfmet1 = cms.untracked.string("pfMet"),
                              algo =cms.untracked.string("pf"),
                              fillJetConstituents = cms.untracked.bool(False),
                              fillSubJetConstituents = cms.untracked.bool(False)),

                    cms.PSet( jet = cms.untracked.string('selectedPatJetsCA8CHSprunedwithNsub'),
                              met = cms.untracked.string('patMETsPF'),
                              pfmet1 = cms.untracked.string('pfMet'),
                              algo = cms.untracked.string('CA8Pruned'),
                              fillJetConstituents = cms.untracked.bool(False),
                              fillSubJetConstituents = cms.untracked.bool(True)),
                    ),

# -----------------------  Pile-Up ----------------------------------
        doPileUp            = cms.bool(True),  
        rho_PUUE_dens       = cms.InputTag("kt6PFJetsForRhoComputationVoronoi", "rho"),
        neutralRho_PUUE_dens= cms.InputTag("kt6PFJetsCentralNeutral", "rho"),
# -----------------------  MonteCarlo ------------------------------- 
        doGenParticleCollection = cms.bool(True),
        mcDescentMax            = cms.uint32(10),
        mcNGenPartMax           = cms.uint32(10000),
        mcTauDecayMode          = cms.uint32(2),
        mcHeavyQuarkDecayMode   = cms.uint32(0)
    )
    
# #################################################
# #                     Input                     #
# #################################################

process.maxEvents.input = cms.untracked.int32(-1)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#        'rfio:/dpm/in2p3.fr/home/cms/phedex/store/relval/CMSSW_5_3_2_patch1-START53_V7A/RelValTTbar/GEN-SIM-RECO/v1/0000'
#        '/RelValTTbar/CMSSW_5_3_2_patch1-START53_V7A-v1/GEN-SIM-RECO'
        # RelVal synchro files
        'file:/opt/sbg/data/data1/cms/aaubin/prodSUSYstop/synchro/inputDataset/64542608-69C7-E111-AFC8-002618943953.root',
        'file:/opt/sbg/data/data1/cms/aaubin/prodSUSYstop/synchro/inputDataset/8C41444F-62C7-E111-9FE7-002618943833.root',
        'file:/opt/sbg/data/data1/cms/aaubin/prodSUSYstop/synchro/inputDataset/D80E86FF-7EC7-E111-BB09-003048678DD6.root'
#        '/store/relval/CMSSW_5_3_2_patch1-START53_V7A/RelValTTbar/GEN-SIM-RECO/v1/0000/64542608-69C7-E111-AFC8-002618943953.root',
#       '/store/relval/CMSSW_5_3_2_patch1-START53_V7A/RelValTTbar/GEN-SIM-RECO/v1/0000/8C41444F-62C7-E111-9FE7-002618943833.root', 
#       '/store/relval/CMSSW_5_3_2_patch1-START53_V7A/RelValTTbar/GEN-SIM-RECO/v1/0000/D80E86FF-7EC7-E111-BB09-003048678DD6.root'
        )
    #duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

# #################################################
# #                   Globaltag                   #
# #################################################

# Global tags for synchro
#############

# For MC
process.GlobalTag.globaltag = cms.string('START53_V7G::All')

# For data
#process.GlobalTag.globaltag = cms.string('GR_R_52_V9::All')

# Global tags updated
#############

# For MC
# process.GlobalTag.globaltag = cms.string('DESIGN53_V15::All')

# For data
# process.GlobalTag.globaltag = cms.string('GR_P_V39_AN3::All')

# #################################################
# #                    Output                     #
# #################################################

process.out.outputCommands = cms.untracked.vstring('drop *',
                                                   'keep IPHCTreeMTEvent_*_*_*',
                                                   'keep *_MiniTreeSkimming_*_*')

# #################################################
# #                     Paths                     #
# #################################################

process.susyPatDefaultSequence = cms.Sequence(process.eventCountProducer
                                             +process.producePFMETCorrections
                                             +process.METfiltersSeq
                                             +process.kt6PFJetsForIsolation2011
                                             +process.kt6PFJetsForRhoComputationVoronoi
                                             +process.recoTauClassicHPSSequence
                                             +process.patPF2PATSequencePF
                                             +process.patPF2PATSequence
                                             +process.CA8prunedJets
                                             +process.puJetId
                                             +process.puJetMva
                                             +process.QuarkGluonTagger
                                             )

process.p = cms.Path(process.patTrigger * 
                     process.patTriggerEvent * 
                     process.susyPatDefaultSequence * 
                     process.patConversions * 
                     process.MiniTreeSkimming *
                     process.MiniTreeProduction)


# #############################################################################

#  Dump config
file = open('SusyPAT_cfg.py','w')
conf = str(process.dumpPython())

# Add traceability info
file.write('\n')
file.write('# This is traceability info used by our local NTuple format\n')
file.write('\n')
file.write('# ---------------------------------------------------------------------------\n')
file.write('# BEGIN    TRACEABILITY - TRACEABILITY - TRACEABILITY - TRACEABILITY         \n')
file.write('# ---------------------------------------------------------------------------\n')
file.write('def GetTraceability():                                                       \n')
file.write('    import inspect, os, socket, time                                         \n')
file.write('    Traceability=[]                                                          \n')
file.write('    Traceability.append( "RiverSong" ) #VERSION NAME                         \n')
file.write('    logScript = inspect.getfile(inspect.currentframe())                      \n')
file.write('    Traceability.append( logScript )                                         \n')
file.write('    logDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) \n')
file.write('    Traceability.append( logDir )                                            \n')
file.write('    Traceability.append( os.getlogin() )                                     \n')
file.write('    Traceability.append( socket.gethostname() )                              \n')
file.write('    Traceability.append( time.strftime(\'%d/%m/%y %H:%M\',time.localtime()) )\n')
file.write('    try:                                                                     \n')
file.write('        logInput = open(logDir+\'/\'+logScript)                              \n')
file.write('        for line in logInput:                                                \n')
file.write('          Traceability.append(line)                                          \n')
file.write('        logInput.close()                                                     \n')
file.write('    except:                                                                  \n')
file.write('        print "TraceabilityError : impossible to get configuration"          \n')
file.write('    return Traceability                                                      \n')
file.write('Traceability = GetTraceability()                                             \n')
file.write('# ---------------------------------------------------------------------------\n')
file.write('# END    TRACEABILITY - TRACEABILITY - TRACEABILITY - TRACEABILITY           \n')
file.write('# ---------------------------------------------------------------------------\n')
file.write('\n')
conf = conf.replace('traceability = cms.vstring()','traceability = cms.vstring(Traceability)')
conf = conf.replace('process.None+','')

file.write(conf)

file.close()
