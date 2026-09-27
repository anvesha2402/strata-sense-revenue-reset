import pandas as pd, numpy as np, warnings; warnings.filterwarnings("ignore")
from d4_methods import *
# walk-forward predictions for all quarters from index 1 using rolling window, then calibrated versions
def preds(window=4, use_cat=False):
    rows = []
    for i in range(1, 12):
        s = QS[i]; tr = sn[sn.snapshot_date.isin(QS[max(0, i - window):i])]; te = sn[sn.snapshot_date == s]
        if use_cat:
            tr = tr.assign(stage_n=tr.stage_n * 10 + tr.forecast_category.map({"Commit": 1, "Best Case": 2}).fillna(3))
            te = te.assign(stage_n=te.stage_n * 10 + te.forecast_category.map({"Commit": 1, "Best Case": 2}).fillna(3))
        a = act.set_index("snapshot_date").actual_cr[s]
        rows.append(dict(i=i, snapshot=s, actual=a, sw=m1(tr, te), ca=m2(tr if not use_cat else sn[sn.snapshot_date.isin(QS[max(0, i - window):i])], te if not use_cat else sn[sn.snapshot_date == s])))
    return pd.DataFrame(rows)
def calibrate(df, col, lookback=4, mode="median"):
    out = []
    for k, r in df.iterrows():
        past = df[(df.i < r.i) & (df.i >= r.i - lookback)]
        f = (past.actual / past[col]).median() if len(past) else 1.0
        out.append(r[col] * f)
    return np.array(out)
def mape(df, col): e = (df[col] - df.actual) / df.actual; return round(e.abs().mean(), 3), round(e.mean(), 3)
for w in (3, 4, 6):
    df = preds(w)
    for col in ("sw", "ca"):
        df[col + "_cal"] = calibrate(df, col)
    bt = df[df.i >= 4]
    print("window", w, {c: mape(bt, c) for c in ["sw", "ca", "sw_cal", "ca_cal"]})
df = preds(4, use_cat=True); df["sw_cal"] = calibrate(df, "sw"); bt = df[df.i >= 4]
print("with category", {c: mape(bt, c) for c in ["sw", "sw_cal"]})
