"""D1 step 3a: build the analysis table: qualified closed deals with account attributes, rep tenure and flags."""
import pandas as pd, numpy as np
D = "../../data/"
o = pd.read_csv("out/opps_clean.csv", parse_dates=["created_date", "close_date", "last_activity_date"])
sh = pd.read_csv("out/stage_history_clean.csv", parse_dates=["entered_date"])
t = pd.read_csv(D + "dr2_target_accounts.csv"); c = pd.read_csv(D + "dr2_customers.csv")
ae = pd.read_csv(D + "dr3_ae_roster.csv", parse_dates=["hire_date", "exit_date"])
attrs = ["segment", "region", "revenue_band", "plant_count", "installed_rotating_assets_est", "incumbent_automation_vendor"]
A = pd.concat([t[["account_id"] + attrs + ["existing_condition_monitoring"]],
               c[c.crm_account_id.notna()].rename(columns={"crm_account_id": "account_id"})[["account_id"] + attrs]])
A = A.drop_duplicates("account_id").set_index("account_id")
A.columns = ["acc_" + x for x in A.columns]
o = o.join(A, on="account_id")
print("account attribute coverage", o.acc_revenue_band.notna().mean().round(3), "cm coverage", o.acc_existing_condition_monitoring.notna().mean().round(3))
st = sh.groupby("opp_id").stage.apply(set)
o["stages"] = o.opp_id.map(st)
o["reached"] = o.stages.map(lambda s: max([int(x[0]) for x in s if x[0].isdigit()] + [6 if "Closed Won" in s else 0]) if isinstance(s, set) else 0)
o["qualified"] = o.reached >= 2
o["fy"] = np.where(o.close_date.dt.month >= 4, o.close_date.dt.year + 1, o.close_date.dt.year)
o = o.join(ae.set_index("ae_id")[["hire_date"]], on="owner_ae_id")
o["tenure_m"] = (o.created_date - o.hire_date).dt.days / 30.44
o["tenure_band"] = pd.cut(o.tenure_m, [-1e9, 9, 24, 1e9], labels=["<9 months", "9-24 months", ">24 months"])
o["tenure_band"] = o.tenure_band.astype(str).where(o.owner_reassigned == "N", "Reassigned deal")
o["threading"] = pd.cut(o.contacts_engaged, [0, 1, 2, 99], labels=["1 contact", "2 contacts", "3+ contacts"]).astype(str)
o["band_idx"] = o.acc_revenue_band.map({"< 500 cr": 0, "500-1,000 cr": 1, "1,000-5,000 cr": 2, "5,000-20,000 cr": 3, "> 20,000 cr": 4})
o["helix_inc"] = o.acc_incumbent_automation_vendor.eq("Helix Automation")
lr = o.loss_reason.fillna("")
comp = o.primary_competitor.copy()
comp = comp.where(comp.notna() & (comp != "None identified"), None)
# infer from loss reason when competitor blank
comp = comp.where(comp.notna() | ~lr.str.contains("bundled|existing vendor"), "Helix Automation (inferred)")
comp = comp.where(comp.notna() | ~lr.str.contains("existing sensors"), "TrueSense AI (inferred)")
o["competitor"] = comp.fillna(pd.Series(np.where(o.primary_competitor.eq("None identified"), "None identified", "Unknown"), index=o.index))
o["comp_group"] = o.competitor.str.replace(" (inferred)", "", regex=False)
o["lead_source_f"] = o.lead_source.fillna("Unknown")
o["partner_mistag"] = (o.partner_role == "Sourced") & (o.lead_source != "Partner")
o["partner_sourced_adj"] = (o.lead_source == "Partner") | o.partner_mistag
o.to_pickle("out/opps_analysis.pkl")
q = o[o.qualified & o.stage.isin(["Closed Won", "Closed Lost"])]
print("qualified closed", len(q), q.groupby("fy").size().to_dict())
print("partner mistag rows", o.partner_mistag.sum())
