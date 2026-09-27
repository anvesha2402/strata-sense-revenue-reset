"""D1 step 3e: size root causes in Rs crore of annual ARR (FY26 run-rate basis)."""
import pandas as pd, numpy as np
q = pd.read_pickle("out/q_scored.pkl"); A = pd.read_pickle("out/arr.pkl"); M = pd.read_pickle("out/model.pkl")
o = pd.read_pickle("out/opps_analysis.pkl")
w26 = o[o.is_won & (o.fy == 2026)]; avg = w26.first_year_value_lakh.mean() / 100
n26 = (q.fy == 2026).sum()
d = M["decomp"]
S = {}
S["winrate_total"] = n26 * (d["a24"] - d["a26"]) * avg
S["winrate_mix"] = n26 * (d["p24"] - d["p26_24"]) * avg
S["winrate_within"] = n26 * (d["p26_24"] - d["p26"]) * avg
S["mix_fit"] = -n26 * M["contrib"]["fit_score_logit"] * avg
S["mix_threading"] = -n26 * M["contrib"]["threading"] * avg
S["mix_committee"] = -n26 * M["contrib"]["buyer_committee_includes_fin_proc_it"] * avg
hx = q[q.helix_inc]; nh = q[~q.helix_inc]
wr = q.groupby(["fy", "helix_inc"]).won.mean().unstack()
S["helix_newlogo"] = (hx.fy == 2026).sum() * (wr.loc[2024, True] - wr.loc[2026, True]) * avg
S["nonhelix_newlogo"] = (nh.fy == 2026).sum() * (wr.loc[2024, False] - wr.loc[2026, False]) * avg
r = A["ret"]["helix_incumbent"]
S["helix_retention"] = (r[("FY25", "NRR")]["Helix incumbent"] - r[("FY26", "NRR")]["Helix incumbent"]) * r[("FY26", "opening")]["Helix incumbent"]
S["nonhelix_retention"] = (r[("FY25", "NRR")]["Other incumbent"] - r[("FY26", "NRR")]["Other incumbent"]) * r[("FY26", "opening")]["Other incumbent"]
br = A["br"]; S["nrr_total"] = (br.loc["FY25", "NRR"] - br.loc["FY26", "NRR"]) * br.loc["FY26", "opening"]
d24 = o[o.is_won & (o.fy == 2024)].discount_pct.mean(); d26 = w26.discount_pct.mean()
S["discount_leak"] = w26.first_year_value_lakh.sum() / 100 * ((1 - d24 / 100) / (1 - d26 / 100) - 1)
S["avg_deal_cr"] = avg; S["n26"] = n26; S["d24"] = d24; S["d26"] = d26
# cycle decomposition
w = o[o.is_won].copy(); w["cyc"] = (w.close_date - w.created_date).dt.days / 30.44
g = w.groupby(["fy", "buyer_committee_includes_fin_proc_it"]).cyc.mean().unstack(); sh = w.groupby("fy").buyer_committee_includes_fin_proc_it.apply(lambda s: (s == "Y").mean())
c24 = w[w.fy == 2024].cyc.mean(); c26 = w[w.fy == 2026].cyc.mean()
c26_at24 = g.loc[2024, "N"] * (1 - sh[2026]) + g.loc[2024, "Y"] * sh[2026]
S.update(cyc24=c24, cyc26=c26, cyc_mix=c26_at24 - c24, cyc_within=c26 - c26_at24)
for k, v in S.items(): print(f"{k:22s} {v:8.2f}")
pd.to_pickle(S, "out/sizing.pkl")
