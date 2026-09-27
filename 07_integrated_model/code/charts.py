import json, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from openpyxl import load_workbook
B, O, A, G, INK, INK2 = "#2a78d6", "#eb6834", "#1baf7a", "#a3a29c", "#0b0b0b", "#52514e"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#c9c8c2", "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#ecebe7", "axes.axisbelow": True, "figure.dpi": 200, "savefig.bbox": "tight"})
M = json.load(open("out/rowmap.json")); runs = json.load(open("out/runs.json"))
wb = load_workbook("out/D7_Integrated_Model.xlsx", data_only=True)
QC = "CDEFGHIJKLMN"; ab, ann, pl = M["ab"], M["ann"], M["pl"]
v = lambda ws, ref: wb[ws][ref].value
import os; os.makedirs("fig", exist_ok=True)
# 1 ARR path
yrs = ["FY26", "FY27", "FY28", "FY29"]; x = np.arange(4)
fig, ax = plt.subplots(figsize=(7.0, 3.0))
board = [310] + [v("ARR_bridge", f"{c}{ann['board']}") for c in "OPQ"]; dn = [310] + [v("Do_nothing", f"{c}8") for c in "CDE"]
for s, col, lw, ls in [("Aggressive", A, 1.4, (0, (3, 2))), ("Downside", O, 1.4, (0, (3, 2))), ("CFO-capped", G, 1.4, (0, (1, 1.5)))]:
    ys = [310] + [runs["res"][s][f"ARR {y}"] for y in yrs[1:]]; ax.plot(x, ys, color=col, lw=lw, ls=ls, label=s); ax.annotate(f"{ys[-1]:.0f}", (3, ys[-1]), xytext=(5, 0), textcoords="offset points", va="center", color=col, fontsize=8)
ax.plot(x, board, color=INK, lw=1.2, ls=(0, (6, 2)), label="Board path (15/20/22%)"); ax.annotate(f"{board[-1]:.0f}", (3, board[-1]), xytext=(5, 6), textcoords="offset points", va="center", color=INK, fontsize=8)
ax.plot(x, dn, color=INK2, lw=1.2, label="Do nothing"); ax.annotate(f"{dn[-1]:.0f}", (3, dn[-1]), xytext=(5, 0), textcoords="offset points", va="center", color=INK2, fontsize=8)
base = [310] + [runs["res"]["Base"][f"ARR {y}"] for y in yrs[1:]]
ax.plot(x, base, color=B, lw=2.4, marker="o", ms=4, label="Base plan"); ax.annotate(f"{base[-1]:.0f}", (3, base[-1]), xytext=(5, -8), textcoords="offset points", va="center", color=B, fontsize=8, fontweight="bold")
ax.set_xticks(x, yrs); ax.set_ylabel("Closing ARR (₹ cr)"); ax.set_xlim(-0.1, 3.35); ax.legend(frameon=False, fontsize=7.5, ncol=3, loc="upper left")
plt.savefig("fig/arr_path.png"); plt.close()
# 2 bridge FY26 -> FY29
comp = [("FY26\nARR", 310, "t"), ("Direct\nnew logo", sum(v("ARR_bridge", f"{c}{ab['dir']}") for c in "OPQ"), "+"), ("Partner\nnew logo", sum(v("ARR_bridge", f"{c}{ab['par']}") for c in "OPQ"), "+"),
        ("Expansion", sum(v("ARR_bridge", f"{c}{ab['expn']}") for c in "OPQ"), "+"), ("Contraction", -sum(v("ARR_bridge", f"{c}{ab['cont']}") for c in "OPQ"), "-"),
        ("Churn", -sum(v("ARR_bridge", f"{c}{ab['chrn']}") for c in "OPQ"), "-"), ("Vajra\n(expected)", -v("ARR_bridge", f"O{ab['vaj']}"), "-")]
fig, ax = plt.subplots(figsize=(7.0, 2.8)); run_ = 0
for i, (lab, val, t) in enumerate(comp):
    if t == "t": ax.bar(i, val, color=G, width=0.6); run_ = val; ax.text(i, val + 6, f"{val:.0f}", ha="center", fontsize=8)
    else:
        bottom = run_ if val > 0 else run_ + val; ax.bar(i, abs(val), bottom=bottom, color=B if val > 0 else O, width=0.6)
        ax.text(i, run_ + max(val, 0) + 6, f"{val:+.0f}", ha="center", fontsize=8, color=INK); run_ += val
ax.bar(len(comp), run_, color=INK2, width=0.6); ax.text(len(comp), run_ + 6, f"{run_:.0f}", ha="center", fontsize=8, fontweight="bold")
ax.set_xticks(range(len(comp) + 1), [c[0] for c in comp] + ["FY29\nARR"], fontsize=7.5); ax.set_ylabel("₹ cr"); ax.set_ylim(0, (310 + sum(c[1] for c in comp if c[2] == "+")) * 1.1)
plt.savefig("fig/bridge.png"); plt.close()
# 3 tornado
drv = [("Win rate ±3 pts", "Win rate"), ("Churn ±2 pts", "Churn"), ("Partner productivity ±30%", "Partner productivity"), ("Discount ±3 pts", "Discount"), ("Sales cycle ±1 month", "Sales cycle")]
b0 = runs["res"]["Base"]["ARR FY29"]
fig, ax = plt.subplots(figsize=(7.0, 2.4))
for i, (lab, k) in enumerate(drv[::-1]):
    lo = runs["sens"][f"{k}|-1"]["ARR FY29"] - b0; hi = runs["sens"][f"{k}|1"]["ARR FY29"] - b0
    fav, unf = max(lo, hi), min(lo, hi)
    ax.barh(i, fav, color=B, height=0.55); ax.barh(i, unf, color=O, height=0.55)
    ax.text(fav + 0.8, i, f"{fav:+.1f}", va="center", fontsize=8); ax.text(unf - 0.8, i, f"{unf:+.1f}", va="center", ha="right", fontsize=8)
ax.axvline(0, color=INK2, lw=0.8); ax.set_yticks(range(len(drv)), [d[0] for d in drv[::-1]]); ax.set_xlabel(f"Change in FY29 closing ARR vs Base ₹{b0:.0f} cr (₹ cr)"); ax.grid(axis="y", visible=False)
ax.set_xlim(-32, 32); plt.savefig("fig/tornado.png"); plt.close()
# 4 CAC payback quarterly
q = ["Q1\nFY27", "Q2", "Q3", "Q4", "Q1\nFY28", "Q2", "Q3", "Q4", "Q1\nFY29", "Q2", "Q3", "Q4"]
cac = [v("PnL", f"{c}{pl['cac']}") for c in QC]
fig, ax = plt.subplots(figsize=(7.0, 2.4)); xx = np.arange(12)
ax.bar(xx, cac, color=[O if c > 30 else B for c in cac], width=0.6)
for i, c in enumerate(cac): ax.text(i, c / 2, f"{c:.1f}", ha="center", fontsize=7.5, color="white", fontweight="bold")
ax.plot([-0.4, 11.4], [30, 30], color=INK, lw=1, ls=(0, (4, 2))); ax.text(11.45, 30, "30-month cap", va="center", fontsize=7.5)
ax.plot([6.6, 7.4], [24, 24], color=INK, lw=1.5); ax.text(7.0, 25.3, "24-month cap, Q4 FY28", ha="center", fontsize=7)
ax.set_xticks(xx, q, fontsize=7.5); ax.set_ylabel("Months"); ax.set_ylim(0, 36)
plt.savefig("fig/cac.png"); plt.close()
print("charts ok")
