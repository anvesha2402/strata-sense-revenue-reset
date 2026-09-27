"""D1 step 3c: account fit score (H1), win-rate model and mix-vs-rate decomposition (H0), effort allocation."""
import pandas as pd, numpy as np, statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score
D = "../../data/"
o = pd.read_pickle("out/opps_analysis.pkl")
q = o[o.qualified & o.stage.isin(["Closed Won", "Closed Lost"])].copy()
q["won"] = q.is_won.astype(int)
q["log_assets"] = np.log(q.acc_installed_rotating_assets_est.clip(lower=50))
q["seg"] = q.segment.replace({"Discrete manufacturing": "Discrete", "Process industries": "Process", "Energy & utilities": "Energy"})
# ---- fit score: firmographics only, trained FY24-25, tested FY26 (out of time)
ff = "won ~ C(seg, Treatment('Discrete')) + band_idx + log_assets + helix_inc + C(region)"
tr = q[q.fy <= 2025]; te = q[q.fy == 2026]
fm = smf.logit(ff, tr).fit(disp=0)
print(fm.summary2().tables[1].round(3))
q["fit_score"] = fm.predict(q)
print("AUC train", round(roc_auc_score(tr.won, fm.predict(tr)), 3), "AUC FY26 out-of-time", round(roc_auc_score(te.won, fm.predict(te)), 3))
cuts = q[q.fy <= 2025].fit_score.quantile([1/3, 2/3]).values
q["fit_tier"] = pd.cut(q.fit_score, [-1, cuts[0], cuts[1], 2], labels=["Low fit", "Mid fit", "High fit"])
ft = q.groupby(["fit_tier", "fy"], observed=True).won.agg(["mean", "size"]).unstack()
print(ft.round(3))
print("low-fit share of qualified deals", q.groupby("fy").fit_tier.apply(lambda s: (s == "Low fit").mean()).round(3).to_dict())
# ---- effort on 3,100 targets
t = pd.read_csv(D + "dr2_target_accounts.csv")
t["seg"] = t.segment.replace({"Discrete manufacturing": "Discrete", "Process industries": "Process", "Energy & utilities": "Energy"})
t["band_idx"] = t.revenue_band.map({"< 500 cr": 0, "500-1,000 cr": 1, "1,000-5,000 cr": 2, "5,000-20,000 cr": 3, "> 20,000 cr": 4})
t["log_assets"] = np.log(t.installed_rotating_assets_est.clip(lower=50)); t["helix_inc"] = t.incumbent_automation_vendor.eq("Helix Automation")
t["fit_score"] = fm.predict(t)
t["fit_tier"] = pd.cut(t.fit_score, [-1, cuts[0], cuts[1], 2], labels=["Low fit", "Mid fit", "High fit"])
eff = t.groupby("fit_tier", observed=True).agg(accounts=("account_id", "size"), touches=("ae_touches_fy26", "sum"),
      touches_per_acc=("ae_touches_fy26", "mean"), multi_contact=("distinct_contacts_engaged_fy26", lambda s: (s > 1).mean()))
eff["touch_share"] = eff.touches / eff.touches.sum(); eff["acc_share"] = eff.accounts / eff.accounts.sum()
print(eff.round(3))
act_ae = t.groupby("assigned_ae_id").size()
ros = pd.read_csv(D + "dr3_ae_roster.csv")
print("accounts per AE: median", act_ae.median(), "range", act_ae.min(), act_ae.max(), "on exited AEs", t.assigned_ae_id.isin(ros[ros.status_31mar2026 == "Exited"].ae_id).sum())
print("accounts per AE by region", t.merge(ros, left_on="assigned_ae_id", right_on="ae_id").groupby("region_y").assigned_ae_id.agg(["size", "nunique"]).assign(per=lambda d: d["size"] / d["nunique"]).round(0))
# ---- explanatory model: all years
q["tenure"] = q.tenure_band.astype(str)
mf = ("won ~ fit_score_logit + C(threading) + C(tenure, Treatment('>24 months')) + C(buyer_committee_includes_fin_proc_it) "
      "+ C(proof_of_value) + C(lead_source_f, Treatment('SDR / Marketing')) + C(fy)")
q["fit_score_logit"] = np.log(q.fit_score / (1 - q.fit_score))
m = smf.logit(mf, q).fit(disp=0)
tab = pd.DataFrame({"coef": m.params, "OR": np.exp(m.params), "p": m.pvalues}).round(3); print(tab)
# ---- mix vs rate decomposition FY24 -> FY26
def pred(df, year):
    d = df.copy(); d["fy"] = year; return m.predict(d).mean()
a24 = q[q.fy == 2024].won.mean(); a26 = q[q.fy == 2026].won.mean()
p24 = pred(q[q.fy == 2024], 2024); p26_24 = pred(q[q.fy == 2026], 2024); p26 = pred(q[q.fy == 2026], 2026)
print(f"actual {a24:.3f} -> {a26:.3f}; model FY24 {p24:.3f}; FY26 mix @FY24 rates {p26_24:.3f}; FY26 {p26:.3f}")
print(f"mix effect {p26_24 - p24:+.3f}; within-cell (year) effect {p26 - p26_24:+.3f}")
# factor-by-factor mix: swap one factor's FY26 values into FY24 rows by resampling
rng = np.random.default_rng(0); base = q[q.fy == 2024].copy(); f26 = q[q.fy == 2026]
contrib = {}
for col in ["fit_score_logit", "threading", "tenure", "buyer_committee_includes_fin_proc_it", "proof_of_value", "lead_source_f"]:
    vals = []
    for _ in range(200):
        d = base.copy(); d[col] = rng.choice(f26[col].values, len(d)); d["fy"] = 2024; vals.append(m.predict(d).mean())
    contrib[col] = np.mean(vals) - p24
print("mix contribution by factor (pp):", {k: round(v * 100, 2) for k, v in contrib.items()})
# ---- ideal-cell trend (H0 test)
ideal = q[(q.fit_tier == "High fit") & (q.threading != "1 contact") & (q.tenure.isin([">24 months", "9-24 months"]))]
print("ideal cell win by FY", ideal.groupby("fy").won.agg(["mean", "size"]).round(3).to_dict())
pd.to_pickle(dict(fm=fm.params, auc=(roc_auc_score(tr.won, fm.predict(tr)), roc_auc_score(te.won, fm.predict(te))), ft=ft, eff=eff,
                  tab=tab, decomp=dict(a24=a24, a26=a26, p24=p24, p26_24=p26_24, p26=p26), contrib=contrib,
                  ideal=ideal.groupby("fy").won.agg(["mean", "size"]), cuts=cuts), "out/model.pkl")
q.to_pickle("out/q_scored.pkl"); t.to_pickle("out/targets_scored.pkl")
