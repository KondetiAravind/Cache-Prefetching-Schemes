#!/usr/bin/env python3
import json
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--sim", required=True)
parser.add_argument("--out", required=True)
parser.add_argument("--benchmark", required=True)
parser.add_argument("--mode", required=True)
parser.add_argument("--freq", type=float, required=True)     # Hz
parser.add_argument("--mainmem_latency", type=float, required=True)   # cycles
args = parser.parse_args()

with open(args.sim) as f:
    sim = json.load(f)

# Frequency → seconds per cycle
sec_per_cycle = 1.0 / args.freq
ns_per_cycle = sec_per_cycle * 1e9

# Extract basic values
sim_inst  = sim.get("sim_num_insn", 0)
sim_cycle = sim.get("sim_cycle",    1)

CPI = sim_cycle / max(sim_inst, 1)
IPC = sim_inst / max(sim_cycle, 1)

cpu_time_s = sim_cycle * sec_per_cycle


# L1 Instruction Cache
il1_A = sim.get("il1.accesses", 0)
il1_M = sim.get("il1.misses",   0)
il1_hit_time = 1
il1_amat_cycles = il1_hit_time + (il1_M / max(il1_A,1)) * args.mainmem_latency
il1_amat_ns = il1_amat_cycles * ns_per_cycle

# L1 Data Cache
dl1_A = sim.get("dl1.accesses", 0)
dl1_M = sim.get("dl1.misses",   0)
dl1_hit_time = 1
dl1_amat_cycles = dl1_hit_time + (dl1_M / max(dl1_A,1)) * args.mainmem_latency
dl1_amat_ns = dl1_amat_cycles * ns_per_cycle

# Unified L2 Cache
l2_A = sim.get("ul2.accesses", 0)
l2_M = sim.get("ul2.misses",   0)

# DRAM dynamic energy placeholder (later overwritten by CACTI)
dram_energy_j = (l2_M * 2e-10)

row = {
    "benchmark": args.benchmark,
    "mode": args.mode,
    "sim_inst": sim_inst,
    "sim_cycle": sim_cycle,
    "CPI": CPI,
    "IPC": IPC,
    "cpu_time_s": cpu_time_s,
    "ns_per_cycle": ns_per_cycle,
    "il1_accesses": il1_A,
    "il1_hits": sim.get("il1.hits", 0),
    "il1_misses": il1_M,
    "il1_amat_cycles": il1_amat_cycles,
    "il1_amat_ns": il1_amat_ns,
    "dl1_accesses": dl1_A,
    "dl1_hits": sim.get("dl1.hits", 0),
    "dl1_misses": dl1_M,
    "dl1_amat_cycles": dl1_amat_cycles,
    "dl1_amat_ns": dl1_amat_ns,
    "l2_accesses": l2_A,
    "l2_hits": sim.get("ul2.hits", 0),
    "l2_misses": l2_M,
    "dram_energy_j": dram_energy_j,
    # These will be updated later (CACTI merge)
    "il1_dyn_j": 0,
    "dl1_dyn_j": 0,
    "l2_dyn_j": 0,
    "il1_leak_j": 0,
    "dl1_leak_j": 0,
    "l2_leak_j": 0,
    "total_energy_j": dram_energy_j
}

# Append to CSV
write_header = False
try:
    with open(args.out, "r") as f:
        pass
except:
    write_header = True

with open(args.out, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=row.keys())
    if write_header:
        writer.writeheader()
    writer.writerow(row)

print(f"Appended row to {args.out}")
