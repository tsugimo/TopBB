
from _src.sys1d import KitaevChain
from _src.vqe import VQE
from matplotlib import pyplot


if __name__ == "__main__":

  # read-in Ham. paras of Kitaev chain
  kc = KitaevChain("para.toml")
  print(kc)

  # prep. VQE 
  vqe = VQE("para.toml", kc.ham(), kc.ans(mly=2))
  print(vqe)

  # exact diag. (option)
  vqe.ham.diag(omod=1,k=3)

  # exec. VQE
  vqe.bfgs()
  print(vqe.ans)

  # plot VQE convergence
  pyplot.figure(figsize=(8, 6))
  ax = pyplot.gca()
  ax.set_title('Energy convergence in VQE')
  ax.set_xlabel('BFGS steps')
  ax.set_ylabel('Energy diff. from exact value')

  ax.semilogy(range(len(vqe.etb)), [n - vqe.ham.eig[0][0] for n in vqe.etb]) 
  pyplot.show()

  print(vqe.etb)