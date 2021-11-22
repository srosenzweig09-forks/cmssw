import FWCore.ParameterSet.Config as cms

import sys
from Configuration.Eras.Era_Run3_cff import Run3
process = cms.Process("L1TStage2DQM", Run3)

unitTest = False
if 'unitTest=True' in sys.argv:
    unitTest=True

#--------------------------------------------------
# Event Source and Condition

# hack to put the source file here
process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring("file:/eos/cms/store/data/Commissioning2021/Cosmics/RAW/v1/000/345/823/00000/7f9ccd7b-11df-4aea-8f30-2a6b656313bf.root",)
#    fileNames = cms.untracked.vstring("/store/relval/CMSSW_11_0_0/RelValDisplacedMuPt10To30/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/47F006BA-915E-9940-B7D3-04E59C255A1F.root",)
   fileNames = cms.untracked.vstring("file:/eos/cms/store/relval/CMSSW_12_2_0_pre2/RelValDisplacedSUSY_14TeV/GEN-SIM-DIGI-RAW/122X_mcRun3_2021_realistic_v1_HighStat-v1/2580000/fd4d2a88-69af-43f5-a80b-94c5b95a71ba.root",)

   )

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)         

# if unitTest:
#     process.load("DQM.Integration.config.unittestinputsource_cfi")
#     from DQM.Integration.config.unittestinputsource_cfi import options
# else:
#     # Live Online DQM in P5
#     process.load("DQM.Integration.config.inputsource_cfi")
#     from DQM.Integration.config.inputsource_cfi import options

# # Testing in lxplus
# process.load("DQM.Integration.config.fileinputsource_cfi")
# from DQM.Integration.config.fileinputsource_cfi import options
# process.load("FWCore.MessageLogger.MessageLogger_cfi")
# process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Required to load Global Tag
process.load("DQM.Integration.config.FrontierCondition_GT_cfi") 

# # Condition for lxplus: change and possibly customise the GT
from Configuration.AlCa.GlobalTag import GlobalTag as gtCustomise
process.GlobalTag = gtCustomise(process.GlobalTag, '122X_mcRun3_2021_realistic_v1', '')

# Required to load EcalMappingRecord
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")

#--------------------------------------------------
# DQM Environment

process.load("DQM.Integration.config.environment_cfi")

process.dqmEnv.subSystemFolder = "L1T"
process.dqmSaver.tag = "L1T"
# process.dqmSaver.runNumber = options.runNumber
process.dqmSaverPB.tag = "L1T"
# process.dqmSaverPB.runNumber = options.runNumber

process.dqmEndPath = cms.EndPath(process.dqmEnv * process.dqmSaver * process.dqmSaverPB)

#--------------------------------------------------
# Standard Unpacking Path

process.load("Configuration.StandardSequences.RawToDigi_cff")    

# remove unneeded unpackers
# process.RawToDigi.remove(process.ecalPreshowerDigis)
# process.RawToDigi.remove(process.muonCSCDigis)
# process.RawToDigi.remove(process.muonDTDigis)
# process.RawToDigi.remove(process.muonRPCDigis)
# process.RawToDigi.remove(process.siPixelDigis)
# process.RawToDigi.remove(process.siStripDigis)
# process.RawToDigi.remove(process.castorDigis)
# process.RawToDigi.remove(process.scalersRawToDigi)
# process.RawToDigi.remove(process.tcdsDigis)
# process.RawToDigi.remove(process.totemTriggerRawToDigi)
# process.RawToDigi.remove(process.totemRPRawToDigi)
# process.RawToDigi.remove(process.ctppsDiamondRawToDigi)
# process.RawToDigi.remove(process.ctppsPixelDigis)

process.rawToDigiPath = cms.Path(process.RawToDigi)

#--------------------------------------------------
# Stage2 Unpacker and DQM Path

# Filter fat events
from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.hltFatEventFilter = hltHighLevel.clone(
  throw = False,
# HLT_Physics now has the event % 107 filter as well as L1FatEvents
  HLTPaths = ['HLT_L1FatEvents_v*', 'HLT_Physics_v*']
)

# This can be used if HLT filter not available in a run
process.selfFatEventFilter = cms.EDFilter("HLTL1NumberFilter",
        invert = cms.bool(False),
        period = cms.uint32(107),
        rawInput = cms.InputTag("rawDataCollector"),
        fedId = cms.int32(1024)
        )

process.load("DQM.L1TMonitor.L1TStage2_cff")

process.l1tMonitorPath = cms.Path(
    process.l1tStage2OnlineDQM) # +
    # process.hltFatEventFilter +
#    process.selfFatEventFilter +
    # process.l1tStage2OnlineDQMValidationEvents
# )

# Remove DQM Modules
#process.l1tStage2OnlineDQM.remove(process.l1tStage2CaloLayer1)
#process.l1tStage2OnlineDQM.remove(process.l1tStage2CaloLayer2)
#process.l1tStage2OnlineDQM.remove(process.l1tStage2Bmtf)
#process.l1tStage2OnlineDQM.remove(process.l1tStage2Emtf)
#process.l1tStage2OnlineDQM.remove(process.l1tStage2uGMT)
#process.l1tStage2OnlineDQM.remove(process.l1tStage2uGt)

#--------------------------------------------------
# Stage2 Quality Tests
process.load("DQM.L1TMonitorClient.L1TStage2MonitorClient_cff")
process.l1tStage2MonitorClientPath = cms.Path(process.l1tStage2MonitorClient)

#--------------------------------------------------
# Customize for other type of runs

# # Cosmic run
# if (process.runType.getRunType() == process.runType.cosmic_run):
#     # Remove Quality Tests for L1T Muon Subsystems since they are not optimized yet for cosmics
#     process.l1tStage2MonitorClient.remove(process.l1TStage2uGMTQualityTests)
#     process.l1tStage2MonitorClient.remove(process.l1TStage2EMTFQualityTests)
#     #process.l1tStage2MonitorClient.remove(process.l1TStage2OMTFQualityTests)
#     process.l1tStage2MonitorClient.remove(process.l1TStage2BMTFQualityTests)
#     process.l1tStage2MonitorClient.remove(process.l1TStage2MuonQualityTestsCollisions)
#     process.l1tStage2EventInfoClient.DisableL1Systems = ["EMTF", "OMTF", "BMTF", "uGMT"]

# # Heavy-Ion run
# if (process.runType.getRunType() == process.runType.hi_run):
#     process.onlineMetaDataDigis.onlineMetaDataInputLabel = "rawDataRepacker"
#     process.onlineMetaDataRawToDigi.onlineMetaDataInputLabel = "rawDataRepacker"
#     process.castorDigis.InputLabel = "rawDataRepacker"
#     process.ctppsDiamondRawToDigi.rawDataTag = "rawDataRepacker"
#     process.ctppsPixelDigis.inputLabel = "rawDataRepacker"
#     process.ecalDigis.cpu.InputLabel = "rawDataRepacker"
#     process.ecalPreshowerDigis.sourceTag = "rawDataRepacker"
#     process.hcalDigis.InputLabel = "rawDataRepacker"
#     process.muonCSCDigis.InputObjects = "rawDataRepacker"
#     process.muonDTDigis.inputLabel = "rawDataRepacker"
#     process.muonRPCDigis.InputLabel = "rawDataRepacker"
#     process.muonGEMDigis.InputLabel = "rawDataRepacker"
#     process.scalersRawToDigi.scalersInputTag = "rawDataRepacker"
#     process.siPixelDigis.cpu.InputLabel = "rawDataRepacker"
#     process.siStripDigis.ProductLabel = "rawDataRepacker"
#     process.tcdsDigis.InputLabel = "rawDataRepacker"
#     process.tcdsRawToDigi.InputLabel = "rawDataRepacker"
#     process.totemRPRawToDigi.rawDataTag = "rawDataRepacker"
#     process.totemTriggerRawToDigi.rawDataTag = "rawDataRepacker"
#     process.totemTimingRawToDigi.rawDataTag = "rawDataRepacker"
#     process.csctfDigis.producer = "rawDataRepacker"
#     process.dttfDigis.DTTF_FED_Source = "rawDataRepacker"
#     process.gctDigis.inputLabel = "rawDataRepacker"
#     process.gtDigis.DaqGtInputTag = "rawDataRepacker"
#     process.twinMuxStage2Digis.DTTM7_FED_Source = "rawDataRepacker"
#     process.bmtfDigis.InputLabel = "rawDataRepacker"
#     process.omtfStage2Digis.inputLabel = "rawDataRepacker"
#     process.emtfStage2Digis.InputLabel = "rawDataRepacker"
#     process.gmtStage2Digis.InputLabel = "rawDataRepacker"
#     process.caloLayer1Digis.InputLabel = "rawDataRepacker"
#     process.caloStage1Digis.InputLabel = "rawDataRepacker"
#     process.caloStage2Digis.InputLabel = "rawDataRepacker"
#     process.gtStage2Digis.InputLabel = "rawDataRepacker"
#     process.l1tStage2CaloLayer1.fedRawDataLabel = "rawDataRepacker"
#     process.l1tStage2uGMTZeroSupp.rawData = "rawDataRepacker"
#     process.l1tStage2uGMTZeroSuppFatEvts.rawData = "rawDataRepacker"
#     process.l1tStage2BmtfZeroSupp.rawData = "rawDataRepacker"
#     process.l1tStage2BmtfZeroSuppFatEvts.rawData = "rawDataRepacker"
#     process.selfFatEventFilter.rawInput = "rawDataRepacker"
#     process.rpcTwinMuxRawToDigi.inputTag = "rawDataRepacker"
#     process.rpcCPPFRawToDigi.inputTag = "rawDataRepacker"

#--------------------------------------------------
# L1T Online DQM Schedule

process.load('L1Trigger.L1TMuonEndCap.simEmtfDigis_cfi')
process.load('L1Trigger.CSCTriggerPrimitives.cscTriggerPrimitiveDigis_cfi')
process.simCscTriggerPrimitiveDigis = process.cscTriggerPrimitiveDigis.clone()
process.simCscTriggerPrimitiveDigis.CSCComparatorDigiProducer = cms.InputTag('muonCSCDigis', 'MuonCSCComparatorDigi')
process.simCscTriggerPrimitiveDigis.CSCWireDigiProducer       = cms.InputTag('muonCSCDigis', 'MuonCSCWireDigi')
process.l1tStage2Emtf.emtfSource = cms.InputTag("simEmtfDigis")
process.simCscTriggerPrimitiveDigis.GEMPadDigiProducer       = cms.InputTag('muonGEMPadDigis')
process.simCscTriggerPrimitiveDigis.GEMPadDigiClusterProducer       = cms.InputTag('muonGEMPadDigiClusters')

reEmulation = cms.Sequence(
process.simCscTriggerPrimitiveDigis +
process.simEmtfDigis
)

process.reEmulStep = cms.Path(reEmulation)

process.schedule = cms.Schedule(
    process.rawToDigiPath,
    process.reEmulStep,
    process.l1tMonitorPath,
    process.l1tStage2MonitorClientPath,
#    process.l1tMonitorEndPath,
    process.dqmEndPath
)

#--------------------------------------------------
# Process Customizations

from DQM.Integration.config.online_customizations_cfi import *
process = customise(process)
print("Final Source settings:", process.source)
