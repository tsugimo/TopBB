
from _src.sys1d import KitaevChain
from _src.vqe import VQE

import matplotlib.pyplot as plt


if __name__ == "__main__":

  kc = KitaevChain("para.toml")
  print(kc)

  vqe = VQE("para.toml", kc.ham(), kc.ans(mly=2))
  print(vqe)

  vqe.ham.diag(omod=1,k=3)

  vqe.bfgs()
  print(vqe.ans)

  plt.figure(figsize=(8, 6))
  ax = plt.gca()
  ax.set_title('Energy convergence in VQE')
  ax.set_xlabel('BFGS steps')
  ax.set_ylabel('Energy diff. from exact value')

  ax.semilogy(range(len(vqe.etb)), [n - vqe.ham.eig[0][0] for n in vqe.etb]) 
  plt.show()

  print(vqe.etb)