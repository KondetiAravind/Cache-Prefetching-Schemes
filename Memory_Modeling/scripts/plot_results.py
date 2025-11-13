import pandas as pd
import matplotlib.pyplot as plt
import os

# Load final CSV
csv_path = "results/summary_with_energy_final.csv"

if not os.path.exists(csv_path):
    print(f"ERROR: {csv_path} not found.")
    exit(1)

df = pd.read_csv(csv_path)

# Ensure output directory exists
os.makedirs("results", exist_ok=True)

print("\nLoaded CSV with columns:")
print(df.columns.tolist())


# =======================================================================
# PLOT 1 — IPC Comparison
# =======================================================================
print("Generating IPC plot...")

plt.figure(figsize=(10,6))
for benchmark in df["benchmark"].unique():
    subset = df[df["benchmark"] == benchmark]
    plt.plot(subset["mode"], subset["IPC"], marker='o', label=benchmark)

plt.title("IPC Comparison Across Prefetch Modes")
plt.xlabel("Prefetch Mode")
plt.ylabel("IPC")
plt.grid(True)
plt.legend()
plt.savefig("results/plot_ipc.png")
plt.close()


# =======================================================================
# PLOT 2 — CPI Comparison
# =======================================================================
print("Generating CPI plot...")

plt.figure(figsize=(10,6))
for benchmark in df["benchmark"].unique():
    subset = df[df["benchmark"] == benchmark]
    plt.plot(subset["mode"], subset["CPI"], marker='o', label=benchmark)

plt.title("CPI Comparison Across Prefetch Modes")
plt.xlabel("Prefetch Mode")
plt.ylabel("CPI")
plt.grid(True)
plt.legend()
plt.savefig("results/plot_cpi.png")
plt.close()


# =======================================================================
# PLOT 3 — AMAT (IL1 + DL1 ONLY)
# =======================================================================
print("Generating AMAT plot...")

plt.figure(figsize=(10,6))

plt.plot(df["mode"], df["il1_amat_cycles"], marker='o', label="IL1 AMAT (cycles)")
plt.plot(df["mode"], df["dl1_amat_cycles"], marker='o', label="DL1 AMAT (cycles)")

plt.title("Average Memory Access Time (Cycles)")
plt.xlabel("Prefetch Mode")
plt.ylabel("AMAT (cycles)")
plt.grid(True)
plt.legend()
plt.savefig("results/plot_amat.png")
plt.close()


# =======================================================================
# PLOT 4 — TOTAL ENERGY
# =======================================================================
print("Generating energy plot...")

plt.figure(figsize=(10,6))
for benchmark in df["benchmark"].unique():
    subset = df[df["benchmark"] == benchmark]
    plt.plot(subset["mode"], subset["total_energy_j"], marker='o', label=benchmark)

plt.title("Total Energy Consumption (Joules)")
plt.xlabel("Prefetch Mode")
plt.ylabel("Energy (J)")
plt.grid(True)
plt.legend()
plt.savefig("results/plot_energy.png")
plt.close()


# =======================================================================
# PLOT 5 — L1 MISS REDUCTION
# =======================================================================
print("Generating L1 miss reduction plot...")

plt.figure(figsize=(10,6))
for benchmark in df["benchmark"].unique():
    subset = df[df["benchmark"] == benchmark]
    plt.plot(subset["mode"], subset["il1_misses"], marker='o', label=f"{benchmark} IL1 Misses")
    plt.plot(subset["mode"], subset["dl1_misses"], marker='x', label=f"{benchmark} DL1 Misses")

plt.title("Prefetch Impact on L1 Misses")
plt.xlabel("Prefetch Mode")
plt.ylabel("Miss Count")
plt.grid(True)
plt.legend()
plt.savefig("results/plot_prefetch_effect.png")
plt.close()


print("\nAll plots generated successfully!")
print("  results/plot_ipc.png")
print("  results/plot_cpi.png")
print("  results/plot_amat.png")
print("  results/plot_energy.png")
print("  results/plot_prefetch_effect.png")
