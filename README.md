
# **Cache Prefetching Schemes — Advanced Computer Architecture Lab Project**

### **SimpleScalar ⬩ Hardware Prefetching ⬩ AMAT Modeling ⬩ CACTI energy analysis**

This repository implements and evaluates **hardware cache prefetching** inside the **SimpleScalar (sim-outorder)** superscalar pipeline simulator, combined with **memory modeling**, **AMAT computation**, and **CACTI-based energy estimation**.

The entire workflow—from simulator build → cache modification → benchmark execution → statistics extraction → AMAT/energy modeling → plotting—is fully automated and documented.

---

# 🚀 **Project Overview**

This project extends the SimpleScalar out-of-order simulator by integrating:

### ✔ **Prefetching Schemes Implemented**

| Scheme                        | Trigger             | Prefetch Action          | Target   |
| ----------------------------- | ------------------- | ------------------------ | -------- |
| **Baseline**                  | —                   | No prefetch              | IL1, DL1 |
| **Next-Line Prefetching**     | On every access     | Prefetch 1 next block    | IL1, DL1 |
| **One-Block Lookahead (OBL)** | On access/miss      | Prefetch 2 blocks ahead  | IL1      |
| **Stride Prefetching**        | When stride repeats | Prefetch `addr + stride` | IL1, DL1 |

All modifications occur inside:

```
cache.c
cache.h
```

which are supplied in the project root and **must be copied** into SimpleScalar before rebuild.

---

# 📂 **Directory Structure**

```
Cache_Prefetching_Schemes/
│
├── simplescalar/
│   └── simplesim-3.0/
│       ├── cache.c       ← Overwrite with modified version
│       ├── cache.h       ← Overwrite with modified version
│       ├── sim-outorder
│       ├── tests/bin.little/
│       │   ├── test-math
│       │   ├── test-fmath
│       │   ├── anagram
│       │   └── test-llong
│       └── Makefile
│
├── Memory_Modeling/
│   ├── scripts/
│   │   ├── parse_sim_stats.py
│   │   ├── compute_amat_and_energy.py
│   │   ├── merge_cacti_energy.py
│   │   └── plot_results.py
│   └── parsed/      ← JSON stats extracted from SimpleScalar
│
├── CACTI/
│   └── cacti/
│       ├── cacti
│       ├── il1.cfg
│       ├── dl1.cfg
│       └── l2.cfg
│
├── results/
│   ├── baseline_*.txt
│   ├── nextline_*.txt
│   ├── oneblock_*.txt
│   ├── summary_with_energy.csv
│   └── summary_with_energy_final.csv
│
├── il1.cfg
├── dl1.cfg
├── l2.cfg
├── cache.c
├── cache.h
├── commands.txt
└── README.md
```

---

# 🧩 **Phase 1 — Building SimpleScalar**

```
mkdir Cache_Prefetching_Schemes
cd Cache_Prefetching_Schemes

mkdir simplescalar
cd simplescalar

git clone https://github.com/toddmaustin/simplesim-3.0.git
cd simplesim-3.0

make config-pisa
make -j$(nproc)
cd ../../
```

---

# 🛠 **Phase 2 — Copy Modified cache.c & cache.h**

The project provides **modified cache.c & cache.h** (prefetch-enabled).
Copy them before rebuilding:

```
cp cache.c simplescalar/simplesim-3.0/cache.c
cp cache.h simplescalar/simplesim-3.0/cache.h

cd simplescalar/simplesim-3.0
make clean
make -j$(nproc)
cd ../../
```

This activates Next-Line, One-Block, and Stride Prefetchers.

---

# 🔬 **Phase 3 — Run Prefetching Experiments**

Benchmarks:

```
test-math
test-fmath
anagram
test-llong
```

### **Baseline (no prefetch)**

```
unset PREFETCH_MODE
./simplescalar/simplesim-3.0/sim-outorder -max:inst 5000000 -redir:sim results/baseline_test-math.txt simplescalar/simplesim-3.0/tests/bin.little/test-math
...
```

### **Next-Line Prefetch**

```
export PREFETCH_MODE=nextline
./simplescalar/simplesim-3.0/sim-outorder ...
```

### **One-Block Prefetch**

```
export PREFETCH_MODE=oneblock
./simplescalar/simplesim-3.0/sim-outorder ...
```

12 total results saved in `results/`.

---

# 📊 **Phase 4 — Parsing Stats + Computing AMAT + Energy**

### Parse SimpleScalar stats → JSON

```
python3 Memory_Modeling/scripts/parse_sim_stats.py --in results/baseline_test-math.txt --out Memory_Modeling/parsed/baseline_test-math.json
...
```

### Compute AMAT, CPI, IPC, Core Energy

```
python3 Memory_Modeling/scripts/compute_amat_and_energy.py --sim Memory_Modeling/parsed/baseline_test-math.json --out results/summary_with_energy.csv --benchmark test-math --mode baseline --freq 2.5e9 --mainmem_latency 300
...
```

Outputs:

```
summary_with_energy.csv
```

---

# ⚡ **Phase 5 — CACTI-Based IL1, DL1, L2 Energy Modeling**

### Clone & build CACTI

```
cd CACTI
git clone https://github.com/HewlettPackard/cacti.git
cd cacti
make
cd ../../
```

### Copy provided custom config files

```
cp il1.cfg CACTI/cacti/il1.cfg
cp dl1.cfg CACTI/cacti/dl1.cfg
cp l2.cfg CACTI/cacti/l2.cfg
```

### Run CACTI

```
cd CACTI/cacti
./cacti -infile il1.cfg > il1.out
./cacti -infile dl1.cfg > dl1.out
./cacti -infile l2.cfg  > l2.out
cd ../../
```

---

# 🔗 **Phase 6 — Merge CACTI Energy + Final CSV**

```
python3 Memory_Modeling/scripts/merge_cacti_energy.py \
   results/summary_with_energy.csv \
   results/summary_with_energy_final.csv \
   CACTI/cacti/il1.out \
   CACTI/cacti/dl1.out \
   CACTI/cacti/l2.out
```

Outputs:

```
summary_with_energy_final.csv
```

---

# 📈 **Phase 7 — Generate Plots**

```
python3 -m venv venv
source venv/bin/activate
pip install numpy pandas matplotlib

python Memory_Modeling/scripts/plot_results.py

deactivate
```

Generates:

* `plot_ipc.png`
* `plot_cpi.png`
* `plot_amat.png`
* `plot_energy.png`
* `plot_prefetch_effect.png`

---

# 🧾 **Results Summary**

### ✔ One-Block Prefetching gives the best IPC

### ✔ Next-Line gives moderate gains

### ✔ Prefetching reduces L1 miss rates up to **35–60%**

### ✔ OBL improves IPC by ~40–50% depending on benchmark

### ✔ Energy improves due to fewer stalls & lower cycles

### ✔ CACTI provides physical energy/area scaling based on 22nm model

All results are included in:

```
results/summary_with_energy_final.csv
results/*.png
```

---

# 📝 **Commands File**

The file `commands.txt` contains the entire reproducible workflow with every command used.

---

# 👨‍💻 **Authors**

**Kondeti Aravind (22CS02008)**
**Gunupuru Sai Siddhartha (22CS02007)**


If you want a **PDF report**, **LaTeX version**, or **auto-generated documentation**, I can prepare that too.
