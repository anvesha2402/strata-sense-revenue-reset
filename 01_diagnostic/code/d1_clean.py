"""D1 step 1: clean the DR1 CRM export and quantify the effect of each fix.
Inputs: data room CSVs only. Reference date = 31 Mar 2026 (export date)."""
import pandas as pd, numpy as np
D = "../../data/"
ASOF = pd.Timestamp("2026-03-31")
QUAL = ["2-Solution Design", "3-Proof of Value", "4-Proposal", "5-Negotiation & Procurement", "Closed Won"]

def fy(s): return pd.Series(np.where(s.dt.month >= 4, s.dt.year + 1, s.dt.year), index=s.index)

def load():
    o = pd.read_csv(D + "dr1_opportunities.csv", parse_dates=["created_date", "close_date", "last_activity_date"])
    sh = pd.read_csv(D + "dr1_stage_history.csv", parse_dates=["entered_date"])
    return o, sh

def headline(o, sh):
    q_ids = set(sh[sh.stage.isin(QUAL)].opp_id)
    c = o[o.is_closed & o.opp_id.isin(q_ids) & o.stage.isin(["Closed Won", "Closed Lost"])].copy(); c["fy"] = fy(c.close_date)
    w = o[o.is_won].copy(); w["fy"] = fy(w.close_date)
    allc = o[o.stage.isin(["Closed Won", "Closed Lost"])].copy(); allc["fy"] = fy(allc.close_date)
    w["cyc"] = (w.close_date - w.created_date).dt.days / 30.44
    out = pd.DataFrame({"qualified_closed": c.groupby("fy").size(), "win_rate": c.groupby("fy").is_won.mean(),
                        "wins": w.groupby("fy").size(), "bookings_cr": w.groupby("fy").first_year_value_lakh.sum() / 100,
                        "avg_deal_lakh": w.groupby("fy").first_year_value_lakh.mean(),
                        "cycle_m": w.groupby("fy").cyc.mean(),
                        "naive_win_rate_all_closed": allc.groupby("fy").is_won.mean(), "disc_pct": w.groupby("fy").discount_pct.mean()})
    return out.loc[[2024, 2025, 2026]]

def clean(o, sh, steps=("tests", "dups", "units", "dq", "dates")):
    o = o.copy(); sh = sh.copy(); log = {}
    if "tests" in steps:
        t = o.account_id.eq("T99999") | o.opp_name.str.startswith("TEST")
        log["tests"] = o.opp_id[t].tolist(); o = o[~t]; sh = sh[sh.opp_id.isin(o.opp_id)]
    if "units" in steps:
        u = o.first_year_value_lakh > 10000
        log["units"] = o.opp_id[u].tolist()
        o.loc[u, "first_year_value_lakh"] = o.loc[u, "first_year_value_lakh"] / 1e5
    if "dups" in steps:
        o = o.sort_values(["created_date", "opp_id"])
        drop = set(); pairs = []; near = []
        for acc, g in o.groupby("account_id"):
            if len(g) < 2: continue
            g = g.reset_index(drop=True)
            for i in range(len(g)):
                for j in range(i + 1, len(g)):
                    a, b = g.loc[i], g.loc[j]
                    if b.opp_id in drop or a.opp_id in drop: continue
                    if abs((b.created_date - a.created_date).days) <= 10 and \
                       abs(b.first_year_value_lakh - a.first_year_value_lakh) <= 0.02 * a.first_year_value_lakh:
                        if a.owner_ae_id == b.owner_ae_id and a.stage == b.stage:
                            drop.add(b.opp_id); pairs.append((a.opp_id, b.opp_id))
                        else:
                            near.append((a.opp_id, b.opp_id))
        log["dup_pairs"] = pairs; log["dup_candidates_kept"] = near; o = o[~o.opp_id.isin(drop)]; sh = sh[sh.opp_id.isin(o.opp_id)]
    if "dq" in steps:
        reached = set(sh[sh.stage.isin(QUAL[:-1])].opp_id)
        m = (o.stage == "Closed Lost") & ~o.opp_id.isin(reached)
        log["dq"] = o.opp_id[m].tolist()
        o.loc[m, "stage"] = "Disqualified"
        sh.loc[sh.opp_id.isin(log["dq"]) & (sh.stage == "Closed Lost"), "stage"] = "Disqualified"
    if "dates" in steps:
        bad = o.close_date < o.created_date
        fixed = o.loc[bad, "close_date"] + pd.DateOffset(years=1)
        ok = (fixed >= o.loc[bad, "created_date"]) & (fixed <= ASOF)
        log["dates_fixed"] = o.opp_id[bad][ok].tolist(); log["dates_excluded_from_cycle"] = o.opp_id[bad][~ok].tolist()
        o.loc[fixed[ok].index, "close_date"] = fixed[ok]
        o["cycle_excluded"] = o.opp_id.isin(log["dates_excluded_from_cycle"])
    return o, sh, log

if __name__ == "__main__":
    o, sh = load()
    rows = []
    base = headline(o, sh); rows.append(("0 Raw export", base))
    cum = []
    for s in ["tests", "dups", "units", "dq", "dates"]:
        cum.append(s); oc, shc, lg = clean(o, sh, tuple(cum))
        rows.append((f"+ {s}", headline(oc, shc)))
    oc, shc, log = clean(o, sh)
    for k, v in log.items(): print(k, len(v), v[:6])
    tab = pd.concat({k: v for k, v in rows}, names=["step", "fy"])
    print(tab.round(3).to_string())
    oc.to_csv("out/opps_clean.csv", index=False); shc.to_csv("out/stage_history_clean.csv", index=False)
    tab.round(4).to_csv("out/audit_waterfall.csv")
    pd.to_pickle(log, "out/clean_log.pkl")
