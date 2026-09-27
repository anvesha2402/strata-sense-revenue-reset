"""D1 step 2: rebuild FY26 ARR bridge from the DR2 ledger; retention by cohort, segment, usage, incumbent."""
import pandas as pd, numpy as np
D = "../../data/"
m = pd.read_csv(D + "dr2_arr_movements.csv", parse_dates=["effective_date"])
c = pd.read_csv(D + "dr2_customers.csv", parse_dates=["customer_since", "churn_date"])
pl = pd.read_csv(D + "dr3_pl_quarterly.csv")
oc = pd.read_csv("out/opps_clean.csv", parse_dates=["close_date"])
m["fy"] = "FY" + m.fiscal_quarter.str[-2:]
br = m.pivot_table(index="fy", columns="movement_type", values="arr_change_cr", aggfunc="sum").fillna(0)
open_ = {"FY24": c.arr_mar2023_cr.sum(), "FY25": c.arr_mar2024_cr.sum(), "FY26": c.arr_mar2025_cr.sum()}
br["opening"] = pd.Series(open_)
br["closing_calc"] = br.opening + br[["New logo", "Expansion", "Contraction", "Churn"]].sum(axis=1)
br["closing_master"] = [c.arr_mar2024_cr.sum(), c.arr_mar2025_cr.sum(), c.arr_mar2026_cr.sum()]
br["GRR"] = (br.opening + br.Contraction + br.Churn) / br.opening
br["NRR"] = (br.opening + br.Expansion + br.Contraction + br.Churn) / br.opening
# CRM reconciliation
oc["fy"] = "FY" + pd.Series(np.where(oc.close_date.dt.month >= 4, oc.close_date.dt.year + 1, oc.close_date.dt.year)).astype(str).str[-2:].values
br["crm_clean_bookings"] = oc[oc.is_won].groupby("fy").first_year_value_lakh.sum() / 100
br["crm_raw_bookings"] = [41.62, 41.531, 44.054]
print(br.round(3).T.to_string())
fy26q = m[m.fy == "FY26"].pivot_table(index="fiscal_quarter", columns="movement_type", values="arr_change_cr", aggfunc="sum").round(2)
print(fy26q)
# ---- retention per customer for each FY
def ret(fy_prev, fy_cur, by):
    base = c[c[f"arr_mar{fy_prev}_cr"] > 0].copy()
    base["open"] = base[f"arr_mar{fy_prev}_cr"]; base["close"] = base[f"arr_mar{fy_cur}_cr"]
    base["churned"] = base.close == 0
    mv = m[m.fy == f"FY{str(fy_cur)[-2:]}"].pivot_table(index="customer_id", columns="movement_type", values="arr_change_cr", aggfunc="sum")
    base = base.join(mv, on="customer_id").fillna({"Expansion": 0, "Contraction": 0, "Churn": 0})
    g = base.groupby(by, observed=True).agg(customers=("customer_id", "size"), opening=("open", "sum"), exp=("Expansion", "sum"),
                                           con=("Contraction", "sum"), churn=("Churn", "sum"), logo_churn=("churned", "mean"))
    g["GRR"] = (g.opening + g.con + g.churn) / g.opening; g["NRR"] = (g.opening + g.exp + g.con + g.churn) / g.opening
    return g
c["cohort"] = np.where(c.customer_since.dt.month >= 4, c.customer_since.dt.year + 1, c.customer_since.dt.year)
c["cohort_band"] = pd.cut(c.cohort, [0, 2020, 2022, 2023, 2024, 2025], labels=["FY20 or earlier", "FY21-22", "FY23", "FY24", "FY25"])
c["usage_band"] = pd.cut(c.usage_pct_90d, [0, 0.5, 0.7, 1.01], labels=["<50%", "50-70%", ">70%"])
c["helix_incumbent"] = np.where(c.incumbent_automation_vendor == "Helix Automation", "Helix incumbent", "Other incumbent")
c["size_band"] = pd.cut(c.arr_mar2025_cr, [-1, 0.25, 0.75, 2, 100], labels=["<0.25 cr", "0.25-0.75", "0.75-2", ">2 cr"])
out = {}
for by in ["cohort_band", "segment", "region", "usage_band", "helix_incumbent", "size_band"]:
    t = pd.concat({"FY25": ret(2024, 2025, by), "FY26": ret(2025, 2026, by)}, axis=1)
    out[by] = t; print("\n==", by); v = pd.DataFrame({"NRR25": t[("FY25","NRR")], "NRR26": t[("FY26","NRR")], "GRR26": t[("FY26","GRR")], "n26": t[("FY26","customers")], "open26": t[("FY26","opening")], "logo_churn26": t[("FY26","logo_churn")], "churn26": t[("FY26","churn")], "con26": t[("FY26","con")], "exp26": t[("FY26","exp")]}); print(v.round(3).to_string())
# expansion concentration: top-30 accounts at FY25 end — expansion FY25 vs FY26
top = c.nlargest(30, "arr_mar2025_cr").customer_id
for f in ("FY25", "FY26"):
    x = m[(m.fy == f) & m.customer_id.isin(top) & (m.movement_type == "Expansion")].arr_change_cr.sum()
    print(f, "expansion from top-30 (by Mar-25 ARR):", round(x, 2))
# whitespace
act = c[c.status == "Active"].copy(); act["ws_assets"] = act.installed_rotating_assets_est - act.assets_licensed
act["ws_share"] = act.assets_licensed / act.installed_rotating_assets_est
print("active licensed/installed median", act.ws_share.median().round(3), "top30 whitespace assets", act.nlargest(30, "arr_mar2026_cr").ws_assets.sum())
print("implied whitespace ARR (Rs cr) at avg price", round((act.ws_assets * (act.arr_mar2026_cr / act.assets_licensed)).sum(), 1))
print("top30 whitespace ARR", round((act.nlargest(30, "arr_mar2026_cr").pipe(lambda d: d.ws_assets * d.arr_mar2026_cr / d.assets_licensed)).sum(), 1))
# billing-unit duplicates
act["stem"] = act.account_name.str.replace(r" - Unit 2 Ltd| \(Unit 2\)", "", regex=True).str.replace(" Ltd", "")
print("unit-2 billing accounts", act.account_name.str.contains("Unit 2").sum())
# FY27 renewal exposure
act["renew_q"] = act.next_renewal_date
print(act.nlargest(5, "arr_mar2026_cr")[["customer_id", "account_name", "arr_mar2026_cr", "incumbent_automation_vendor", "next_renewal_date", "usage_pct_90d"]])
low = act[act.usage_pct_90d < 0.5]; print("active low-usage: n", len(low), "ARR", round(low.arr_mar2026_cr.sum(), 1), "helix inc share", round((low.incumbent_automation_vendor == "Helix Automation").mean(), 2))
pd.to_pickle(dict(br=br, fy26q=fy26q, ret=out), "out/arr.pkl")
