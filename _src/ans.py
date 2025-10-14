
import os
import copy
import qulacs
import tomllib
import math
import random


### class of ansatz
class ANS:
  def __init__(self, ipara: str | dict, ikey: str = 'ANS'): # ipara is toml-file name or ditc

    self.tom: dict = None # To avoid confusing scope
    if type(ipara) is str: # input form file 
      assert os.path.exists(ipara), f"ERROR: Input file NOT exist '{ipara}'. <class ANS>"
      with open(ipara, mode="rb") as f:
        self.tom = tomllib.load(f)[ikey]
    else:  # input from dict
      self.tom = ipara[ikey]

    # #(qubits)
    self.nqb = self.tom['NQB']

    # initial (classical) state; 2-bit string
    self.ins = self.tom['INS']

    # #(layers)
    self.mly = self.tom['MLY']

    # gates ["F"/"P", initial angles, site# list, Pauli index list]
    # "F": fixed / "P": param., Pauli index (0: I, 1: X, 2: Y, 3: Z) 
    gtl = self.tom['GTL'] # layered gates
    gti = self.tom['GTI'] # initial gates
    gtf = self.tom['GTF'] # final gates

    # merge all gates into gta with MLY = 1.
    # causion: direct connection of list makes duplication of references 
    self.gta = copy.deepcopy(gti)
    for i in range(self.mly):
      self.gta += copy.deepcopy(gtl)
    self.gta += copy.deepcopy(gtf)

    # make circuit
    random.seed()
    self.aqc = qulacs.ParametricQuantumCircuit(self.nqb)
    for g in self.gta:
      if g[0] == "F":
        self.aqc.add_multi_Pauli_rotation_gate(g[2],g[3],g[1])
      else: # parametric gate
        if g[1] == "*": # random initial angle
          self.aqc.add_parametric_multi_Pauli_rotation_gate(g[2],g[3],random.uniform(0.0, 4 * math.pi))
        else:
          self.aqc.add_parametric_multi_Pauli_rotation_gate(g[2],g[3],g[1])

    txt = "[InitANS]\n"
    txt += f"  #(qubits) = {self.nqb}\n"
    txt += f"  InitialState = 0b{self.ins:0{self.nqb}b}\n"
    txt += f"  #(Layers) = {self.mly}\n"
    txt += f"  #(LayeredGates) = {len(gtl)}\n"
    txt += f"  #(InitialGates) = {len(gti)}\n"
    txt += f"  #(FinalGates) = {len(gtf)}\n"
    txt += f"  #(Parameters) = {self.aqc.get_parameter_count()}\n"
    print(txt)

  def __str__(self):
    self.aqc2gta()

    txt = "[ANS]\n"
    txt += "# #(qubits)\n"
    txt += f"  NQB = {self.nqb}\n"
    txt += "# initial state (2-bit repr.)\n"
    txt += f"  INS = 0b{self.ins:0{self.nqb}b}\n"
    txt += "# #(layers)\n"
    txt += f"  MLY = 1\n"
    txt += "# set of layered gates (1 layer)\n"
    txt += f"  GTL = {self.gta}\n"
    txt += "# set of initial gates; not repeated\n"
    txt += f"  GTI = []\n"
    txt += "# set of final gates; not repeated\n"
    txt += f"  GTF = []\n"
    return txt


  def get_par(self) -> list:
    # set initial params. except for fixed para.
    par = []
    for i in range(self.aqc.get_parameter_count()):
      par.append(self.aqc.get_parameter(i))

    return par
  
  def set_par(self, par: list):
    assert len(par) == self.aqc.get_parameter_count(), f"ERROR: #(params) is NOR consistent. set_par in <class ANS>"

    # set parameters except for fixed para.
    for i, p in enumerate(par):
      self.aqc.set_parameter(i, p)

  def aqc2gta(self):
    # set current parrams. to gta from aqc
    i = 0
    for g in self.gta:
      if g[0] == "P":
        g[1] = self.aqc.get_parameter(i)
        i += 1

  def get_state(self) -> qulacs.QuantumState:
    # set initial state
    st = qulacs.QuantumState(self.nqb)
    st.set_computational_basis(self.ins)

    # apply gate & get exp. value
    self.aqc.update_quantum_state(st)
    return st
