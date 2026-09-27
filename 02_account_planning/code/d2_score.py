"""D2 step 1: account score = P(win | qualified) x expected first-year ARR; back-test; tier the 3,100 targets."""
import pandas as pd, numpy as np, statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score
D = "/home/claude/strata/out/csv/"
q = pd.read_pickle("../d1/out/q_scored.pkl")          # qualified closed deals FY24-26 with fit score (trained FY24-25)
t = pd.read_pickle("../d1/out/targets_scored.pkl")    # 3,100 targets with fit score
t["existing_condition_monitoring"] = t.existing_condition_monitoring.fillna("None")
# ---- deal-size model on won deals (firmographics only)
w = q[q.won == 1].copy(); w["lv"] = np.log(w.first_year_value_lakh)
sm = smf.ols("lv ~ log_assets + band_idx + C(region) + C(seg)", w).fit()
print("deal size model R2", round(sm.rsquared, 3)); print(sm.params.round(3))
resid_var = sm.mse_resid
def exp_size(df): return np.exp(sm.predict(df) + resid_var / 2)
q["exp_arr_lakh"] = exp_size(q); t["exp_arr_lakh"] = exp_size(t)
q["ev_lakh"] = q.fit_score * q.exp_arr_lakh; t["ev_lakh"] = t.fit_score * t.exp_arr_lakh
# ---- back-test (out of time): FY26 deals, models trained on FY24-25 only
te = q[q.fy == 2026]
print("AUC fit (win) FY26", round(roc_auc_score(te.won, te.fit_score), 3), " AUC EV (win)", round(roc_auc_score(te.won, te.ev_lakh), 3))
# ---- tier thresholds on the 3,100 targets
t = t.sort_values("ev_lakh", ascending=False).reset_index(drop=True)
t["ev_rank"] = np.arange(1, len(t) + 1)
N_STRAT, N_SCALED = 400, 1100
thr_s = t.ev_lakh.iloc[N_STRAT - 1]; thr_c = t.ev_lakh.iloc[N_STRAT + N_SCALED - 1]
def tier(df):
    base = np.where(df.ev_lakh >= thr_s, "1 Strategic", np.where(df.ev_lakh >= thr_c, "2 Scaled", "3 Low-touch"))
    return pd.Series(base, index=df.index)
t["tier"] = tier(t); q["tier"] = tier(q)
# cap Helix-incumbent accounts in the strategic tier at the 40 highest-EV (win rate in Helix-incumbent accounts fell to 7% in FY26)
hx = t[(t.tier == "1 Strategic") & t.helix_inc].sort_values("ev_lakh", ascending=False)
demote = hx.index[40:]
t.loc[demote, "tier"] = "2 Scaled"; t.loc[demote, "helix_hold"] = True
fill = t[(t.tier == "2 Scaled") & ~t.helix_inc].sort_values("ev_lakh", ascending=False).index[:len(demote)]
t.loc[fill, "tier"] = "1 Strategic"
t["helix_hold"] = t["helix_hold"].astype("boolean").fillna(False).astype(bool)
# plays / overlays
t["play"] = np.select([
    t.helix_inc & (t.tier == "1 Strategic"),
    t.helix_hold.values,
    t.existing_condition_monitoring.eq("Wireless third-party"),
    t.region.eq("SEA") & (t.tier != "1 Strategic"),
    t.tier.eq("3 Low-touch") & t.region.eq("India") & (t.fit_tier.astype(str) == "Low fit")],
    ["Helix displacement (named 40)", "Helix: hold until pricing decision", "Sensor-agnostic risk (TrueSense)", "Partner-led (SEA)", "Stop-list: marketing nurture only"], default="Standard")
t["need_signal"] = t.existing_condition_monitoring.map({"None": "High", "Portable / route-based": "High", "Online wired": "Medium", "Wireless third-party": "Low"})
# ---- back-test by tier: past deals (FY24-26) and FY26 out-of-time
bt = q.groupby("tier").agg(deals=("won", "size"), win_rate=("won", "mean"), avg_won_lakh=("first_year_value_lakh", lambda s: s[q.loc[s.index, "won"] == 1].mean()),
                           won_arr_cr=("first_year_value_lakh", lambda s: s[q.loc[s.index, "won"] == 1].sum() / 100))
bt["arr_per_qual_opp_lakh"] = bt.won_arr_cr * 100 / bt.deals
bt26 = te.assign(tier=tier(te)).groupby("tier").won.agg(["mean", "size"])
print("\n== back-test FY24-26 by tier"); print(bt.round(3)); print("FY26 only (out of time)"); print(bt26.round(3))
print("share of won ARR FY24-26 by tier", (bt.won_arr_cr / bt.won_arr_cr.sum()).round(3).to_dict(), "share of deals", (bt.deals / bt.deals.sum()).round(3).to_dict())
# ---- target universe summary
summ = t.groupby("tier").agg(accounts=("account_id", "size"), ev_total_cr=("ev_lakh", lambda s: s.sum() / 100), exp_arr_avg_lakh=("exp_arr_lakh", "mean"),
      p_win_avg=("fit_score", "mean"), touches_fy26=("ae_touches_fy26", "sum"), helix=("helix_inc", "mean"), open_opp=("open_opportunity", lambda s: (s == "Y").sum()))
summ["touch_share"] = summ.touches_fy26 / summ.touches_fy26.sum()
print("\n== targets by tier"); print(summ.round(3))
print(pd.crosstab(t.tier, t.region)); print(t.play.value_counts())
print(pd.crosstab(t.tier, t.segment))
t.to_pickle("out/targets_tiered.pkl"); q.to_pickle("out/q_tiered.pkl")
pd.to_pickle(dict(sm=sm.params, r2=sm.rsquared, rv=resid_var, thr=(thr_s, thr_c), bt=bt, bt26=bt26, summ=summ,
                  auc=(roc_auc_score(te.won, te.fit_score), roc_auc_score(te.won, te.ev_lakh))), "out/score.pkl")
