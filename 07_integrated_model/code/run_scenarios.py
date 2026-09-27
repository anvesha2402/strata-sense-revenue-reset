"""Runs the D7 workbook under each scenario and sensitivity shift (LibreOffice recalc), then writes the saved-run sheets back into the model."""
import json, shutil, subprocess, os
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
M = json.load(open("out/rowmap.json")); R = M["R"]
BASE = "out/D7_Integrated_Model.xlsx"; TMP = "/tmp/claude-0/d7run.xlsx"
RECALC = "/mnt/skills/public/xlsx/scripts/recalc.py"
def run(scn="Base", **shift):
    wb = load_workbook(BASE); a = wb["Assumptions"]; a["C4"] = scn
    for k in ("dwin", "dcyc", "ddisc", "dpp", "dchurn", "ddel"): a[f"B{R[k]}"] = shift.get(k, 1 if k == "ddel" else 0)
    wb.save(TMP); subprocess.run(["python3", RECALC, TMP, "90"], capture_output=True)
    d = load_workbook(TMP, data_only=True)
    g = lambda ws, ref: d[ws][ref].value
    ab, ann, pl, hc, br, ir, CAP = M["ab"], M["ann"], M["pl"], M["hc"], M["br"], M["ir"], M["CAP"]
    out = {f"ARR {y}": g("ARR_bridge", f"{c}{ab['close']}") for y, c in zip(("FY27", "FY28", "FY29"), "OPQ")}
    out.update({f"Growth {y}": g("ARR_bridge", f"{c}{ann['growth']}") for y, c in zip(("FY27", "FY28", "FY29"), "OPQ")})
    out.update({f"New logo {y}": g("ARR_bridge", f"{c}{ann['nl']}") for y, c in zip(("FY27", "FY28", "FY29"), "OPQ")})
    out.update({f"NRR {y}": g("ARR_bridge", f"{c}{ann['nrr']}") for y, c in zip(("FY27", "FY29"), "OQ")})
    out["Partner share FY29"] = g("Channel", f"Q{hc['share']}")
    out["GM min year"] = min(g("PnL", f"{c}{pl['gmpost']}") for c in "OPQ")
    cac = [g("PnL", f"{c}{pl['cac']}") for c in "CDEFGHIJKLMN"]; out["CAC worst qtr"] = max(cac); out["CAC Q4 FY28"] = cac[7]
    out["CAC worst qtr from Q2 FY27"] = max(cac[1:])
    out["S&M/ARR FY29"] = g("PnL", f"Q{pl['smarr']}")
    out.update({f"EBITDA {y}": g("PnL", f"{c}{pl['ebitda']}") for y, c in zip(("FY27", "FY28", "FY29"), "OPQ")})
    out["Investment FY27"] = g("Investment", f"J{ir['tot']}"); out["Investment FY27-29"] = g("Investment", f"L{ir['cum']}")
    out["Investment payback FY29 (months)"] = g("Investment", f"L{ir['pbk']}")
    out["Investment payback FY29 vs FY26-flat (months)"] = g("Investment", f"L{ir['pbk2']}")
    out["AE headcount end FY29"] = g("Capacity", f"Q{CAP['hc']}")
    ck = d["Checks"]; n = [ck[f"C{r}"].value for r in range(5, 40)]
    out["Guardrails failed"] = sum(1 for v in n if v in ("ERROR", "OVER", "BREACH")); out["Board-goal shortfalls"] = sum(1 for v in n if v == "SHORTFALL")
    casc = [d["Cascade"][f"E{5 + k}"].value for k in range(len(M["casc"]))]
    return out, casc
res = {}
for s in ("Base", "Downside", "Aggressive", "CFO-capped"):
    res[s] = run(s); print(s, round(res[s][0]["ARR FY29"], 1), res[s][0]["Guardrails failed"])
sens = {}
SENS = [("Win rate", "dwin", 3, "pts"), ("Sales cycle", "dcyc", 1, "months"), ("Discount", "ddisc", 3, "pts"), ("Partner productivity", "dpp", 0.30, "%"), ("Churn", "dchurn", 2, "pts")]
for lab, k, v, u in SENS:
    for sg in (-1, 1):
        sens[(lab, sg)] = run("Base", **{k: sg * v})[0]; print(lab, sg, round(sens[(lab, sg)]["ARR FY29"], 1))
# break-evens: the shift at which a payback test fails
def num(x): return 999 if isinstance(x, str) else x
TESTS = [("CAC payback Q4 FY28 > 24 months", "CAC Q4 FY28", 24), ("CAC payback > 30 months in any quarter from Q2 FY27", "CAC worst qtr from Q2 FY27", 30),
         ("Investment payback vs FY26-flat > 30 months (FY29)", "Investment payback FY29 vs FY26-flat (months)", 30)]
DRIVERS = [("Win rate (pts)", "dwin", -14.0, 0.0, False), ("Churn (pts)", "dchurn", 0.0, 14.0, True), ("Plan delivery (share)", "ddel", 0.0, 1.0, False)]
be = {}
for tlab, metric, thr in TESTS:
    for dlab, k, lo, hi, up in DRIVERS:
        f = lambda v: num(run("Base", **{k: v})[0][metric])
        if f(lo if up else hi) > thr: be[f"{tlab} | {dlab}"] = "fails at plan"; continue
        if f(hi if up else lo) <= thr: be[f"{tlab} | {dlab}"] = "never in range"; continue
        for _ in range(7):
            mid = (lo + hi) / 2; p = f(mid)
            if up: lo, hi = (mid, hi) if p <= thr else (lo, mid)
            else: lo, hi = (lo, mid) if p <= thr else (mid, hi)
        be[f"{tlab} | {dlab}"] = round((lo + hi) / 2, 3); print(tlab, dlab, be[f"{tlab} | {dlab}"])
json.dump(dict(res={k: v[0] for k, v in res.items()}, casc_base=res["Base"][1], sens={f"{a}|{b}": v for (a, b), v in sens.items()}, be=be), open("out/runs.json", "w"), indent=1, default=str)
plus3 = run("Base", dwin=3)[1]
json.dump(plus3, open("out/casc_plus3.json", "w"))
print("done")
