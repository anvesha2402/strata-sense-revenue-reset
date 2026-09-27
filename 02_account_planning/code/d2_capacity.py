"""D2 step 2: AE supply by tenure band for FY27 (deterministic cohort model) and baseline direct capacity."""
import pandas as pd, numpy as np
D = "/home/claude/strata/out/csv/"
r = pd.read_csv(D + "dr3_ae_roster.csv", parse_dates=["hire_date"])
act = r[r.status_31mar2026 == "Active"].copy()
ten0 = ((pd.Timestamp("2026-03-31") - act.hire_date).dt.days / 30.44).values
PROD = {"0-6": 0.0, "6-12": 0.29, "12-24": 0.59, "24+": 0.89}      # Rs cr per AE-year, D1 (DR3 ae_quarterly FY24-26)
def band(m): return "0-6" if m < 6 else "6-12" if m < 12 else "12-24" if m < 24 else "24+"
def simulate(net_new=(0, 0, 0, 0), q_attr=0.29 / 4):
    cohorts = [[m, 1.0] for m in ten0]              # [tenure months at start of quarter, weight]
    rows = []
    for qi in range(4):
        for _ in range(net_new[qi]): cohorts.append([0.0, 1.0])
        hc = sum(w for _, w in cohorts)
        # exits this quarter, weighted toward 6-20 months tenure (DR3 pattern)
        wts = np.array([w * (1.6 if 6 <= m <= 20 else 0.8) for m, w in cohorts]); exits = q_attr * hc
        share = wts / wts.sum() * exits
        ae_q = {b: 0.0 for b in PROD}
        for (m, w), e in zip(cohorts, share):
            ae_q[band(m + 1.5)] += (w - e / 2) / 4       # AE-years this quarter (leavers count half)
        rows.append(dict(quarter=f"Q{qi+1} FY27", headcount_start=hc, exits=exits, **{f"ae_years_{b}": v for b, v in ae_q.items()}))
        cohorts = [[m + 3, w - e] for (m, w), e in zip(cohorts, share)] + [[0.0, exits]]   # backfill at quarter end
    df = pd.DataFrame(rows)
    df["capacity_cr_at_fy26_productivity"] = sum(df[f"ae_years_{b}"] * p for b, p in PROD.items())
    return df
A = simulate(); B = simulate(net_new=(6, 6, 0, 0))
for n, d in (("A: hold 64", A), ("B: +12 net new in H1 (76)", B)):
    print(n); print(d.round(2).to_string()); print("FY27 capacity", round(d.capacity_cr_at_fy26_productivity.sum(), 1), "AE-years", round(d.filter(like="ae_years").sum().sum(), 1))
print("tenure mix now", pd.Series([band(m) for m in ten0]).value_counts().to_dict())
pd.to_pickle(dict(A=A, B=B, PROD=PROD, mix=pd.Series([band(m) for m in ten0]).value_counts()), "out/capacity.pkl")
