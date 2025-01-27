import FWCore.ParameterSet.Config as cms

from Validation.MuonGEMHits.MuonGEMHits_cff import *
from Validation.MuonGEMDigis.MuonGEMDigis_cff import *
from Validation.MuonGEMRecHits.MuonGEMRecHits_cff import *
from DQM.GEM.GEMDQM_cff import *

GEMDigiSource.modeRelVal = True
GEMRecHitSource.modeRelVal = True

gemSimValid = cms.Sequence(GEMDQMForRelval*gemSimValidation*gemDigiValidation*gemLocalRecoValidation)
