
import os
import copy
import qulacs
import tomllib

from ham import HAM

### Trotter Time Evolution
class TTE:
  def __init__(self, ipara: str | dict, ham: HAM = None, ikeys: list = ['TTE','HAM']): # ipara is toml-file name or dict

    tom: dict = None # To avoid confusing scope
    if type(ipara) is str: # input form file 
      assert os.path.exists(ipara), f"ERROR: Input file NOT exist '{ipara}'. <class TTE>"
      with open(ipara, mode="rb") as f:
        tom = tomllib.load(f)
    else:  # input from dict
      tom = ipara

    # init ham
    if ham != None:
      self.ham = copy.deepcopy(ham)
    else:
      self.ham = HAM(tom, ikeys[1])

    tom = tom[ikeys[0]]
    # Dulation of time evolution
    self.dte = tom['DTE'] 
    # tics of time evolution, 1 time step 
    self.tte = tom['TTE'] 
    # order of applying terms of Hamiltonian (optional)
    self.oat = tom.get('OAT') if tom.get('OAT') != None else list(range(len(self.ham.trm)))

    # #(time steps)
    self.nts = int(self.dte / self.tte) 

    txt = "[InitTTE]\n"
    txt += f"  DulationOfTimeEvolution = {self.dte}\n"
    txt += f"  TicsOfTimeEvolution = {self.tte}\n"
    txt += f"  #(TimeSteps) = {self.nts}\n"
    txt += f"  OrderOfApplyingTerms = {self.oat}\n"
    print(txt)


  def __str__(self):
    txt = "[TTE]\n"
    txt += "# Dulation of time evolution\n"
    txt += f"  DTE = {self.tte}\n"
    txt += "# tics of time evolution; 1 time step\n"
    txt += f"  TTE = {self.tte}\n"
    txt += "# order of applying terms of Hamiltonian \n"
    txt += f"  OAT = {self.oat}\n"
    return txt
  
  # execution of time evolution
  def ete(self, st: qulacs.QuantumState, mod = True) -> qulacs.QuantumState:
    if mod == False: # st is NOT updated, time-evolved st is return value (rst)
      rst = copy.deepcopy(st)
    else: 
      rst = st

    for t in range(self.nts):
       for n in self.oat:
         trm = self.ham.trm[n]
         qulacs.gate.PauliRotation(trm[1], trm[2], -2.0 * trm[0] * self.tte).update_quantum_state(rst)

    return rst
  
  # dynamical correlation func.
  def dcf(self, st: qulacs.QuantumState, opl: qulacs.QuantumCircuit, opr: qulacs.QuantumCircuit) -> complex:

    ket = copy.deepcopy(st)
    opr.update_quantum_state(ket)

    for t in range(self.nts):
       for n in self.oat:
         trm = self.ham.trm[n]
         qulacs.gate.PauliRotation(trm[1], trm[2], -2.0 * trm[0] * self.tte).update_quantum_state(ket)

    opl.update_quantum_state(ket)

    return qulacs.state.inner_product(st, ket)



if __name__ == "__main__":

  ln = """
########################
### TTE calc. starts ###
########################
"""
  print(ln)
  
  tte = TTE("para.toml")

  # set initial state
  st = qulacs.QuantumState(tte.ham.lss)
  st.set_computational_basis(0)

  tte.ete(st)
  print(st)

  # set ops
  opl = qulacs.QuantumCircuit(tte.ham.lss)
  opl.add_gate(qulacs.gate.X(1))

  opr = qulacs.QuantumCircuit(tte.ham.lss)
  opr.add_gate(qulacs.gate.X(1))

  print(f"DCF <X_1(t)X_1>: {tte.dcf(st,opl,opr)}")