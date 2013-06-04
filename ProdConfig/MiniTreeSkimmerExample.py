

process.MiniTreeSkimming = cms.EDFilter('MiniTreeSkimmer',

        verbose             = cms.uint32(3), 
        
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

# Don't forget to add the filter in the path (process.p)

