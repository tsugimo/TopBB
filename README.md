# TopBB
トポロジカル物性解析のための量子計算フレンドリなpythonコードです。
現在、VQEと動的相関関数の計算ができるようになっています。
今後、より発展的なアルゴリズムを実装していく予定です。

## Usage
- _src を置いたディレクトリ内に、para.toml と main.py を用意します。
- そのディレクトリを、カレントディレクトリとして、main.py を python で実行します。
- para.toml を入力ファイルとして使います。記述方法は、以下に示します。
 (python 3.11 以降を推奨します。3.10 以前のバージョンに関しては、toml をインストールしてください。)
- ライブラリとして、qulacs および scipy など、可視化に matplotlib などを使用します。

## Output
- 厳密対角化によって得られた基底状態エネルギーとの差分を、VQEステップに対してプロットした図を返す。
- 標準出力として、詳細なステップごとの結果と、最終的に得られたアンザツパラメータを返す。

## Example
### para.toml for (Interacting) Kitaev chain model

```toml
[KitaevChain]
# system size
LSS = 8
# boundary condition
BDC = 'OBC'
# parity; 0: even, 1: odd (bool)
PAR = 0

# coupling constants
[KitaevChain.CPC]
# hopping integral
t1 = 1.0
# pairing potential
D1 = 0.3
# chemical potential
mu = 0.05
# Coulomb potential b/w neighboring sites
V1 = 0.1

[VQE]
# maximal # of minimize ite.
MIT = 10
# tics # in each minimize ite. 
TIT = 100
# tolerence error
TOL = 1.0e-6 
```

### main.py for (Interacting) Kitaev chain model

```python
from _src.sys1d import KitaevChain
from _src.vqe import VQE
from matplotlib import pyplot

# read-in Ham. para of Kitaev chain
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
```

### Result of VQE
<img width="800" height="600" alt="Figure1" src="https://github.com/user-attachments/assets/a3d3957a-6527-4ea4-ae58-ce1482a6b57a" />
