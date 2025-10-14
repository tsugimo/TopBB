
import os
import tomllib

from .ham import HAM

### class of Hamiltonian
class KitaevChain:
  def __init__(self, ipara: str | dict, ikey: str = 'KitaevChain'): # ipara is toml-file name or dict

    self.tom: dict = None # To avoid confusing scope
    if type(ipara) is str: # input form file 
      assert os.path.exists(ipara), f"ERROR: Input file NOT exist '{ipara}'. <class KitaevChain>"
      with open(ipara, mode="rb") as f:
        self.tom = tomllib.load(f)[ikey]
    else:  # input from dict
      self.tom = ipara[ikey]

    # system size
    self.lss = self.tom['LSS']

    # boundary condition
    self.bdc = self.tom['BDC']

    # parity; False(0) = even, True(1) = Odd; For PBC and initial state
    self.par = self.tom['PAR']

    # coupling const {'t1': **, 'D1': **, 'V1': **, 'mu': **}
    self.cpc = self.tom['CPC']

    # make parity subspace
    self.sbs = []
    for i in range(2 ** self.lss):
      if bin(i)[2:].count('1') % 2 == self.par:
        self.sbs.append(i)


  def __str__(self):
    txt = "[KitaevChain]\n"
    txt += "# system size\n"
    txt += f"  LSS = {self.lss}\n"
    txt += "# Boundary condition\n"
    txt += f"  BDC = {self.bdc}\n"
    txt += "# parity\n"
    txt += f"  PAR = {self.par}\n"
    txt += "# Coupling constatnts\n"
    txt += f"  CPC = {self.cpc}\n"
    return txt
  
  def ham(self) -> dict:
    # temporary use
    lss = self.lss
    t1 = self.cpc['t1']
    D1 = self.cpc['D1']
    V1 = self.cpc['V1']
    mu = self.cpc['mu']

    htom: dict = {'HAM': {}}
    htom['HAM']['LSS'] = lss
    htom['HAM']['TRM'] = []
    for n in range(lss-1):
      # X X terms
      htom['HAM']['TRM'].append([-2 * (t1 + D1), [n, n+1], [1, 1]])
      # Y Y terms
      htom['HAM']['TRM'].append([-2 * (t1 - D1), [n, n+1], [2, 2]])
      # Z Z terms
      htom['HAM']['TRM'].append([-V1, [n, n+1], [3, 3]])
    for n in range(lss):
      # Hz terms
      htom['HAM']['TRM'].append([-mu, [n], [3]])

    if self.bdc == 'PBC':
      if self.par == False: # even parity
        # X X terms
        htom['HAM']['TRM'].append([2 * (t1 + D1), [0, lss-1], [1, 1]])
        # Y Y terms
        htom['HAM']['TRM'].append([2 * (t1 - D1), [0, lss-1], [2, 2]])
      else: # odd parity
        # X X terms
        htom['HAM']['TRM'].append([-2 * (t1 + D1), [0, lss-1], [1, 1]])
        # Y Y terms
        htom['HAM']['TRM'].append([-2 * (t1 - D1), [0, lss-1], [2, 2]])

      # Z Z term NOT depend on parity
      htom['HAM']['TRM'].append([-V1, [0, lss-1], [3, 3]])

    return htom 
  

  def ans(self, mly: int = 1, qct: str = "Sequential", ins: int = None) -> dict:
    # temporary use
    lss = self.lss

    atom: dict = {'ANS': {}}
    atom['ANS']['LSS'] = lss
    atom['ANS']['MLY'] = mly

    if ins == None:
      ins = self.par
    atom['ANS']['INS'] = ins

    atom['ANS']['GTL'] = []
    if qct == 'Sequential':
      for n in range(lss-1):
        for s in range(3):
          atom['ANS']['GTL'].append(['P', '*', [n, n+1], [s, s]])

      if self.bdc == 'PBC':
        for s in range(3):
          atom['ANS']['GTL'].append(['P', '*', [0, lss-1], [s, s]])

      for n in range(lss):
        atom['ANS']['GTL'].append(['P', '*', [n], [3]])

    atom['ANS']['GTI'] = []
    atom['ANS']['GTF'] = []


    return atom 

