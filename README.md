# TopBB
量子計算機フレンドリなトポロジカル物性解析のためのpythonコードです。
現在、VQEと動的相関関数の計算ができるようになっています。
今後、より発展的なアルゴリズムを使いしていく予定です。

# Usage
- para.toml を入力ファイルとして使います。記述方法は、以下に示します。
- main.py を python で実行します。python 3.9 以降を推奨します。
- ライブラリとして、qulacs および scipy など、可視化に matplotlib などを使用します。

# Output
- 厳密対角化によって得られた基底状態エネルギーとの差分を、VQEステップに対してプロットした図を返す。
- 標準出力として、詳細なステップごとの結果と、最終的に得られたアンザツパラメータを返す。

# Example
## (Interacting) Kitaev chani model

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

## Result
<img width="800" height="600" alt="Figure1" src="https://github.com/user-attachments/assets/a3d3957a-6527-4ea4-ae58-ce1482a6b57a" />
