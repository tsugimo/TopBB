
from _src.sys1d import KitaevChain
from _src.vqe import VQE


if __name__ == "__main__":

  kc = KitaevChain("para.toml")

  print(kc)

  vqe = VQE("para.toml", kc.ham, )
