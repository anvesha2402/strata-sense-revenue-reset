"""D4 step 2: forecast methods and back-test (8 quarters, no look-ahead)."""
import pandas as pd, numpy as np, statsmodels.formula.api as smf, warnings
warnings.filterwarnings("ignore")
D = "/home/claude/strata/out/csv/"
sn = pd.read_pickle("out/snap.pkl"); act = pd.read_pickle("out/actuals.pkl")
fh = pd.read_csv(D + "dr1_forecast_history.csv", parse_dates=["quarter_start"])
QS = sorted(sn.snapshot_date.unique())
def bucket(df): return np.where(df.stale, "stale", np.where(df.inq, "inq", "later"))
def agebin(a): return pd.cut(a, [-1, 3, 6, 9, 12, 1e9], labels=["0-3", "3-6", "6-9", "9-12", "12+"]).astype(str)
def sgrp(s): return np.where(s <= 2, "early", np.where(s == 3, "mid", "late"))
def rate_table(tr, keys, k=3.0):
    base = tr.groupby("stage_n").apply(lambda g: (g.val_cr * g.won_in_q).sum() / g.val_cr.sum())
    g = tr.groupby(keys).apply(lambda d: pd.Series({"w": (d.val_cr * d.won_in_q).sum(), "v": d.val_cr.sum(), "n": len(d)}))
    return g, base
def m1(tr, te):
    tr = tr.assign(b=bucket(tr)); te = te.assign(b=bucket(te))
    g = tr.groupby(["stage_n", "b"]).apply(lambda d: pd.Series({"w": (d.val_cr * d.won_in_q).sum(), "v": d.val_cr.sum(), "n": len(d)}))
    st = tr.groupby("stage_n").apply(lambda d: (d.val_cr * d.won_in_q).sum() / d.val_cr.sum())
    k = 5
    rate = ((g.w + k * st.reindex(g.index.get_level_values(0)).values * (g.v / g.n)) / (g.v + k * (g.v / g.n)))
    r = te.apply(lambda x: rate.get((x.stage_n, x.b), st.get(x.stage_n, 0)), axis=1)
    return (te.val_cr * r).sum()
def m2(tr, te):
    tr = tr.assign(a=agebin(tr.age_m), s=sgrp(tr.stage_n)); te = te.assign(a=agebin(te.age_m), s=sgrp(te.stage_n))
    g = tr.groupby(["s", "a"]).apply(lambda d: (d.val_cr * d.won_in_q).sum() / d.val_cr.sum())
    sg = tr.groupby("s").apply(lambda d: (d.val_cr * d.won_in_q).sum() / d.val_cr.sum())
    r = te.apply(lambda x: g.get((x.s, x.a), sg.get(x.s, 0)), axis=1)
    return (te.val_cr * r).sum()
FORM = "won ~ C(stage_n) + inq + stale + np.log(age_m + 0.5) + pushes + np.log(val_cr)"
def m3(tr, te, sims=0, seed=1):
    tr = tr.assign(won=tr.won_in_q.astype(int)); te = te.copy()
    mod = smf.logit(FORM, tr).fit(disp=0, maxiter=200)
    p = mod.predict(te).clip(0, 1).values
    exp = (te.val_cr.values * p).sum()
    if not sims: return exp
    rng = np.random.default_rng(seed)
    draws = (rng.random((sims, len(p))) < p) @ te.val_cr.values
    return exp, np.percentile(draws, [10, 50, 90]), mod
def run(window=None):
    rows = []
    for i in range(4, 12):
        s = QS[i]; trq = QS[:i] if window is None else QS[max(0, i - window):i]
        tr = sn[sn.snapshot_date.isin(trq)]; te = sn[sn.snapshot_date == s]
        a = act.set_index("snapshot_date").actual_cr[s]
        e3, pct, _ = m3(tr, te, sims=4000)
        r = dict(quarter=fh.set_index("quarter_start").quarter.get(s), snapshot=s, actual=a, commit=fh.set_index("quarter_start").commit_call_m1_cr.get(s),
                 stage_weighted=m1(tr, te), cohort_age=m2(tr, te), simulation=e3, sim_p10=pct[0], sim_p90=pct[2])
        r["ensemble"] = np.mean([r["stage_weighted"], r["cohort_age"], r["simulation"]])
        rows.append(r)
    return pd.DataFrame(rows)
def score(bt):
    out = {}
    for m in ["commit", "stage_weighted", "cohort_age", "simulation", "ensemble"]:
        e = (bt[m] - bt.actual) / bt.actual
        out[m] = dict(MAPE=e.abs().mean(), bias=e.mean(), MAPE_last4=e.iloc[4:].abs().mean(), max_abs=e.abs().max())
    cov = ((bt.actual >= bt.sim_p10) & (bt.actual <= bt.sim_p90)).mean()
    return pd.DataFrame(out).T, cov
if __name__ == "__main__":
    res = {}
    for name, win in [("expanding", None), ("rolling4", 4)]:
        bt = run(win); sc, cov = score(bt); res[name] = (bt, sc, cov)
        print("==", name); print(bt.round(2).to_string()); print(sc.round(3)); print("p10-p90 coverage", cov)
    pd.to_pickle(res, "out/backtest.pkl")
