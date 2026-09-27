"""D1 step 3b: funnel decomposition — win rate, cycle, discount by cut and year."""
import pandas as pd, numpy as np
o = pd.read_pickle("out/opps_analysis.pkl")
q = o[o.qualified & o.stage.isin(["Closed Won", "Closed Lost"])].copy()
w = o[o.is_won].copy(); w["cyc"] = (w.close_date - w.created_date).dt.days / 30.44
R = {}
def cut(col, df=q, min_n=15):
    g = df.groupby([col, "fy"], observed=True).is_won.agg(["mean", "size"]).unstack("fy")
    g.columns = [f"{a}_{b}" for a, b in g.columns]
    return g
print("== headline"); print(q.groupby("fy").is_won.agg(["mean", "size"]).round(3).T)
for col in ["segment", "region", "lead_source_f", "comp_group", "tenure_band", "threading", "acc_revenue_band", "buyer_committee_includes_fin_proc_it", "proof_of_value"]:
    R[col] = cut(col); print("\n==", col); print(R[col].round(3).to_string())
p = q[q.reached >= 4].copy()
print("\n== proposals: business case"); R["bc"] = cut("business_case_attached", p); print(R["bc"].round(3))
p["disc_band"] = pd.cut(p.discount_pct, [-1, 10, 15, 20, 25, 60], labels=["<=10%", "10-15%", "15-20%", "20-25%", ">25%"])
print("\n== proposals: discount band"); R["disc"] = p.groupby("disc_band", observed=True).is_won.agg(["mean", "size"]); print(R["disc"].round(3))
print("discount band within competitor:"); print(p.pivot_table(index="disc_band", columns="comp_group", values="is_won", aggfunc="mean", observed=True).round(2))
print("\n== competitor x Helix incumbent"); R["comp_helix"] = q.pivot_table(index="comp_group", columns="helix_inc", values="is_won", aggfunc=["mean", "size"]); print(R["comp_helix"].round(3))
# share of losses FY26
l26 = q[(q.fy == 2026) & ~q.is_won]
lt = np.where(l26.comp_group.isin(["Helix Automation", "TrueSense AI", "Bharat Machine Intelligence"]), l26.comp_group,
     np.where(l26.loss_reason.fillna("").str.contains("No decision|Budget|deferred|IT security"), "No decision", "Unattributed"))
R["loss_mix"] = pd.Series(lt).value_counts(); print("\n== FY26 loss attribution"); print(R["loss_mix"], (R["loss_mix"] / R["loss_mix"].drop("Unattributed").sum()).round(3))
# stage conversion by close FY (qualified closed deals): share reaching each stage
print("\n== stage reach (qualified closed deals)")
sr = pd.DataFrame({f"reach_{s}": q.groupby("fy").reached.apply(lambda x: (x >= s).mean()) for s in [3, 4, 5, 6]}); R["stage_reach"] = sr; print(sr.round(3))
cond = pd.DataFrame({"2->3+": sr.reach_3, "3->4": sr.reach_4 / sr.reach_3, "4->5": sr.reach_5 / sr.reach_4, "5->won": sr.reach_6 / sr.reach_5}); print(cond.round(3))
# cycle & discount for won
print("\n== won cycle by cut, months")
for col in ["buyer_committee_includes_fin_proc_it", "threading", "comp_group", "proof_of_value", "region"]:
    print(w.groupby([col, "fy"]).cyc.mean().unstack().round(2))
R["cyc_committee"] = w.groupby(["buyer_committee_includes_fin_proc_it", "fy"]).cyc.mean().unstack()
print("committee share of won deals", w.groupby("fy").buyer_committee_includes_fin_proc_it.apply(lambda s: (s == "Y").mean()).round(3).to_dict())
print("won discount by comp", w.groupby(["comp_group", "fy"]).discount_pct.mean().unstack().round(1))
print("won discount by BC", w.groupby(["business_case_attached", "fy"]).discount_pct.mean().unstack().round(1))
# composition of qualified deals
comp = q.groupby("fy").agg(single=("threading", lambda s: (s == "1 contact").mean()), junior=("tenure_band", lambda s: (s == "<9 months").mean()),
    reassigned=("tenure_band", lambda s: (s == "Reassigned deal").mean()), helix=("comp_group", lambda s: (s == "Helix Automation").mean()),
    truesense=("comp_group", lambda s: (s == "TrueSense AI").mean()), small=("band_idx", lambda s: (s <= 0).mean()),
    other_seg=("segment", lambda s: (s == "Other").mean()), committee=("buyer_committee_includes_fin_proc_it", lambda s: (s == "Y").mean()),
    helix_inc=("helix_inc", "mean"))
R["composition"] = comp; print("\n== composition of qualified closed deals"); print(comp.round(3))
pd.to_pickle(R, "out/funnel.pkl")
