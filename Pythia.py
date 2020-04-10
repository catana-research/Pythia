# main34.py is a part of the PYTHIA event generator.
# Copyright (C) 2017 Torbjorn Sjostrand.
# PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.

# Author: Philip Ilten, March 2016.

# An example where the hard process (p p -> mu+ mu-) is automatically
# produced externally with MadGraph 5, read in, and the remainder of
# the event is then produced by Pythia (MPI, showers, hadronization,
# and decays). A comparison is made between events produced with
# Pythia at LO, MadGraph 5 at LO, and aMC@NLO at NLO.

# For this example to run, MadGraph 5 must be installed and the
# command "exe" (set by default as "mg5_aMC") must be available via
# the command line. Additionally, GZIP support must be enabled via
# the "--with-gzip" configuration option(s). Note that this example has
# only been tested with MadGraph 5 version 2.3.3; due to rapid
# MadGraph development, this example may not work with other
# versions. For more details on the LHAMadgraph class see the
# comments of Pythia8Plugins/LHAMadgraph.h.

# To set the path to the Pythia 8 Python interface do either (in a
# shell prompt):
#      export PYTHONPATH=$(PREFIX_LIB):$PYTHONPATH
# or the following which sets the path from within Python.
import sys
cfg = open('/home/tau/pythia8230/Makefile.inc')
lib = '/home/tau/pythia8230/lib'
for line in cfg:
    if line.startswith('PREFIX_LIB='): lib = line[11:-1]; break
sys.path.insert(0, lib)
import pythia8

#==========================================================================

# A simple method to run Pythia, analyze the events, and fill a histogram.

def run(pythia, nEvent):
  pythia.readString("Random:setSeed = on")
  pythia.readString("Random:seed = 1")
  pythia.init()
  for iEvent in range(0, nEvent):
      if not pythia.next(): continue
      iMu1 = 0; iMu2 = 0
      for prt in pythia.event:
          if not iMu1 and prt.id() == 13:  iMu1 = prt.index()
          if not iMu2 and prt.id() == -13: iMu2 = prt.index()
          if iMu1 and iMu2:
              iMu1 = pythia.event[iMu1].iBotCopyId()
              iMu2 = pythia.event[iMu2].iBotCopyId()
              #hist.fill((pythia.event[iMu1].p() + pythia.event[iMu2].p()).pT())
              break
  pythia.stat()


# Create the histograms.
#pyPtZ = pythia8.Hist("Pythia dN/dpTZ", 100, 0., 100.)


import pandas as pd
nEvent = 10000

selected_process = 'ffbar2gmZ'

Process = namedtuple('Process', ['process_string', 'match_particles', 'phase_space'], verbose=True)

processes = {}
processes['ffbar2gmZ'] = Process(process_string='WeakSingleBoson:ffbar2gmZ = on', match_particles='23:onIfMatch = -13 13', phase_space='PhaseSpace:mHatMin = 80.')
processes['ffbar2W']   = Process(process_string='WeakSingleBoson:ffbar2W = on',   match_particles='24:onIfAny = 13 14', phase_space='')
processes['ffbar2gmZ'] = Process(process_string='', match_particles='', phase_space='')
processes['ffbar2gmZ'] = Process(process_string='', match_particles='', phase_space='')
processes['ffbar2gmZ'] = Process(process_string='', match_particles='', phase_space='')
processes['ffbar2gmZ'] = Process(process_string='', match_particles='', phase_space='')



# Produce leading-order events with Pythia.
pythia = pythia8.Pythia()
pythia.readString("Beams:eCM = 13000.")




# Single Z production
pythia.readString("WeakSingleBoson:ffbar2gmZ = on") # ffbar -> gamma/Z (Drell-Yan)
pythia.readString("23:onMode = off")
pythia.readString("23:onIfMatch = -13 13")
pythia.readString("PhaseSpace:mHatMin = 80.")


# Single W production                                                                                                                                                                                                             
pythia.readString("WeakSingleBoson:ffbar2W = on");
# Force decay W->muv                                                                                                                                                                                                               
 pythia.readString("24:onMode = off");
  pythia.readString("24:onIfAny = 13 14");


run(pythia, nEvent)


# Print the histograms.
#print(pyPtZ)


# Store events to csv
d = []
full_hard_scatter = [21, 22, 23, 24] 
partial_hard_scatter = [22, 23] 
 
pdgid_selection = partial_hard_scatter
 
for iEvent in range(0, nEvent):
    for i, prt in enumerate(pythia.event):
        i_particle = -1
        if abs(prt.status()) in pdgid_selection: # Seelct particles from the hardscatter
            i_particle += 1
            d.append({'iEvent':iEvent, 'n':i_particle, 'id':prt.id(), 'name':prt.name(), 'status':prt.status(), 'charge':prt.charge(),
                      'px':prt.p().px(), 'py':prt.p().py(), 'pz':prt.p().pz(), 'e':prt.e(), 'm':prt.m(), 'eta':prt.eta(), 'phi':prt.phi(), 'pT':prt.pT(), 'eT':prt.eT()})
            pass
        pass
    pass


df = pd.DataFrame(d, columns=['iEvent', 'n', 'id', 'name', 'status', 'charge', 'px', 'py', 'pz', 'e', 'm', 'eta', 'phi', 'pT', 'eT'])
df.to_csv('/home/tau/Data/Pythia/DYmumubar_13TeV.csv')

