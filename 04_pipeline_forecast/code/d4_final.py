"""D4 step 3: final method (stage-weighted, rolling 4 quarters, walk-forward bias calibration) — back-test table and LOCKED hold-out forecast."""
import pandas as pd, numpy as np, json, hashlib, datetime, warnings; warnings.filterwarnings("ignore")
from d4_methods import sn, act, QS, fh, m1, m2, m3, bucket
W = 4
rows = []
for i in range(1, 13):
    s = QS[i]; tr = sn[sn.snapshot_date.isin(QS[max(0, i - W):i])]; te = sn[sn.snapshot_date == s]
    e3, pct, _ = m3(tr, te, sims=4000, seed=i)
    rows.append(dict(i=i, snapshot=s, actual=act.set_index("snapshot_date").actual_cr[s], sw=m1(tr, te), ca=m2(tr, te), sim=e3, sim_p10=pct[0], sim_p90=pct[2]))
df = pd.DataFrame(rows)
fac = []
for k, r in df.iterrows():
    past = df[(df.i < r.i) & (df.i >= r.i - 4) & df.actual.notna()]
    fac.append((past.actual / past.sw).median() if len(past) else 1.0)
df["cal_factor"] = fac; df["final_p50"] = df.sw * df.cal_factor
bt = df[(df.i >= 4) & (df.i <= 11)].copy()
bt["err"] = (bt.final_p50 - bt.actual) / bt.actual
# interval: p50 × (1 + empirical error quantiles from calibrated back-test, available up to that quarter) blended with simulation spread
q10, q90 = np.quantile(bt.err, [0.1, 0.9])
sim_rel_lo = (df.sim_p10 / df.sim).median() - 1; sim_rel_hi = (df.sim_p90 / df.sim).median() - 1
lo = min(-q90, sim_rel_lo); hi = max(-q10, sim_rel_hi)          # forecast error = f/a-1 → actual ≈ f/(1+err)
bt["p10"] = bt.final_p50 * (1 + lo); bt["p90"] = bt.final_p50 * (1 + hi)
cov = ((bt.actual >= bt.p10) & (bt.actual <= bt.p90)).mean()
print(bt[["snapshot", "actual", "sw", "cal_factor", "final_p50", "p10", "p90", "err"]].round(3).to_string())
print("MAPE", round(bt.err.abs().mean(), 4), "bias", round(bt.err.mean(), 4), "coverage p10-p90", cov, "band", round(lo, 3), round(hi, 3))
h = df[df.i == 12].iloc[0]
hold = dict(quarter="Q1 FY27", snapshot="2026-04-01", method="Stage-weighted conversion (stage x close-date bucket), rolling 4 quarters, walk-forward bias calibration",
            raw_stage_weighted_cr=round(h.sw, 3), calibration_factor=round(h.cal_factor, 4), p10_cr=round(h.sw * h.cal_factor * (1 + lo), 2),
            p50_cr=round(h.sw * h.cal_factor, 2), p90_cr=round(h.sw * h.cal_factor * (1 + hi), 2),
            cross_checks=dict(cohort_age_cr=round(h.ca, 2), simulation_expected_cr=round(h.sim, 2), simulation_p10_p90=[round(h.sim_p10, 2), round(h.sim_p90, 2)],
                              rep_commit_m1_cr=float(pd.read_excel("out/DR1b_holdout_snapshot_1Apr2026.xlsx", sheet_name="q1fy27_quota_commit").commit_call_m1_cr[0])),
            locked_at=datetime.datetime.utcnow().isoformat() + "Z", actuals_viewed=False)
blob = json.dumps(hold, sort_keys=True); hold["sha256"] = hashlib.sha256(blob.encode()).hexdigest()
json.dump(hold, open("out/D4_holdout_forecast_LOCKED.json", "w"), indent=2)
print(json.dumps(hold, indent=2))
df.to_pickle("out/final_df.pkl"); bt.to_pickle("out/final_bt.pkl"); pd.to_pickle(dict(lo=lo, hi=hi, cov=cov), "out/band.pkl")
