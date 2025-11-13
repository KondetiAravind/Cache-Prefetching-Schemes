# **Cache Prefetching Schemes**

### *Advanced Computer Architecture Laboratory Project*

**Students:** Kondeti Aravind (22CS02008), Gunupuru Sai Siddhartha (22CS02007)

---

## **1. Introduction**

This project investigates the impact of hardware-level cache prefetching mechanisms within the SimpleScalar out-of-order (sim-outorder) processor simulator.
The primary objective is to analyze how different prefetching strategies influence processor performance, cache behavior, and memory energy consumption.

By modifying the L1 cache modules to support specific prefetching algorithms and executing a diverse set of benchmarks, the study provides quantitative insight into memory latency reduction, cache efficiency, and the trade-offs between performance improvement and additional memory traffic.

---

## **2. Motivation**

Memory latency continues to be a critical bottleneck in modern superscalar processors. Although multi-level caches help minimize this latency, L1 cache misses still impose significant pipeline stalls.
Hardware prefetching is an effective strategy to mitigate this problem by **predicting future memory accesses** and **fetching blocks before they are demanded** by the processor.

The key motivations behind this project include:

* Understanding the effects of prefetching on real processor performance metrics (CPI, IPC).
* Studying how prefetching influences miss rates and AMAT.
* Quantifying energy consumption through CACTI-based modelling.
* Exploring trade-offs between prefetch aggressiveness and memory traffic overhead.

---

## **3. Prefetching Schemes Implemented**

### **1. Baseline (No Prefetching)**

Serves as a reference to measure the performance and energy benefits of prefetching.

### **2. Next-Line Prefetching**

Fetches the sequentially next cache block upon each access.
This scheme anticipates spatial locality and improves performance in sequential or streaming workloads.

### **3. One-Block Lookahead (OBL)**

Prefetches two blocks ahead of the current access.
OBL is more aggressive than Next-Line and is particularly effective in instruction-intensive sequential patterns.

---

## **4. Methodology**

The study follows a structured workflow:

**1. Integration into SimpleScalar:**
Prefetching logic was added to the L1 cache implementations (cache.c, cache.h).

**2. Benchmark Execution:**
Four benchmarks—*test-math*, *test-fmath*, *anagram*, and *test-llong*—were executed under:

* Baseline
* Next-Line Prefetching
* One-Block Lookahead Prefetching

**3. Statistics Extraction:**
Simulation logs were parsed to compute:

* Miss rates (IL1 and DL1)
* CPI and IPC
* Cycle counts
* AMAT (instruction and data caches)

**4. Energy Estimation Using CACTI:**
CACTI was used to extract per-access energy values for IL1, DL1, and L2 caches.
These values were combined with access counts to evaluate total energy expenditure.

**5. Comparative Analysis:**
All modes were compared in terms of performance improvement and energy cost.

---

## **5. Project Structure Overview**

* **simplescalar/simplesim-3.0/** — Modified simulator with integrated prefetching
* **tests/bin.little/** — Benchmarks used for evaluation
* **Memory_Modeling/scripts/** — Python scripts for statistics parsing and energy computation
* **CACTI/cacti/** — Energy modelling configuration and outputs
* **results/** — Simulation outputs and processed summary data
* **commands.txt** — Workflow documentation
* **Project_Report.pdf** — Complete technical report

---

## **6. Experimental Results**

The following tables present **real simulation results** obtained from your dataset.

---

### **6.1 Miss Rate Analysis**

Miss rates were computed from IL1 and DL1 access/miss counts.

#### **test-math**

| Mode      | IL1 Miss Rate | DL1 Miss Rate |
| --------- | ------------- | ------------- |
| Baseline  | 6.28%         | 0.97%         |
| Next-Line | 4.23%         | 0.53%         |
| One-Block | 4.94%         | 0.54%         |

#### **test-fmath**

| Mode      | IL1 Miss Rate | DL1 Miss Rate |
| --------- | ------------- | ------------- |
| Baseline  | 6.79%         | 2.89%         |
| Next-Line | 4.60%         | 1.58%         |
| One-Block | 5.20%         | 1.62%         |

#### **anagram**

| Mode      | IL1 Miss Rate | DL1 Miss Rate |
| --------- | ------------- | ------------- |
| Baseline  | 5.53%         | 10.47%        |
| Next-Line | 3.27%         | 5.41%         |
| One-Block | 3.63%         | 5.51%         |

#### **test-llong**

| Mode      | IL1 Miss Rate | DL1 Miss Rate |
| --------- | ------------- | ------------- |
| Baseline  | 2.93%         | 4.34%         |
| Next-Line | 1.91%         | 2.25%         |
| One-Block | 2.17%         | 2.32%         |

**Observation:**
Across all benchmarks, **Next-Line Prefetching** consistently achieves the lowest overall miss rates.

---

### **6.2 CPI and IPC Comparison**

| Benchmark  | Mode             | CPI               | IPC                   |
| ---------- | ---------------- | ----------------- | --------------------- |
| test-math  | Baseline: 1.0493 | Next-Line: 0.7923 | One-Block: **0.7828** |
|            | Baseline: 0.9530 | Next-Line: 1.2621 | One-Block: **1.2773** |
| test-fmath | Baseline: 1.2761 | Next-Line: 0.8856 | One-Block: **0.8430** |
|            | Baseline: 0.7836 | Next-Line: 1.1290 | One-Block: **1.1862** |
| anagram    | Baseline: 1.7977 | Next-Line: 1.0452 | One-Block: **0.9156** |
|            | Baseline: 0.5562 | Next-Line: 0.9567 | One-Block: **1.0920** |
| test-llong | Baseline: 1.0473 | Next-Line: 0.7868 | One-Block: **0.7500** |
|            | Baseline: 0.9547 | Next-Line: 1.2708 | One-Block: **1.3331** |

**Observation:**
**One-Block Lookahead** provides the highest IPC and lowest CPI across all benchmarks.

---

### **6.3 AMAT Analysis (Cycles)**

Instruction and data AMAT values taken directly from simulation:

* **test-math:**

  * IL1: Baseline 19.85 → Nextline 13.69 → Oneblock **15.81**
  * DL1: Baseline 3.90 → Nextline 2.60 → Oneblock **2.64**

* **test-fmath:**

  * IL1: Baseline 21.38 → Nextline 14.82 → Oneblock **16.59**
  * DL1: Baseline 9.69 → Nextline 5.75 → Oneblock **5.85**

* **anagram:**

  * IL1: Baseline 17.59 → Nextline 10.83 → Oneblock **11.91**
  * DL1: Baseline 32.41 → Nextline 17.25 → Oneblock **17.54**

* **test-llong:**

  * IL1: Baseline 9.81 → Nextline 6.73 → Oneblock **7.52**
  * DL1: Baseline 14.04 → Nextline 7.77 → Oneblock **7.96**

**Observation:**
Next-Line Prefetching tends to produce the lowest AMAT across benchmarks.

---

### **6.4 Total Energy Consumption (Joules)**

Values from your `total_energy_j` column:

| Benchmark  | Baseline   | Next-Line  | One-Block      |
| ---------- | ---------- | ---------- | -------------- |
| test-math  | 1.8229e-05 | 3.9771e-05 | **4.2349e-05** |
| test-fmath | 5.0276e-06 | 1.0907e-05 | **1.1506e-05** |
| anagram    | 1.0186e-06 | 2.0246e-06 | **2.0970e-06** |
| test-llong | 2.3537e-06 | 4.8172e-06 | **4.9740e-06** |

**Observation:**
Energy increases with prefetching due to additional memory accesses introduced by prefetch operations.

---

## **7. Key Findings**

* Prefetching substantially improves IPC and reduces CPI compared to baseline.
* Next-Line Prefetching achieves the lowest AMAT and lowest overall miss rates.
* One-Block Lookahead yields the highest performance (IPC/CPI).
* Prefetching introduces additional memory accesses, leading to **higher energy consumption**, as reflected in CACTI-based modelling.
* Overall, the results highlight a trade-off between **performance improvement** and **energy overhead**.

---

## **8. Conclusion**

The project successfully demonstrates the impact of hardware prefetching on cache efficiency and processor performance.
Through systematic experimentation on SimpleScalar and accurate energy modelling using CACTI, the study confirms that:

* Prefetching significantly reduces miss rates and improves processor throughput.
* One-Block Lookahead provides the greatest performance gains.
* Next-Line Prefetching lowers AMAT consistently.
* The energy overhead introduced by prefetching must be considered in real-world processor designs.

This work provides an in-depth practical understanding of memory hierarchy behavior and microarchitectural optimization techniques.

---

## **9. Acknowledgement**

We sincerely thank the faculty of the Advanced Computer Architecture Laboratory for their guidance and support throughout the execution of this project.
