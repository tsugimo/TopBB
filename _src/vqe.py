
import os
import copy
import tomllib
import numpy

from scipy import optimize

from .ham import HAM
from .ans import ANS

### class of ansatz
class VQE:
  def __init__(self, ipara: str | dict, iham: str | dict | HAM = None, ians: str | dict | ANS = None, ikeys: list = ['VQE','HAM','ANS']):

    tom: dict = None # To avoid confusing scope
    if type(ipara) is str: # input form file 
      assert os.path.exists(ipara), f"ERROR: Input file NOT exist '{ipara}'. <class VQE>"
      with open(ipara, mode="rb") as f:
        tom = tomllib.load(f)
    else:  # input from dict
      tom = ipara

    # init ham
    if iham == None:
      self.ham = HAM(tom, ikeys[1])
    elif type(iham) is str:
      assert os.path.exists(iham), f"ERROR: Input file for ham NOT exist '{iham}'. <class VQE>"
      with open(iham, mode="rb") as f:
        htom = tomllib.load(f)
      self.ham = HAM(htom, ikeys[1])
    elif type(iham) is dict:
      self.ham = HAM(iham, ikeys[1])
    else: # type is HAM
      self.ham = copy.deepcopy(iham) # not changed in vqe

    # init ans
    if ians == None:
      self.ans = ANS(tom, ikeys[2])
    elif type(ians) is str:
      assert os.path.exists(ians), f"ERROR: Input file for ham NOT exist '{iham}'. <class VQE>"
      with open(ians, mode="rb") as f:
        atom = tomllib.load(f)
      self.ans = ANS(atom, ikeys[2])
    elif type(ians) is dict:
      self.ans = ANS(ians, ikeys[2])
    else: # type is ANS
      self.ans = copy.deepcopy(ians) # not changed in vqe

    # System size consistency
    assert self.ham.lss == self.ans.lss, f"ERROR: System size is NOT consistent. <class VQE>"

    self.tom = tom[ikeys[0]]
    # maximal # of minimize ite.
    self.mit = self.tom['MIT'] 
    # tics # in each minimize ite. 
    self.tit = self.tom['TIT'] 
    # tolerant error  
    self.tol = self.tom['TOL'] 
    # energy trajectory in bfgs
    self.etb = []

    txt = "[IniVQE]\n"
    txt += f"  MaxNIte = {self.mit}\n"
    txt += f"  TicNIte = {self.tit}\n"
    txt += f"  TolErr = {self.tol}\n"
    print(txt)


  def __str__(self):
    txt = "[VQE]\n"
    txt += "# maximal # of minimize ite.\n"
    txt += f"  MIT = {self.mit}\n"
    txt += "# tics # in each minimize ite.\n"
    txt += f"  TIT = {self.tit}\n"
    txt += "# tolerence error\n"
    txt += f"  TOL = {self.tol}\n"
    return txt

  
  # calc. energy
  def cale(self, par: list) -> float:
    # set params in ans.aqc
    self.ans.set_par(par)

    return self.ham.cale(self.ans.get_state())
    

  # calc infidelity of eigenstate b/w VQE & ED
  def ifid(self) -> float:
    self.ham.diag(omod = 0, k = 1)
    return 1.0 - abs(numpy.vdot(self.ans.get_state().get_vector(), numpy.transpose(self.ham.eig[1])[0]))


  def bfgs(self):
    print("[BFGS]")
    par = self.ans.get_par()
    ene = self.cale(par)
    print(f"  [BFGS.In]")
    print(f"    Ene = {ene}")
    print(f"    Par = {par}")      

    def cb(intermediate_result: optimize.OptimizeResult):
      self.etb.append(intermediate_result.fun)

    min_args = dict(
      method = "L-BFGS-B",
      tol = self.tol,
      options = {"maxiter": self.tit},
      callback = cb
    )

    # main iterations
    npar = numpy.array(par)
    for n in range(self.mit):
      res = optimize.minimize(self.cale, npar, **min_args)
      npar = res.x
      ene = res.fun 
      print(f"  [BFGS.Stp{n}]")
      print(f"    Ene = {ene}")
      print(f"    Dif = {res.fun - ene}")

    par = npar.tolist()
    print(f"  [BFGS.Res]")
    print(f"    Stp = {n}")
    print(f"    Ene = {ene}")
    #print(f"    Inf = {self.ifid()}")     
    print(f"    Par = {par}")
    print("")



if __name__ == "__main__":

  ln = """
########################
### VQE calc. starts ###
########################
"""
  print(ln)

  vqe = VQE("para.toml")

  vqe.bfgs()
  print(vqe.ans)