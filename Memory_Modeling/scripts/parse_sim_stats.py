#!/usr/bin/env python3
import json
import re
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--in", dest="infile", required=True)
parser.add_argument("--out", dest="outfile", required=True)
args = parser.parse_args()

data = {}

# Regex to match:  "<metric>   <value>  # comment"
pattern = re.compile(r'^([A-Za-z0-9_\.]+)\s+([0-9.+-Ee]+)')

with open(args.infile, "r") as f:
    for line in f:
        m = pattern.match(line.strip())
        if m:
            key = m.group(1).strip()
            val_str = m.group(2)
            try:
                if '.' in val_str:
                    val = float(val_str)
                else:
                    val = int(val_str)
            except:
                continue
            data[key] = val

with open(args.outfile, "w") as f:
    json.dump(data, f, indent=2)

print(f"Wrote {args.outfile} with {len(data)} entries.")
