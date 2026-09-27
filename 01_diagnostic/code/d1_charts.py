"""D1 exhibits (static PNG for the memo). Palette: validated reference slots 1-3 + neutral gray."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
B, O, A, G, INK, INK2 = "#2a78d6", "#eb6834", "#1baf7a", "#a3a29c", "#0b0b0b", "#52514e"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#c9c8c2", "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": "#ecebe7", "grid.linewidth": 0.8, "axes.axisbelow": True, "figure.dpi": 200, "savefig.bbox": "tight"})
A_ = pd.read_pickle("out/arr.pkl"); F = pd.read_pickle("out/funnel.pkl"); M = pd.read_pickle("out/model.pkl"); H = pd.read_pickle("out/h3.pkl"); S = pd.read_pickle("out/sizing.pkl")
q = pd.read_pickle("out/q_scored.pkl")
def title(ax, t, sub=None):
    ax.set_title(t, loc="left", fontsize=10.5, fontweight="bold", color=INK, pad=16 if sub else 8)
    if sub: ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=8.5, color=INK2)

# ---- Ex1 ARR bridge + retention trend
br = A_["br"]
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={"width_ratios": [1.7, 1]})
steps = [("Opening\n1 Apr 25", br.loc["FY26", "opening"], "tot"), ("New logo", br.loc["FY26", "New logo"], "up"), ("Expansion", br.loc["FY26", "Expansion"], "up"),
         ("Contraction", br.loc["FY26", "Contraction"], "dn"), ("Churn", br.loc["FY26", "Churn"], "dn"), ("Closing\n31 Mar 26", br.loc["FY26", "closing_calc"], "tot")]
run = 0
for i, (lab, v, k) in enumerate(steps):
    if k == "tot": bottom, h, col = 0, v, B; run = v
    elif k == "up": bottom, h, col = run, v, A; run += v
    else: bottom, h, col = run + v, -v, O; run += v
    ax.bar(i, h, bottom=bottom, color=col, width=0.62)
    ax.text(i, bottom + h + 5, f"{v:+.0f}" if k != "tot" else f"{v:.0f}", ha="center", fontsize=8.5, color=INK)
ax.set_xticks(range(6)); ax.set_xticklabels([s[0] for s in steps], fontsize=7.0); ax.set_ylim(0, 360); ax.set_ylabel("₹ crore ARR")
title(ax, "FY26 ARR bridge", "Rebuilt from the DR2 ledger; reconciles to DR3 to ₹0.01 cr")
yrs = ["FY24", "FY25", "FY26"]
ax2.plot(yrs, br.NRR * 100, color=B, lw=2, marker="o", ms=5); ax2.plot(yrs, br.GRR * 100, color=O, lw=2, marker="o", ms=5)
for x, v in zip(yrs, br.NRR * 100): ax2.text(x, v + 1.8, f"{v:.0f}%", ha="center", fontsize=8, color=INK)
for x, v in zip(yrs, br.GRR * 100): ax2.text(x, v - 4.5, f"{v:.0f}%", ha="center", fontsize=8, color=INK)
ax2.text(2.1, br.NRR.iloc[-1] * 100, "NRR", color=INK2, fontsize=8, va="center"); ax2.text(2.1, br.GRR.iloc[-1] * 100 - 1, "GRR", color=INK2, fontsize=8, va="center")
ax2.set_ylim(80, 125); ax2.set_xlim(-0.3, 2.5); title(ax2, "Retention, %")
fig.tight_layout(); fig.savefig("fig/ex1_arr_bridge.png"); plt.close()

# ---- Ex2 NRR by driver
R = A_["ret"]
rows = [("Helix incumbent", R["helix_incumbent"], "Helix incumbent"), ("Other incumbent", R["helix_incumbent"], "Other incumbent"),
        ("Usage < 50%", R["usage_band"], "<50%"), ("Usage 50-70%", R["usage_band"], "50-70%"), ("Usage > 70%", R["usage_band"], ">70%"),
        ("Accounts > ₹2 cr", R["size_band"], ">2 cr"), ("Accounts < ₹0.25 cr", R["size_band"], "<0.25 cr")]
fig, ax = plt.subplots(figsize=(7.2, 2.9))
y = np.arange(len(rows))[::-1]
for yy, (lab, t, key) in zip(y, rows):
    a, b = t[("FY25", "NRR")][key] * 100, t[("FY26", "NRR")][key] * 100; op = t[("FY26", "opening")][key]
    ax.plot([a, b], [yy, yy], color=G, lw=1.5, zorder=1)
    ax.scatter(a, yy, s=42, color=B, zorder=2, edgecolor="white", lw=1.5); ax.scatter(b, yy, s=42, color=O, zorder=3, edgecolor="white", lw=1.5)
    ax.text(max(a, b) + 1.5, yy, f"{b:.0f}%  (₹{op:.0f} cr base)", va="center", fontsize=8, color=INK)
ax.axvline(100, color=INK2, lw=0.8, ls=(0, (3, 3)))
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows]); ax.set_xlim(65, 150); ax.set_xlabel("Net revenue retention, %")
ax.scatter([], [], color=B, label="FY25"); ax.scatter([], [], color=O, label="FY26"); ax.legend(frameon=False, loc="upper left", fontsize=8)
title(ax, "Where NRR fell: Helix-incumbent customers dropped 24 points", "NRR by customer group, FY25 → FY26; base = opening ARR FY26")
fig.tight_layout(); fig.savefig("fig/ex2_nrr_drivers.png"); plt.close()

# ---- Ex4 win rate small multiples
fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=True)
panels = [("Account fit tier", M["ft"]["mean"], ["High fit", "Mid fit", "Low fit"]),
          ("Buyer contacts engaged", F["threading"].filter(like="mean"), ["3+ contacts", "2 contacts", "1 contact"]),
          ("AE tenure at deal creation", F["tenure_band"].filter(like="mean"), [">24 months", "9-24 months", "<9 months"])]
for ax, (t, df, order) in zip(axs, panels):
    df = df.copy(); df.columns = ["FY24", "FY25", "FY26"]
    for key, col in zip(order, [B, A, O]):
        v = df.loc[key] * 100; ax.plot(df.columns, v, color=col, lw=2, marker="o", ms=4.5)
        ax.text(2.12, v.iloc[-1], key.replace(" contacts", "").replace(" contact", "").replace(" months", "m"), fontsize=7.5, color=INK2, va="center")
    ax.set_xlim(-0.2, 2.9); ax.set_title(t, fontsize=9, loc="left", color=INK)
axs[0].set_ylabel("Win rate on qualified deals, %"); axs[0].set_ylim(0, 42)
fig.suptitle("Win rate by account fit, threading and rep tenure", x=0.01, ha="left", fontsize=10.5, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig("fig/ex4_winrate_cuts.png"); plt.close()

# ---- Ex5 decomposition
d = M["decomp"]; c = M["contrib"]
items = [("FY24 win rate", d["a24"] * 100, "tot"), ("Lower-fit\naccounts", c["fit_score_logit"] * 100, "d"), ("Bigger buying\ncommittees", c["buyer_committee_includes_fin_proc_it"] * 100, "d"),
         ("Single-\nthreading", c["threading"] * 100, "d")]
other = (d["p26_24"] - d["p24"]) * 100 - sum(v for _, v, _ in items[1:])
items += [("Tenure &\nsource mix", other, "d"), ("Within-segment\ndecline", (d["p26"] - d["p26_24"]) * 100, "d"), ("FY26 win rate", d["a26"] * 100, "tot")]
fig, ax = plt.subplots(figsize=(7.2, 2.9)); run = 0
for i, (lab, v, k) in enumerate(items):
    if k == "tot": ax.bar(i, v, color=B, width=0.6); run = v; ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=8.5)
    else:
        col = O if v < 0 else A; ax.bar(i, v, bottom=run, color=col, width=0.6)
        ax.text(i, max(run, run + v) + 0.5, f"{v:+.1f}", ha="center", fontsize=8.5); run += v
ax.set_xticks(range(len(items))); ax.set_xticklabels([x[0] for x in items], fontsize=7.6); ax.set_ylim(0, 28); ax.set_ylabel("Win rate, %")
ax.axvspan(0.5, 4.5, color="#f4f3ef", zorder=0); ax.text(2.5, 26.5, "Mix: who we sell to and how (−3.4 pts)", ha="center", fontsize=8, color=INK2)
ax.text(5, 26.5, "Rate (−3.6 pts)", ha="center", fontsize=8, color=INK2)
title(ax, "Half the win-rate fall is mix, half is a within-segment decline", "Logistic model on 1,218 qualified closed deals, FY24 → FY26, percentage points")
fig.tight_layout(); fig.savefig("fig/ex5_winrate_decomp.png"); plt.close()

# ---- Ex6 forecast
fh = H["fh"]
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.7))
x = np.arange(len(fh)); ax.bar(x, fh.err_m1 * 100, color=[O if v > 0 else B for v in fh.err_m1], width=0.62)
ax.axhline(0, color=INK2, lw=0.8)
for fy, xs in [("FY24", 1.5), ("FY25", 5.5), ("FY26", 9.5)]:
    mape = fh[fh.fy == fy].err_m1.abs().mean() * 100; ax.text(xs, 38, f"{fy}\nmiss {mape:.0f}%", ha="center", fontsize=8, color=INK)
ax.set_xticks(x); ax.set_xticklabels([q_[:2] for q_ in fh.quarter], fontsize=7.5); ax.set_ylim(-15, 48); ax.set_ylabel("Month-1 commit vs actual, %")
title(ax, "Commit calls over-forecast", "Positive = commit above actual bookings")
yr = fh.groupby("fy")[["coverage", "pipe_conv"]].mean()
ax2.plot(yr.index, yr.coverage, color=B, lw=2, marker="o", ms=5)
for xx, v in zip(yr.index, yr.coverage): ax2.text(xx, v + 0.18, f"{v:.1f}x", ha="center", fontsize=8)
ax2.plot(yr.index, 1 / yr.pipe_conv / (1 / yr.attain if False else 1), color=O, lw=2, marker="o", ms=5)
for xx, v in zip(yr.index, 1 / yr.pipe_conv): ax2.text(xx, v + 0.18, f"{v:.1f}x", ha="center", fontsize=8)
ax2.text(2.22, yr.coverage.iloc[-1], "Reported", fontsize=7.5, color=INK2, va="center"); ax2.text(2.22, 1 / yr.pipe_conv.iloc[-1], "Needed for\n100% quota", fontsize=7.5, color=INK2, va="center")
ax2.set_ylim(0, 6.5); ax2.set_xlim(-0.2, 3.0); ax2.set_ylabel("Pipeline ÷ quarterly quota")
title(ax2, "Coverage rose; conversion fell faster")
fig.tight_layout(); fig.savefig("fig/ex6_forecast.png"); plt.close()

# ---- Ex8 root causes
rc = [("Helix bundle: base erosion\n+ lost Helix-incumbent deals", S["helix_retention"] + S["helix_newlogo"], "Not fixable by sales alone"),
      ("Installed-base expansion stall\n(non-Helix customers)", S["nonhelix_retention"], "Needs CS + sales"),
      ("Targeting drift and\nsingle-threading", S["mix_fit"] + S["mix_threading"], "Fixable by sales action"),
      ("Discount creep\n(13% → 19%)", S["discount_leak"], "Fixable by sales action")]
fig, ax = plt.subplots(figsize=(7.2, 2.6)); y = np.arange(len(rc))[::-1]
cols = {"Not fixable by sales alone": O, "Needs CS + sales": G, "Fixable by sales action": B}
for yy, (lab, v, k) in zip(y, rc):
    ax.barh(yy, v, color=cols[k], height=0.55); ax.text(v + 0.5, yy, f"₹{v:.1f} cr  ·  {k}", va="center", fontsize=8.2, color=INK)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rc], fontsize=8); ax.set_xlim(0, 58); ax.set_xlabel("ARR at stake, ₹ crore per year (FY26 run-rate)")
title(ax, "Root causes ranked by ARR at stake")
fig.tight_layout(); fig.savefig("fig/ex8_root_causes.png"); plt.close()
print("ok")
