import pandas as pd, numpy as np, json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B, O, A, G, INK, INK2 = "#2a78d6", "#eb6834", "#1baf7a", "#a3a29c", "#0b0b0b", "#52514e"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#c9c8c2", "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#ecebe7", "axes.axisbelow": True, "figure.dpi": 200, "savefig.bbox": "tight"})
BT = pd.read_pickle("out/backtest.pkl")["rolling4"][0]; FB = pd.read_pickle("out/final_bt.pkl"); V = pd.read_pickle("out/views.pkl"); hold = json.load(open("out/D4_holdout_forecast_LOCKED.json"))
q = [s[:2] + "\n" + s[3:] for s in BT.quarter]
fig, ax = plt.subplots(figsize=(7.2, 2.8)); x = np.arange(8)
ax.fill_between(x, FB.p10, FB.p90, color=B, alpha=0.12, lw=0, label="Final p10–p90")
ax.plot(x, BT.actual, color=INK, lw=2.2, marker="o", ms=4, label="Actual (clean)")
ax.plot(x, BT.commit, color=O, lw=1.8, marker="o", ms=3.5, label="Rep commit")
ax.plot(x, BT.stage_weighted, color=G, lw=1.6, ls=(0, (3, 2)), label="Stage-weighted, uncalibrated")
ax.plot(x, FB.final_p50, color=B, lw=2, marker="o", ms=3.5, label="Final (calibrated) p50")
ax.set_xticks(x); ax.set_xticklabels(q, fontsize=7.5); ax.set_ylabel("Bookings, ₹ crore"); ax.set_ylim(0, 20)
ax.legend(frameon=False, fontsize=7.5, ncol=3, loc="upper left")
ax.set_title("Back-test: final method misses by 15.6% on average vs 26.6% for rep commits", loc="left", fontsize=10, fontweight="bold", color=INK)
fig.savefig("fig/backtest.png"); plt.close()
cov = V["cov"]; fig, ax = plt.subplots(figsize=(7.2, 2.5)); x = np.arange(len(cov))
ax.plot(x, cov.coverage_reported, color=B, lw=2, marker="o", ms=4); ax.plot(x, cov.coverage_required, color=O, lw=2, marker="o", ms=4)
ax.text(len(cov) - 0.8, cov.coverage_reported.iloc[-1], "Reported", color=INK2, fontsize=8, va="center"); ax.text(len(cov) - 0.8, cov.coverage_required.iloc[-1], "Required", color=INK2, fontsize=8, va="center")
ax.set_xticks(x); ax.set_xticklabels([s[:2] + "\n" + s[3:] for s in cov.quarter], fontsize=7); ax.set_ylim(0, 6.5); ax.set_xlim(-0.3, len(cov) + 0.6); ax.set_ylabel("× quarterly quota")
ax.set_title("Reported coverage rose to 3.5x; conversion fell faster, so 5.6x is now needed", loc="left", fontsize=10, fontweight="bold", color=INK)
fig.savefig("fig/coverage.png"); plt.close(); print("ok")
