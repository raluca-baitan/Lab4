import os
import statistics

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import load_workbook

EXCEL_FILE = "Lab4_defect_data_solved.xlsx"
BIN_WIDTH = 10
os.makedirs("images", exist_ok=True)
wb = load_workbook(EXCEL_FILE)

# Exercise 2: defect age
ws = wb["Defect age"]
ages = []
for name, submitted, resolved, *_ in ws.iter_rows(min_row=2, values_only=True):
    if name is None or submitted is None or resolved is None:
        continue
    age = (resolved - submitted).days      
    ages.append(age)
    print(f"{name}: {age} days")


counts = {}
for age in ages:
    start = (age // BIN_WIDTH) * BIN_WIDTH
    counts[start] = counts.get(start, 0) + 1

labels = []
values = []
for start in range(0, max(counts) + BIN_WIDTH, BIN_WIDTH):
    labels.append(f"{start}-{start + BIN_WIDTH - 1}")
    values.append(counts.get(start, 0))

print("\nHistogram:")
for label, value in zip(labels, values):
    print(f"  {label:>6} days: {value}")
print(f"Total {len(ages)}, min {min(ages)}, max {max(ages)}, "
      f"median {statistics.median(ages)}, average {statistics.mean(ages):.1f}")

plt.figure(figsize=(7, 4))
bars = plt.bar(labels, values, width=0.95, color="#12343b")
plt.bar_label(bars)
plt.xlabel("Age (days)")
plt.ylabel("Number of defects")
plt.title(f"Histogram of defect age (bin = {BIN_WIDTH} days)")
plt.tight_layout()
plt.savefig("images/histogram_defect_age.png", dpi=150)

# Exercise 3: defect density 
ws = wb["Defect density"]
modules = []
for module, defects, loc, *_ in ws.iter_rows(min_row=2, values_only=True):
    if not isinstance(defects, (int, float)) or not loc:  
        continue
    modules.append((module, defects, defects / loc))   

modules.sort(key=lambda m: m[2], reverse=True)         

print("\nDefect density (sorted):")
for module, defects, density in modules:
    print(f"  {module:>3}: {defects:>2} defects, density {density:.2f}")

most_defects = max(modules, key=lambda m: m[1])
print(f"Most defects: {most_defects[0]} ({most_defects[1]})")
print(f"Highest density: {modules[0][0]} ({modules[0][2]:.2f})")

plt.figure(figsize=(8, 4))
colors = ["#c00000"] + ["#12343b"] * (len(modules) - 1)
bars = plt.bar([m[0] for m in modules], [m[2] for m in modules], color=colors)
plt.bar_label(bars, fmt="%.2f")
plt.xlabel("Module")
plt.ylabel("Defects per line of code")
plt.title("Defect density per module, sorted")
plt.tight_layout()
plt.savefig("images/defect_density.png", dpi=150)
print("\nCharts saved in images/")
