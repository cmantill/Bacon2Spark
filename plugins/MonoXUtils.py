#!/usr/bin/env python

# -------------------------------------
# Various functions for Mono-X analysis
# -------------------------------------

# --------------------------------------------------------------------------------------------------
def passJet04Sel(jet):
    # Loose PFJet ID
    if(jet.neuHadFrac >= 0.99): return False
    if(jet.neuEmFrac  >= 0.99): return False
    if(jet.nParticles <= 1):    return False
    if(jet.muonFrac   >= 0.8):  return False
    if (abs(jet.eta)<2.4):
        if(jet.chHadFrac == 0):    return False
        if(jet.nCharged  == 0):    return False
        if(jet.chEmFrac  >= 0.99): return False
    # PU Jet ID
    if (0    <= abs(jet.eta) and abs(jet.eta) < 2.5  and jet.mva < -0.63): return False
    elif(2.5  <= abs(jet.eta) and abs(jet.eta) < 2.75 and jet.mva < -0.60): return False
    elif(2.75 <= abs(jet.eta) and abs(jet.eta) < 3    and jet.mva < -0.55): return False
    elif(3    <= abs(jet.eta) and abs(jet.eta) < 5    and jet.mva < -0.45): return False
    
    return True

# --------------------------------------------------------------------------------------------------
def passJetLooseSel(jet):
    # Loose PFJet ID                                                                                                                                                     
    if(jet.neuHadFrac >= 0.99)    : return False
    if(jet.neuEmFrac  >= 0.99)    : return False
    if(jet.nParticles <= 1)       : return False
    if(fabs(jet.eta)<2.4)
        if(jet.chHadFrac == 0)    : return False
        if(jet.nCharged  == 0)    : return False
        if(jet.chEmFrac  >= 0.99) : return False
    return True

# --------------------------------------------------------------------------------------------------
def eleEffArea(eta): 
    # effective area for PU correction
    # (see slide 4 of https://indico.cern.ch/event/370494/contribution/2/material/slides/0.pdf)                                                                                                                                    
    if  (abs(eta) >= 0.0 and abs(eta) < 0.8) : return 0.1752
    elif(abs(eta) >= 0.8 and abs(eta) < 1.3) : return 0.1862
    elif(abs(eta) >= 1.3 and abs(eta) < 2.0) : return 0.1411
    elif(abs(eta) >= 2.0 and abs(eta) < 2.2) : return 0.1534
    elif(abs(eta) >= 2.2 and abs(eta) < 2.3) : return 0.1903
    elif(abs(eta) >= 2.3 and abs(eta) < 2.4) : return 0.2243
    else                                     : return 0.2687

# --------------------------------------------------------------------------------------------------
def phoEffArea(eta, photype):
    # effective area for PU correction                                                                                                                                                                         
    # (https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonIdentificationRun2#Pointers_for_PHYS14_selection_im)                                                                  

    kCH_HAD  = 0
    kNEU_HAD = 1
    kPHOTON  = 2
    
    if(photype==kCH_HAD):
        if  (abs(eta) >= 0.0   and abs(eta) < 1.0)   : return 0.0157
        elif(abs(eta) >= 1.0   and abs(eta) < 1.479) : return 0.0143
        elif(abs(eta) >= 1.479 and abs(eta) < 2.0)   : return 0.0115
        elif(abs(eta) >= 2.0   and abs(eta) < 2.2)   : return 0.0094
        elif(abs(eta) >= 2.2   and abs(eta) < 2.3)   : return 0.0095
        elif(abs(eta) >= 2.3   and abs(eta) < 2.4)   : return 0.0068
        else                                         : return 0.0053
    elif(photype==kNEU_HAD):
        if  (abs(eta) >= 0.0   and abs(eta) < 1.0)   : return 0.0143
        elif(abs(eta) >= 1.0   and abs(eta) < 1.479) : return 0.0210
        elif(abs(eta) >= 1.479 and abs(eta) < 2.0)   : return 0.0147
        elif(abs(eta) >= 2.0   and abs(eta) < 2.2)   : return 0.0082
        elif(abs(eta) >= 2.2   and abs(eta) < 2.3)   : return 0.0124
        elif(abs(eta) >= 2.3   and abs(eta) < 2.4)   : return 0.0186
        else                                         : return 0.0320
    elif(photype==kPHOTON):
        if  (abs(eta) >= 0.0   and abs(eta) < 1.0)   : return 0.0725
        elif(abs(eta) >= 1.0   and abs(eta) < 1.479) : return 0.0604
        elif(abs(eta) >= 1.479 and abs(eta) < 2.0)   : return 0.0320
        elif(abs(eta) >= 2.0   and abs(eta) < 2.2)   : return 0.0512
        elif(abs(eta) >= 2.2   and abs(eta) < 2.3)   : return 0.0766
        elif(abs(eta) >= 2.3   and abs(eta) < 2.4)   : return 0.0949
        else                                         : return 0.1160
    else: 
        assert(0)

# --------------------------------------------------------------------------------------------------
def phoEffAreaHighPt(eta, photype):
    # effective area for PU correction                                                                                                                                                  
    # (https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonIdentificationRun2#Pointers_for_PHYS14_selection_im)                                                                                                                 
    kPHOTON  = 2
    
    if(photype==kPHOTON):
        if  (abs(eta) >= 0.0   && abs(eta) < 1.0)   : return 0.17    
        elif(abs(eta) >= 1.0   && abs(eta) < 1.479) : return 0.14
        elif(abs(eta) >= 1.479 && abs(eta) < 2.0)   : return 0.11
        elif(abs(eta) >= 2.0   && abs(eta) < 2.2)   : return 0.14
        else                                        : return 0.22
    else:
        assert(0)

# --------------------------------------------------------------------------------------------------
def passMuonLooseSel(muon):
    if(!(muon.pogIDBits & kPOGLooseMuon)): return False
    # PF-isolation with Delta-beta correction                                                                                                                                                  
    iso = muon.chHadIso + max(muon.neuHadIso + muon.gammaIso - 0.5*(muon.puIso), 0)
    if(iso >= 0.2*(muon.pt)): return False

  return True

# -------------------------------------------------------------------------------------------------
