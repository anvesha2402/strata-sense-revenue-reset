"""D1 step 3d: targeted hypothesis tests H2-H5 and forecast accuracy (H3)."""
import pandas as pd, numpy as np, statsmodels.formula.api as smf
D = "../../data/"
q = pd.read_pickle("out/q_scored.pkl"); o = pd.read_pickle("out/opps_analysis.pkl")
p = q[q.reached >= 4].copy(); p = p[p.business_case_attached.notna() & p.discount_pct.notna()]
p["bc"] = (p.business_case_attached == "Y").astype(int)
m2 = smf.logit("won ~ bc + discount_pct + fit_score_logit + C(threading) + C(tenure, Treatment('>24 months')) + C(fy)", p).fit(disp=0)
print("== H2 proposals model"); print(pd.DataFrame({"OR": np.exp(m2.params), "p": m2.pvalues}).round(3).loc[["bc", "discount_pct"]])
print("BC rate on FY proposals", p.groupby("fy").bc.mean().round(3).to_dict(), "n", p.groupby("fy").size().to_dict())
print("BC win rates by fy", p.groupby(["fy", "bc"]).won.mean().unstack().round(3).to_dict())
print("BC by tenure", p.groupby(["tenure", "bc"]).won.mean().unstack().round(3))
bc_cyc = q[q.is_won & q.business_case_attached.notna()].assign(cyc=lambda d: (d.close_date - d.created_date).dt.days / 30.44).groupby("business_case_attached").cyc.mean()
print("won cycle by BC", bc_cyc.round(2).to_dict())
# discount: does discount associate with win within comp groups? logit already; also correlation of discount with BC
print("mean discount by BC (proposals)", p.groupby("bc").discount_pct.mean().round(1).to_dict())
# ---- H4: Helix incumbent structural test
pp = q[q.reached >= 4].copy(); pp["strong"] = (pp.business_case_attached == "Y") & (pp.threading != "1 contact")
print("\n== H4: proposal win rate by Helix-incumbent x strong selling (BC + multi-threaded)")
print(pp.pivot_table(index="helix_inc", columns="strong", values="won", aggfunc=["mean", "size"]).round(3))
hx = pp[pp.comp_group == "Helix Automation"]; ts = pp[pp.comp_group == "TrueSense AI"]
print("Helix-recorded proposals: win by strong", hx.groupby("strong").won.agg(["mean", "size"]).round(3).to_dict())
print("  of which Helix-incumbent", hx[hx.helix_inc].groupby("strong").won.agg(["mean", "size"]).round(3).to_dict())
print("TrueSense-recorded proposals: win by strong", ts.groupby("strong").won.agg(["mean", "size"]).round(3).to_dict())
bm = pp[pp.comp_group == "Bharat Machine Intelligence"]; print("BMI proposals by small band", bm.groupby(bm.band_idx <= 0).won.agg(["mean", "size"]).round(3).to_dict())
# Helix-incumbent share of qualified pipeline & overall win rate
print("win rate Helix-incumbent accounts by fy", q.groupby(["fy", "helix_inc"]).won.mean().unstack().round(3).to_dict())
l = q[~q.is_won]; print("share of FY26 Helix losses in Helix-incumbent accounts", round(l[(l.fy == 2026) & (l.comp_group == "Helix Automation")].helix_inc.mean(), 3))
print("TrueSense losses: reason split", l[l.comp_group == "TrueSense AI"].loss_reason.value_counts(normalize=True).round(2).to_dict())
print("TrueSense loss accounts existing CM", l[l.comp_group == "TrueSense AI"].acc_existing_condition_monitoring.value_counts(normalize=True).round(2).to_dict())
# ---- H5 channel
print("\n== H5")
q["ps"] = q.partner_sourced_adj
print(q.pivot_table(index="region", columns="ps", values="won", aggfunc=["mean", "size"]).round(3))
print("partner-sourced win by region & fy", q[q.ps].groupby(["region", "fy"]).won.mean().unstack().round(2))
w = o[o.is_won].copy()
for f in (2024, 2025, 2026):
    ww = w[w.fy == f]
    print(f, "partner-sourced share of bookings recorded", round(ww[ww.lead_source == "Partner"].first_year_value_lakh.sum() / ww.first_year_value_lakh.sum(), 3),
          "adjusted", round(ww[ww.partner_sourced_adj].first_year_value_lakh.sum() / ww.first_year_value_lakh.sum(), 3),
          "any partner", round(ww[ww.partner_id.notna()].first_year_value_lakh.sum() / ww.first_year_value_lakh.sum(), 3))
print("partner ids on FY26 partner-sourced deals", o[(o.fy == 2026) & o.partner_sourced_adj].partner_id.value_counts().to_dict())
print("partner cycle won", w.groupby("partner_sourced_adj").apply(lambda d: ((d.close_date - d.created_date).dt.days / 30.44).mean()).round(2).to_dict())
print("partner-sourced India helix-inc", q[q.ps & (q.region == "India")].groupby("helix_inc").won.agg(["mean", "size"]).round(3).to_dict())
# ---- H3 forecast
fh = pd.read_csv(D + "dr1_forecast_history.csv"); fh["fy"] = fh.quarter.str[-4:]
for k in ["commit_call_m1_cr", "commit_call_m2_cr", "commit_call_m3_cr"]:
    fh["err_" + k[12:14]] = (fh[k] - fh.bookings_reported_cr) / fh.bookings_reported_cr
fh["coverage"] = fh.reported_pipeline_in_quarter_cr / fh.quota_cr
fh["attain"] = fh.bookings_reported_cr / fh.quota_cr
fh["pipe_conv"] = fh.bookings_reported_cr / fh.reported_pipeline_in_quarter_cr
print("\n== H3"); print(fh[["quarter", "quota_cr", "reported_pipeline_in_quarter_cr", "coverage", "commit_call_m1_cr", "bookings_reported_cr", "err_m1", "err_m3", "attain", "pipe_conv"]].round(3).to_string())
print(fh.groupby("fy")[["err_m1", "err_m2", "err_m3"]].agg(lambda s: s.abs().mean()).round(3), fh.groupby("fy").err_m1.mean().round(3))
print(fh.groupby("fy")[["coverage", "attain", "pipe_conv"]].mean().round(3))
sn = pd.read_csv(D + "dr1_pipeline_snapshots.csv", parse_dates=["snapshot_date", "expected_close_date"])
oc = pd.read_csv("out/opps_clean.csv", parse_dates=["close_date"])
won_ids = oc[oc.is_won][["opp_id", "close_date"]]
sn = sn[sn.opp_id.isin(oc.opp_id)].merge(won_ids, on="opp_id", how="left")
sn["q_end"] = sn.snapshot_date + pd.DateOffset(months=3) - pd.Timedelta(days=1)
sn["inq"] = (sn.expected_close_date >= sn.snapshot_date) & (sn.expected_close_date <= sn.q_end)
sn["won_inq"] = sn.close_date.notna() & (sn.close_date <= sn.q_end)
sn["won_ever"] = sn.close_date.notna()
cat = sn[sn.inq].groupby(["forecast_category"]).apply(lambda d: pd.Series({"deals": len(d), "val_cr": d.first_year_value_lakh.sum() / 100,
      "won_in_q_val": d[d.won_inq].first_year_value_lakh.sum() / d.first_year_value_lakh.sum(), "won_ever_val": d[d.won_ever].first_year_value_lakh.sum() / d.first_year_value_lakh.sum()}))
print("in-quarter pipeline conversion by category (all 12 snapshots)"); print(cat.round(3))
sn["fy"] = np.where(sn.snapshot_date.dt.month >= 4, sn.snapshot_date.dt.year + 1, sn.snapshot_date.dt.year)
print("Commit conversion by FY", sn[sn.inq & (sn.forecast_category == "Commit")].groupby("fy").apply(lambda d: d[d.won_inq].first_year_value_lakh.sum() / d.first_year_value_lakh.sum()).round(3).to_dict())
st = sn[sn.inq].groupby("stage").apply(lambda d: d[d.won_inq].first_year_value_lakh.sum() / d.first_year_value_lakh.sum()); print("in-quarter conversion by stage", st.round(3).to_dict())
# open pipeline hygiene at 31 Mar 2026
op = o[~o.is_closed].copy(); asof = pd.Timestamp("2026-03-31")
op["stale"] = (op.close_date < asof) | (op.last_activity_date < asof - pd.Timedelta(days=90)) | (op.close_date_push_count >= 2)
print("open deals", len(op), "value cr", round(op.first_year_value_lakh.sum() / 100, 1), "stale share value", round(op[op.stale].first_year_value_lakh.sum() / op.first_year_value_lakh.sum(), 3),
      "single-thread share value", round(op[op.contacts_engaged == 1].first_year_value_lakh.sum() / op.first_year_value_lakh.sum(), 3))
print("open by stage value cr", (op.groupby("stage").first_year_value_lakh.sum() / 100).round(1).to_dict())
pd.to_pickle(dict(fh=fh, cat=cat, stage_conv=st), "out/h3.pkl")
