"""D4 step 4: performance views, stage ageing limits, hygiene flags on the 1 Apr 2026 snapshot, coverage by quarter."""
import pandas as pd, numpy as np
D = "/home/claude/strata/out/csv/"
q = pd.read_pickle("/home/claude/strata/d1/out/q_scored.pkl")
o = pd.read_pickle("/home/claude/strata/d1/out/opps_analysis.pkl")
sh = pd.read_csv("/home/claude/strata/d1/out/stage_history_clean.csv", parse_dates=["entered_date"])
sn = pd.read_pickle("out/snap.pkl"); fh = pd.read_csv(D + "dr1_forecast_history.csv"); act = pd.read_pickle("out/actuals.pkl")
q["cyc"] = (q.close_date - q.created_date).dt.days
q["comp_group"] = q.comp_group.replace({"None identified": "None / unknown", "Unknown": "None / unknown"})
dims = {"Segment": "segment", "Lead source": "lead_source_f", "Competitor (recorded)": "comp_group", "Rep tenure": "tenure_band", "Region": "region", "Account tier (D2)": None}
t2 = pd.read_pickle("/home/claude/strata/d2/out/q_tiered.pkl")[["opp_id", "tier"]]
q = q.merge(t2, on="opp_id", how="left"); dims["Account tier (D2)"] = "tier"
rows = []
for dn, col in dims.items():
    for (v, fy), g in q.groupby([col, "fy"]):
        w = g[g.won == 1]
        n = len(g); wr = g.won.mean(); deal = w.first_year_value_lakh.mean() if len(w) else 0; cyc = w.cyc.mean() if len(w) else np.nan
        rows.append(dict(dimension=dn, value=str(v), fy=f"FY{str(fy)[-2:]}", qualified_deals=n, win_rate=wr, avg_won_deal_lakh=deal,
                         avg_cycle_days=cyc, velocity_lakh_per_day=(n * wr * deal / cyc) if cyc and cyc > 0 else 0, key=f"{dn}|{v}|FY{str(fy)[-2:]}"))
perf = pd.DataFrame(rows)
# stage ageing: days spent in each stage for won deals FY25-26
sh = sh.sort_values(["opp_id", "entered_date"]); sh["next"] = sh.groupby("opp_id").entered_date.shift(-1)
sh["days"] = (sh.next - sh.entered_date).dt.days
wonids = set(o[o.is_won & (o.fy >= 2025)].opp_id)
st = sh[sh.opp_id.isin(wonids) & sh.stage.str[0].str.isdigit()].groupby("stage").days.describe(percentiles=[.5, .75, .9])[["count", "50%", "75%", "90%"]]
st["limit_days"] = (st["75%"] / 5).round() * 5
print(st.round(0))
# hygiene flags on the 1 Apr 2026 snapshot
h = sn[sn.snapshot_date == "2026-04-01"].copy()
ex = o.set_index("opp_id")
h["contacts"] = h.opp_id.map(ex.contacts_engaged); h["last_activity"] = h.opp_id.map(ex.last_activity_date)
h["business_case"] = h.opp_id.map(ex.business_case_attached)
entered = sh[sh.entered_date <= "2026-04-01"].groupby("opp_id").entered_date.max()
h["days_in_stage"] = (pd.Timestamp("2026-04-01") - h.opp_id.map(entered)).dt.days
lim = st.limit_days.to_dict(); h["stage_limit"] = h.stage.map(lim)
h["f_stale_date"] = h.stale
h["f_slipped2"] = h.pushes >= 2
h["f_aged"] = h.days_in_stage > h.stage_limit
h["f_single_thread"] = (h.contacts <= 1) & (h.stage_n >= 3)
h["f_no_activity_90d"] = h.last_activity < pd.Timestamp("2026-04-01") - pd.Timedelta(days=90)
h["f_commit_not_stage5"] = (h.forecast_category == "Commit") & (h.stage_n < 5)
fl = [c for c in h.columns if c.startswith("f_")]
h["any_flag"] = h[fl].any(axis=1)
summ = pd.DataFrame({f: [h[f].sum(), h.loc[h[f], "val_cr"].sum()] for f in fl + ["any_flag"]}, index=["deals", "value_cr"]).T
print(summ.round(1)); print("snapshot value", round(h.val_cr.sum(), 1), "in-quarter", round(h[h.inq].val_cr.sum(), 1), "in-quarter clean", round(h[h.inq & ~h.any_flag].val_cr.sum(), 1))
# coverage by quarter
cov = fh.copy(); cov["actual_clean_cr"] = act.actual_cr.values[:12]
cov["coverage_reported"] = cov.reported_pipeline_in_quarter_cr / cov.quota_cr
cov["inq_conversion"] = cov.actual_clean_cr / cov.reported_pipeline_in_quarter_cr
cov["conv_trailing4"] = cov.inq_conversion.rolling(4, min_periods=2).mean().shift(1)
cov["coverage_required"] = 1 / cov.conv_trailing4
cov["attainment"] = cov.actual_clean_cr / cov.quota_cr
q1 = dict(quarter="Q1 FY27", quota_cr=17.15, reported_pipeline_in_quarter_cr=round(h[h.inq & (h.stage_n >= 2)].val_cr.sum(), 2))
q1["coverage_reported"] = q1["reported_pipeline_in_quarter_cr"] / q1["quota_cr"]; q1["conv_trailing4"] = cov.inq_conversion.tail(4).mean(); q1["coverage_required"] = 1 / q1["conv_trailing4"]
cov = pd.concat([cov, pd.DataFrame([q1])], ignore_index=True)
print(cov[["quarter", "quota_cr", "reported_pipeline_in_quarter_cr", "coverage_reported", "coverage_required", "actual_clean_cr", "attainment"]].round(2).to_string())
pd.to_pickle(dict(perf=perf, stage_age=st, flags=h, flag_summary=summ, cov=cov), "out/views.pkl")
