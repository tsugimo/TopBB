
import os
import qulacs
import tomllib

import scipy.sparse as sparse


### class of Hamiltonian
class HAM:
  def __init__(self, ipara: str | dict, ikey: str = 'HAM'): # ipara is toml-file name or dict

    self.tom: dict = None # To avoid confusing scope
    if type(ipara) is str: # input form file 
      assert os.path.exists(ipara), f"ERROR: Input file NOT exist '{ipara}'. <class HAM>"
      with open(ipara, mode="rb") as f:
        self.tom = tomllib.load(f)[ikey]
    else:  # input from dict
      self.tom = ipara[ikey]

    # system size
    self.lss = self.tom['LSS'] 

    # terms; [coupling const., site# list, Pauli index list]
    # Pauli index (0: I, 1: X, 2: Y, 3: Z)
    self.trm = self.tom['TRM']

    # for exact diag.
    self.eig = [[]]

    self.ope = qulacs.Observable(self.lss)
    pau = ["I", "X", "Y", "Z"]
    for cpl, sit, ops in self.trm:
      trm = ""
      for s, o in zip(sit, ops):
        trm += pau[o] + " " + str(s) + " "
      self.ope.add_operator(cpl, trm)

    txt = "[IniHAM]\n"
    txt += f"  SysSiz = {self.lss}\n"
    txt += f"  NTrm = {len(self.trm)}\n"
    print(txt)

  def __str__(self):
    txt = "[HAM]\n"
    txt += "# system size\n"
    txt += f"  LSS = {self.lss}\n"
    txt += "# terms; couplig const, site# list, Pauli indexes\n"
    txt += "# (0, I, 1: X, 2: Y, 3:Z)\n"
    txt += f"  TRM = {self.trm}\n"
    return txt
  
  def diag(self, omod = 1, k = 1, sbs = None, **args) -> tuple:

    if len(self.eig) < k:
      A = self.ope.get_matrix()
      self.eig = sparse.linalg.eigsh(A, k, which='SA', **args)

    if omod:
      print("[EigEne]")
      for i, en in enumerate(self.eig[0]):
        print(f"  {i} = {en}")
      print('')

    return self.eig

  def cale(self, st: qulacs.QuantumState) -> float:
      return self.ope.get_expectation_value(st)

