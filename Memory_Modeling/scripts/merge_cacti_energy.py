#!/usr/bin/env python3
import csv
import sys
import re

if len(sys.argv) != 6:
    print("Usage: python3 merge_cacti_energy.py <csv_in> <csv_out> <il1.out> <dl1.out> <l2.out>")
    sys.exit(1)

csv_in, csv_out, il1_file, dl1_file, l2_file = sys.argv[1:]

def extract_dynamic(fname):
    r = re.compile(r"Total dynamic read energy per access.*?([0-9.]+)")
    with open(fname) as f:
        for line in f:
            m = r.search(line)
            if m:
                return float(m.group(1)) * 1e-9   # nJ → J
    return 0.0

# Extract dynamic read energy from CACTI
il1_dyn = extract_dynamic(il1_file)
dl1_dyn = extract_dynamic(dl1_file)
l2_dyn  = extract_dynamic(l2_file)

print("IL1 dynamic read:", il1_dyn, "J")
print("DL1 dynamic read:", dl1_dyn, "J")
print("L2 dynamic read:", l2_dyn, "J")

rows = []

with open(csv_in) as f:
    reader = csv.DictReader(f)
    for row in reader:
        A_il1 = float(row["il1_accesses"])
        A_dl1 = float(row["dl1_accesses"])
        A_l2  = float(row["l2_accesses"])
        runtime = float(row["cpu_time_s"])

        row["il1_dyn_j"] = A_il1 * il1_dyn
        row["dl1_dyn_j"] = A_dl1 * dl1_dyn
        row["l2_dyn_j"]  = A_l2  * l2_dyn

        # No leakage modeling from CACTI in this version
        row["il1_leak_j"] = 0
        row["dl1_leak_j"] = 0
        row["l2_leak_j"]  = 0

        row["total_energy_j"] = (
            float(row["dram_energy_j"])
            + row["il1_dyn_j"]
            + row["dl1_dyn_j"]
            + row["l2_dyn_j"]
        )

        rows.append(row)

with open(csv_out, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated CSV written to {csv_out}")
