#!/bin/bash

echo " "
echo "##############################################"
echo "# This installer assume your current working #"
echo "#        directory is CMSSW 532patch4        #"
echo "##############################################"
echo " "

echo " "
echo "> Installing IPHC framework"
echo " "

git clone https://github.com/ttbarMET-at-IPHC/IPHCFramework.git

mv IPHCFramework/IPHCDataFormat ./
mv IPHCFramework/MiniTree ./
mv IPHCFramework/NTuple ./
rm -r IPHCFramework

echo " "
echo "> Installing CMSSW packages"
echo " "

addpkg CommonTools/ParticleFlow  	V00-03-15
addpkg CommonTools/RecoAlgos  		V00-03-23
addpkg CommonTools/RecoUtils  		V00-00-12

addpkg CondFormats/EgammaObjects  	V00-04-00

addpkg DataFormats/METReco  		V03-03-11
addpkg DataFormats/PatCandidates  	V06-05-01

addpkg JetMETCorrections/Algorithms V02-03-00
addpkg JetMETCorrections/Modules  	V05-01-06
addpkg JetMETCorrections/Objects  	V03-01-00
addpkg JetMETCorrections/Type1MET  	V04-06-09

addpkg PhysicsTools/Configuration  	V00-12-07
addpkg PhysicsTools/IsolationAlgos  V01-05-07
addpkg PhysicsTools/IsolationUtils  V00-03-01-01
addpkg PhysicsTools/PatAlgos  		V08-09-21
addpkg PhysicsTools/PatExamples 	V00-05-24
addpkg PhysicsTools/PatUtils  		V03-09-23
addpkg PhysicsTools/SelectorUtils  	V00-03-24
addpkg PhysicsTools/UtilAlgos  		V08-02-14

addpkg RecoEgamma/ElectronIdentification  V00-03-31
addpkg RecoJets/JetAnalyzers  		V00-07-02-03
addpkg RecoJets/JetProducers  		V05-10-02
addpkg RecoMET/METAnalyzers  		V00-00-08
addpkg RecoMET/METFilters           V00-00-13-01
addpkg RecoParticleFlow/PFProducer  V15-01-11

#cvs co -r V00-00-30 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools/
cvs co -r HEAD EgammaAnalysis/ElectronTools/interface/ElectronEffectiveArea.h

# For tau ID
cvs up -r 1.31.6.4 PhysicsTools/PatAlgos/python/producersLayer1/tauProducer_cfi.py
cvs up -r 1.52.10.4 PhysicsTools/PatAlgos/python/tools/tauTools.py
cvs co -r V01-04-23 RecoTauTag/RecoTau
cvs co -r V01-04-10 RecoTauTag/Configuration

# PU-jet ID
cvs co -r V00-03-01 -d CMGTools/External UserCode/CMG/CMGTools/External

# CA8 jet collection
cvs co -r HEAD -d ./ExoDiBosonResonances/PATtupleProduction UserCode/ExoDiBosonResonances/PATtupleProduction 

# Quark-gluon tagging
git clone git@github.com:amarini/QuarkGluonTagger.git
cd QuarkGluonTagger
git checkout v1-2-5
cd ..

echo " "
echo "> Launching compilation of CMSSW packages"
echo " "

scramv1 b -j 6

echo " "
echo "> Compilation finished"
echo " "
echo "> Launching compilation of libNTuple"
echo " "

cd IPHCDataFormat/NTFormat/src
make 
cd ../../..

echo " "
echo "> Compilation finished"
echo " "

echo " "
echo "##############################################"
echo "#           Installation completed.          #"
echo "#                 Have fun !                 #"
echo "##############################################"
echo " "
