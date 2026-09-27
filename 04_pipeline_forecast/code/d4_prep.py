"""D4 step 1: snapshot feature table (quarter-start snapshots Apr 2023 - Apr 2026) joined to clean CRM; outcome = won within the quarter."""
import pandas as pd, numpy as np
D = "/home/claude/strata/out/csv/"
o = pd.read_csv("/home/claude/strata/d1/out/opps_clean.csv", parse_dates=["created_date", "close_date"])
cd = pd.read_csv(D + "dr1_close_date_history.csv", parse_dates=["change_date"])
sn = pd.read_csv(D + "dr1_pipeline_snapshots.csv", parse_dates=["snapshot_date", "expected_close_date"])
ho = pd.read_excel("out/DR1b_holdout_snapshot_1Apr2026.xlsx", sheet_name="pipeline_snapshot_1apr2026", parse_dates=["snapshot_date", "expected_close_date"])
sn = pd.concat([sn, ho], ignore_index=True)
sn = sn[sn.opp_id.isin(o.opp_id)].copy()                     # drops test/duplicate ids (none expected)
o_ = o.set_index("opp_id")
sn["created_date"] = sn.opp_id.map(o_.created_date)
sn["segment"] = sn.opp_id.map(o_.segment); sn["region"] = sn.opp_id.map(o_.region); sn["lead_source"] = sn.opp_id.map(o_.lead_source).fillna("Unknown")
sn["q_end"] = sn.snapshot_date + pd.DateOffset(months=3) - pd.Timedelta(days=1)
sn["age_m"] = (sn.snapshot_date - sn.created_date).dt.days / 30.44
sn["stage_n"] = sn.stage.str[0].astype(int)
sn["inq"] = (sn.expected_close_date >= sn.snapshot_date) & (sn.expected_close_date <= sn.q_end)
sn["stale"] = sn.expected_close_date < sn.snapshot_date
sn["later"] = sn.expected_close_date > sn.q_end
pc = []
for s, g in sn.groupby("snapshot_date"):
    c = cd[cd.change_date < s].groupby("opp_id").size()
    pc.append(g.opp_id.map(c).fillna(0))
sn["pushes"] = pd.concat(pc).reindex(sn.index)
# outcome (not used for the hold-out snapshot until scoring)
won = o[o.is_won].set_index("opp_id").close_date
sn["won_in_q"] = sn.opp_id.map(won).le(sn.q_end) & sn.opp_id.isin(won.index)
sn["val_cr"] = sn.first_year_value_lakh / 100
sn["qtr"] = sn.snapshot_date.dt.strftime("%Y-%m-%d")
# actual clean bookings per quarter (= DR3 new-logo ARR) and bookings from deals NOT in the snapshot ("new in quarter")
w = o[o.is_won].copy()
qs = sorted(sn.snapshot_date.unique())
act = []
for s in qs:
    s = pd.Timestamp(s); e = s + pd.DateOffset(months=3) - pd.Timedelta(days=1)
    ww = w[(w.close_date >= s) & (w.close_date <= e)]
    in_snap = set(sn[sn.snapshot_date == s].opp_id)
    act.append(dict(snapshot_date=s, actual_cr=ww.first_year_value_lakh.sum() / 100 if e <= pd.Timestamp("2026-03-31") else np.nan,
                    new_in_q_cr=ww[~ww.opp_id.isin(in_snap)].first_year_value_lakh.sum() / 100 if e <= pd.Timestamp("2026-03-31") else np.nan))
act = pd.DataFrame(act)
print(act.round(2).to_string())
print(sn.groupby("snapshot_date").agg(n=("opp_id", "size"), val=("val_cr", "sum"), inq=("inq", "sum")).round(1).tail(4))
sn.to_pickle("out/snap.pkl"); act.to_pickle("out/actuals.pkl")
