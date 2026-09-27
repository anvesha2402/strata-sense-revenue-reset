import pandas as pd, numpy as np, json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, BarChart, Reference, Series
from openpyxl.worksheet.datavalidation import DataValidation
V = pd.read_pickle("out/views.pkl"); BT = pd.read_pickle("out/backtest.pkl"); FB = pd.read_pickle("out/final_bt.pkl"); FD = pd.read_pickle("out/final_df.pkl")
band = pd.read_pickle("out/band.pkl"); hold = json.load(open("out/D4_holdout_forecast_LOCKED.json"))
BLUE = Font(name="Arial", size=10, color="0000FF"); BLK = Font(name="Arial", size=10); BOLD = Font(name="Arial", size=10, bold=True)
GRN = Font(name="Arial", size=10, color="008000"); HDR = Font(name="Arial", size=10, bold=True, color="FFFFFF"); SM = Font(name="Arial", size=9, color="52514E")
HF = PatternFill("solid", fgColor="1F3A5F"); YEL = PatternFill("solid", fgColor="FFFF00"); TILE = PatternFill("solid", fgColor="EEF2F7")
wb = Workbook()
def sh(n, w):
    ws = wb.create_sheet(n)
    for i, x in enumerate(w, 1): ws.column_dimensions[get_column_letter(i)].width = x
    return ws
def hdr(ws, r, vals, c0=1):
    for j, v in enumerate(vals, c0):
        c = ws.cell(r, j, v); c.font = HDR; c.fill = HF; c.alignment = Alignment(wrap_text=True, vertical="top")
def put(ws, ref, v, f=BLK, fmt=None, fill=None, wrap=False):
    c = ws[ref]; c.value = v; c.font = f
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap: c.alignment = Alignment(wrap_text=True, vertical="top")
    return c
def df_to(ws, df, r0, c0=1, fmts=None):
    hdr(ws, r0, list(df.columns), c0)
    for i, row in enumerate(df.itertuples(index=False), r0 + 1):
        for j, v in enumerate(row, c0):
            if isinstance(v, (np.floating, float)) and np.isnan(v): v = None
            elif hasattr(v, "item"): v = v.item()
            if isinstance(v, pd.Timestamp): v = v.to_pydatetime()
            c = ws.cell(i, j, v); c.font = BLK
            if fmts and df.columns[j - c0] in fmts: c.number_format = fmts[df.columns[j - c0]]
    return r0 + len(df)
T = lambda ws, t, s="": (put(ws, "A1", t, Font(name="Arial", size=13, bold=True, color="1F3A5F")), put(ws, "A2", s, Font(name="Arial", size=9, italic=True, color="52514E")))
# README
ws = wb.active; ws.title = "README"; ws.column_dimensions["A"].width = 22; ws.column_dimensions["B"].width = 110
for i, (a, b) in enumerate([("D4 PIPELINE & FORECAST DASHBOARD", ""), ("Company", "Strata Sense is fictional; all data synthetic (MBA capstone)."),
    ("How to use", "Dashboard: pick a dimension and fiscal year in the yellow cells; the performance table and chart update. Blue = input; black = formula."),
    ("Sheets", "Dashboard · Coverage · Backtest · Holdout · Perf_data · Hygiene · Scenarios · Governance"),
    ("Sources", "DR1 CRM (cleaned in D1), pipeline snapshots (12 quarter starts + the 1 Apr 2026 hold-out), DR1 forecast history, DR3 bookings. Code: d4_prep.py, d4_methods.py, d4_final.py, d4_views.py."),
    ("Hold-out", f"Q1 FY27 forecast locked before any outcome was seen: p10 ₹{hold['p10_cr']} cr, p50 ₹{hold['p50_cr']} cr, p90 ₹{hold['p90_cr']} cr (SHA-256 {hold['sha256'][:16]}…).")], 1):
    ws.cell(i, 1, a).font = BOLD if i == 1 else BLK; ws.cell(i, 2, b).font = BLK; ws.cell(i, 2).alignment = Alignment(wrap_text=True)
# Perf_data (long)
pdx = sh("Perf_data", [22, 30, 7, 10, 10, 12, 12, 14, 44]); T(pdx, "Performance data (qualified closed deals, FY24–FY26)", "Long table feeding the Dashboard selector")
perf = V["perf"][["dimension", "value", "fy", "qualified_deals", "win_rate", "avg_won_deal_lakh", "avg_cycle_days", "velocity_lakh_per_day", "key"]]
end = df_to(pdx, perf, 4, fmts={"win_rate": "0.0%", "avg_won_deal_lakh": "0.0", "avg_cycle_days": "0", "velocity_lakh_per_day": "0.00"})
lists = sh("Lists", [26, 30]); lists.sheet_state = "hidden"
dimsl = list(perf.dimension.unique())
for i, d in enumerate(dimsl, 1): lists.cell(i, 1, d)
vals = {d: list(perf[perf.dimension == d].value.unique()) for d in dimsl}
# Dashboard
Db = sh("Dashboard", [30, 14, 14, 14, 14, 14, 14, 14, 14]); T(Db, "Pipeline & forecast dashboard", "Strata Sense (fictional) · as of 1 Apr 2026 · ₹ crore unless marked")
tiles = [("FY26 bookings (clean)", "=SUM(Coverage!G12:G15)", "0.0"), ("FY26 win rate", 0.169, "0.0%"), ("Reported coverage Q1 FY27", "=Coverage!E16", "0.0x"),
         ("Required coverage Q1 FY27", "=Coverage!H16", "0.0x"), ("FY26 commit miss (MAPE)", "=Backtest!C24", "0%"), ("Hold-out p50 (locked)", "=Holdout!B6", "0.00")]
for k, (lab, f, fmt) in enumerate(tiles):
    col = get_column_letter(1 + k if k == 0 else 1 + k)
    r = 4; c = 1 + k
    Db.cell(r, c, lab).font = SM; Db.cell(r, c).fill = TILE; Db.cell(r, c).alignment = Alignment(wrap_text=True)
    x = Db.cell(r + 1, c, f); x.font = Font(name="Arial", size=16, bold=True, color="1F3A5F"); x.number_format = fmt; x.fill = TILE
Db.row_dimensions[4].height = 28
put(Db, "A8", "PERFORMANCE VIEW", BOLD)
put(Db, "A9", "Dimension"); put(Db, "B9", "Rep tenure", BLUE, fill=YEL)
put(Db, "A10", "Fiscal year"); put(Db, "B10", "FY26", BLUE, fill=YEL)
dv1 = DataValidation(type="list", formula1=f"=Lists!$A$1:$A${len(dimsl)}"); dv2 = DataValidation(type="list", formula1='"FY24,FY25,FY26"')
Db.add_data_validation(dv1); Db.add_data_validation(dv2); dv1.add("B9"); dv2.add("B10")
hdr(Db, 12, ["Value", "Qualified deals", "Win rate", "Avg won deal (lakh)", "Avg cycle (days)", "Velocity (lakh/day)"])
# value list per dimension placed in Lists col B.. (one column per dimension)
for j, d in enumerate(dimsl):
    lists.cell(1, 3 + j, d)
    for i, v in enumerate(vals[d], 2): lists.cell(i, 3 + j, v)
for i in range(8):
    r = 13 + i
    colref = f'INDEX(Lists!$C${2+i}:$Z${2+i},MATCH($B$9,Lists!$C$1:$Z$1,0))'
    Db.cell(r, 1, f'=IFERROR(IF({colref}=0,"",{colref}),"")')
    for j, fld in enumerate(["D", "E", "F", "G", "H"], 2):
        Db.cell(r, j, f'=IFERROR(INDEX(Perf_data!${fld}$5:${fld}${end},MATCH($B$9&"|"&$A{r}&"|"&$B$10,Perf_data!$I$5:$I${end},0)),"")')
    Db.cell(r, 3).number_format = "0.0%"; Db.cell(r, 4).number_format = "0.0"; Db.cell(r, 5).number_format = "0"; Db.cell(r, 6).number_format = "0.00"
ch = BarChart(); ch.type = "bar"; ch.title = "Win rate by selected dimension"; ch.style = 10; ch.height = 7; ch.width = 16
ch.add_data(Reference(Db, min_col=3, min_row=12, max_row=20), titles_from_data=True); ch.set_categories(Reference(Db, min_col=1, min_row=13, max_row=20))
ch.y_axis.numFmt = "0%"; ch.legend = None; Db.add_chart(ch, "H8")
# Coverage sheet
Cv = sh("Coverage", [11, 10, 12, 12, 12, 12, 12, 12, 12]); T(Cv, "Required vs reported coverage by quarter", "Required = 1 ÷ trailing-4-quarter in-quarter conversion of reported pipeline")
cov = V["cov"][["quarter", "quota_cr", "reported_pipeline_in_quarter_cr", "commit_call_m1_cr", "coverage_reported", "inq_conversion", "actual_clean_cr", "coverage_required", "attainment"]]
df_to(Cv, cov, 3, fmts={c: "0.00" for c in cov.columns[1:]} | {"inq_conversion": "0%", "attainment": "0%", "coverage_reported": "0.0x", "coverage_required": "0.0x"})
lc = LineChart(); lc.title = "Coverage: reported vs required (× quarterly quota)"; lc.height = 8; lc.width = 18
lc.add_data(Reference(Cv, min_col=5, min_row=3, max_row=16), titles_from_data=True); lc.add_data(Reference(Cv, min_col=8, min_row=3, max_row=16), titles_from_data=True)
lc.set_categories(Reference(Cv, min_col=1, min_row=4, max_row=16)); lc.y_axis.numFmt = "0.0"; Cv.add_chart(lc, "A19")
import copy
lcb = LineChart(); lcb.title = lc.title; lcb.height = 8; lcb.width = 16
lcb.add_data(Reference(Cv, min_col=5, min_row=3, max_row=16), titles_from_data=True); lcb.add_data(Reference(Cv, min_col=8, min_row=3, max_row=16), titles_from_data=True)
lcb.set_categories(Reference(Cv, min_col=1, min_row=4, max_row=16)); Db.add_chart(lcb, "A23")
# Backtest
Bt = sh("Backtest", [12, 11, 11, 11, 11, 11, 11, 11, 11, 11]); T(Bt, "Back-test: 8 quarters, no look-ahead", "Each quarter forecast only from snapshots and outcomes known before it began. Rolling 4-quarter training window.")
b4 = BT["rolling4"][0].copy(); b4["final"] = FB.final_p50.values; b4["final_p10"] = FB.p10.values; b4["final_p90"] = FB.p90.values
tab = b4[["quarter", "actual", "commit", "stage_weighted", "cohort_age", "simulation", "ensemble", "final", "final_p10", "final_p90"]]
df_to(Bt, tab, 4, fmts={c: "0.00" for c in tab.columns[1:]})
hdr(Bt, 14, ["Method", "Quarters", "MAPE", "Bias (mean error)", "MAPE last 4", "Max miss"])
meths = [("Rep commit (baseline)", "C"), ("Stage-weighted", "D"), ("Cohort-age conversion", "E"), ("Logistic simulation", "F"), ("Ensemble of 3", "G"), ("Final: stage-weighted, calibrated", "H")]
for k, (nm, col) in enumerate(meths):
    r = 15 + k; Bt.cell(r, 1, nm).font = BOLD if "Final" in nm else BLK; Bt.cell(r, 2, 8)
    Bt.cell(r, 3, f"=SUMPRODUCT(ABS({col}5:{col}12-$B$5:$B$12)/$B$5:$B$12)/8").number_format = "0.0%"
    Bt.cell(r, 4, f"=SUMPRODUCT(({col}5:{col}12-$B$5:$B$12)/$B$5:$B$12)/8").number_format = "+0.0%;-0.0%"
    Bt.cell(r, 5, f"=SUMPRODUCT(ABS({col}9:{col}12-$B$9:$B$12)/$B$9:$B$12)/4").number_format = "0.0%"
    Bt.cell(r, 6, f"=SUMPRODUCT(MAX(ABS({col}5:{col}12-$B$5:$B$12)/$B$5:$B$12))").number_format = "0.0%"
Bt.cell(22, 1, "p10–p90 coverage of final band").font = BLK; Bt.cell(22, 3, f"=SUMPRODUCT((B5:B12>=I5:I12)*(B5:B12<=J5:J12))/8").number_format = "0%"
Bt.cell(24, 1, "FY26 rep commit MAPE").font = BLK; Bt.cell(24, 3, "=SUMPRODUCT(ABS(C9:C12-B9:B12)/B9:B12)/4").number_format = "0%"
Bt.cell(26, 1, "Note: the calibration step (multiply by the median actual÷forecast ratio of the previous 4 quarters) was chosen on this back-test, so its 15.6% error is slightly optimistic. The hold-out quarter is the honest test.").font = SM
lc2 = LineChart(); lc2.title = "Actual vs forecasts (₹ cr)"; lc2.height = 8; lc2.width = 18
for col in (2, 3, 4, 8): lc2.add_data(Reference(Bt, min_col=col, min_row=4, max_row=12), titles_from_data=True)
lc2.set_categories(Reference(Bt, min_col=1, min_row=5, max_row=12)); Bt.add_chart(lc2, "H14")
lc3 = LineChart(); lc3.title = lc2.title; lc3.height = 8; lc3.width = 16
for col in (2, 3, 4, 8): lc3.add_data(Reference(Bt, min_col=col, min_row=4, max_row=12), titles_from_data=True)
lc3.set_categories(Reference(Bt, min_col=1, min_row=5, max_row=12)); Db.add_chart(lc3, "H23")
# Holdout
Ho = sh("Holdout", [44, 14, 14, 60]); T(Ho, "Q1 FY27 hold-out forecast (LOCKED)", f"Locked {hold['locked_at']} · SHA-256 {hold['sha256']}")
put(Ho, "A4", "Method"); put(Ho, "B4", hold["method"], wrap=False)
for i, (lab, key) in enumerate([("p10 (₹ cr)", "p10_cr"), ("p50 (₹ cr)", "p50_cr"), ("p90 (₹ cr)", "p90_cr")]):
    put(Ho, f"A{5+i}", lab, BOLD); put(Ho, f"B{5+i}", hold[key], Font(name="Arial", size=12, bold=True, color="1F3A5F"), "0.00")
put(Ho, "A9", "Raw stage-weighted (₹ cr)"); put(Ho, "B9", hold["raw_stage_weighted_cr"], BLK, "0.00")
put(Ho, "A10", "Calibration factor (median actual ÷ forecast, last 4 quarters)"); put(Ho, "B10", hold["calibration_factor"], BLK, "0.000")
put(Ho, "A12", "Cross-checks", BOLD)
cc = hold["cross_checks"]
for i, (lab, v) in enumerate([("Cohort-age method", cc["cohort_age_cr"]), ("Logistic simulation (expected)", cc["simulation_expected_cr"]), ("Simulation p10", cc["simulation_p10_p90"][0]), ("Simulation p90", cc["simulation_p10_p90"][1]), ("Rep commit, month 1", cc["rep_commit_m1_cr"]), ("Quarterly quota", 17.15)]):
    put(Ho, f"A{13+i}", lab); put(Ho, f"B{13+i}", v, BLK, "0.00")
put(Ho, "A20", "Why the forecast is below the rep commit", BOLD)
put(Ho, "A21", "Conversion of open pipeline has fallen every year; uncalibrated methods over-forecast by 16–35% in the back-test. The calibration factor corrects that bias using only past quarters. 57% of snapshot value carries at least one hygiene flag (Hygiene sheet).", wrap=True)
Ho.merge_cells("A21:D23"); Ho.row_dimensions[21].height = 30
fl = V["flags"]; st = fl.groupby(["stage", "forecast_category"]).val_cr.sum().unstack(fill_value=0).round(2).reset_index()
df_to(Ho, st, 26, fmts={c: "0.00" for c in st.columns[1:]})
put(Ho, "A25", "Snapshot 1 Apr 2026: value by stage and forecast category (₹ cr)", BOLD)
# Hygiene
Hy = sh("Hygiene", [30, 16, 60, 16, 14]); T(Hy, "Pipeline hygiene rules", "Stage exit criteria, ageing limits, slippage and single-thread flags; applied to the 1 Apr 2026 snapshot")
hdr(Hy, 4, ["Stage", "Ageing limit (days)", "Exit criteria (to move to next stage)", "Median days (won FY25–26)", "75th pct days"])
exitc = {"1-Qualify": "Pain and asset scope confirmed; economic buyer named; budget route known", "2-Solution Design": "≥3 contacts incl. finance or procurement; security requirements captured; success criteria drafted",
         "3-Proof of Value": "Paid pilot signed with written success criteria and conversion price", "4-Proposal": "Quantified business case using buyer numbers; finance contact engaged; mutual action plan agreed",
         "5-Negotiation & Procurement": "Paper process mapped; legal/security cleared; signature date confirmed by economic buyer"}
sa = V["stage_age"]
for k, (stg, r_) in enumerate(sa.iterrows()):
    r = 5 + k; put(Hy, f"A{r}", stg); put(Hy, f"B{r}", int(r_.limit_days), BLUE, "0"); put(Hy, f"C{r}", exitc[stg], wrap=True); put(Hy, f"D{r}", r_["50%"], BLK, "0"); put(Hy, f"E{r}", r_["75%"], BLK, "0")
hdr(Hy, 11, ["Flag", "Rule", "", "Deals flagged", "Value (₹ cr)"])
rules = [("f_stale_date", "Expected close date already past"), ("f_slipped2", "Close date pushed 2+ times"), ("f_aged", "Longer in stage than the ageing limit"),
         ("f_single_thread", "Stage 3+ with only one buyer contact"), ("f_no_activity_90d", "No activity for 90 days"), ("f_commit_not_stage5", "In Commit but not at stage 5"), ("any_flag", "Any flag")]
fs = V["flag_summary"]
for k, (f, rl) in enumerate(rules):
    r = 12 + k; put(Hy, f"A{r}", f.replace("f_", "")); put(Hy, f"B{r}", rl); put(Hy, f"D{r}", int(fs.loc[f, "deals"]), BLK, "0"); put(Hy, f"E{r}", float(fs.loc[f, "value_cr"]), BLK, "0.0")
put(Hy, "A20", "Snapshot value (₹ cr)"); put(Hy, "E20", float(fl.val_cr.sum()), BLK, "0.0")
put(Hy, "A21", "Share of value with any flag"); put(Hy, "E21", "=E18/E20", BOLD, "0%")
put(Hy, "A22", "In-quarter pipeline, all / clean (no flags) (₹ cr)"); put(Hy, "D22", float(fl[fl.inq].val_cr.sum()), BLK, "0.0"); put(Hy, "E22", float(fl[fl.inq & ~fl.any_flag].val_cr.sum()), BLK, "0.0")
put(Hy, "A23", "Clean in-quarter coverage (× quota ₹17.15 cr)"); put(Hy, "E23", "=E22/17.15", BOLD, "0.0x")
fx = fl[fl.any_flag].sort_values("val_cr", ascending=False)[["opp_id", "stage", "forecast_category", "val_cr", "expected_close_date", "pushes", "days_in_stage", "contacts", "owner_ae_id"] + [c for c in fl.columns if c.startswith("f_")]].head(60)
put(Hy, "A25", "Top 60 flagged deals by value (for Monday inspection)", BOLD); df_to(Hy, fx, 26, fmts={"val_cr": "0.00"})
# Scenarios
Sc = sh("Scenarios", [44, 12, 12, 12, 12, 12, 12, 12, 12, 12, 50]); T(Sc, "FY27–FY29 scenarios (linked to D2 and D3 assumptions)", "Blue inputs; ending ARR = opening × NRR + new-logo ARR. D7 replaces this with the full integrated model.")
put(Sc, "A4", "Scenario selector"); put(Sc, "B4", "Base", BLUE, fill=YEL)
dv3 = DataValidation(type="list", formula1='"Base,Downside,Aggressive"'); Sc.add_data_validation(dv3); dv3.add("B4")
hdr(Sc, 6, ["Driver", "Base FY27", "Base FY28", "Base FY29", "Down FY27", "Down FY28", "Down FY29", "Aggr FY27", "Aggr FY28", "Aggr FY29", "Source / link"])
drv = [("Win rate on qualified deals", [0.218, 0.23, 0.235], [0.17, 0.175, 0.18], [0.23, 0.25, 0.26], "0.0%", "D1 FY26 16.9%; D2 plan mix implies 21.8% (63.5 won ÷ 291 qualified); board goal 23% by FY28"),
       ("Qualified opportunities (direct)", [291, 330, 350], [291, 300, 310], [300, 360, 420], "0", "D2 funnel (291 for FY27); FY28–29 volumes need the capacity D7 must fund"),
       ("Average won deal (₹ lakh)", [66.9, 70, 73], [60, 61, 62], [68, 72, 76], "0.0", "D2 plan mix (₹42.5 cr ÷ 63.5 deals)"),
       ("Partner-sourced new-logo ARR (₹ cr)", [4.0, 9.0, 18.0], [2.6, 4.0, 6.0], [4.5, 11.0, 22.0], "0.0", "D2 SEA plan; D6 builds the channel"),
       ("Net revenue retention", [1.00, 1.04, 1.07], [0.97, 0.99, 1.01], [1.01, 1.05, 1.08], "0.0%", "D1 FY26 98.9%; Inject 1 retention squad; board 108% by FY29")]
for k, (lab, b, d, a, fmt, src) in enumerate(drv):
    r = 7 + k; put(Sc, f"A{r}", lab)
    for j, v in enumerate(b + d + a): put(Sc, f"{get_column_letter(2+j)}{r}", v, BLUE, fmt)
    put(Sc, f"K{r}", src, SM)
put(Sc, "A13", "Direct new-logo ARR (₹ cr) = opps × win × deal")
put(Sc, "A14", "Total new-logo ARR (₹ cr)"); put(Sc, "A15", "Opening ARR (₹ cr)"); put(Sc, "A16", "Ending ARR (₹ cr)", BOLD); put(Sc, "A17", "ARR growth"); put(Sc, "A18", "Board path ending ARR (₹ cr)"); put(Sc, "A19", "Gap to board path (₹ cr)", BOLD)
for j in range(9):
    c = get_column_letter(2 + j); first = j % 3 == 0
    put(Sc, f"{c}13", f"={c}8*{c}7*{c}9/100", BLK, "0.0"); put(Sc, f"{c}14", f"={c}13+{c}10", BLK, "0.0")
    put(Sc, f"{c}15", 310 if first else f"={get_column_letter(1+j)}16", BLUE if first else BLK, "0.0")
    put(Sc, f"{c}16", f"={c}15*{c}11+{c}14", BOLD, "0.0"); put(Sc, f"{c}17", f"={c}16/{c}15-1", BLK, "0.0%")
    put(Sc, f"{c}18", [356.5, 427.8, 521.9][j % 3], BLUE, "0.0"); put(Sc, f"{c}19", f"={c}16-{c}18", BOLD, "0.0;(0.0)")
put(Sc, "A21", "Selected scenario, FY29 ending ARR (₹ cr)", BOLD); put(Sc, "B21", '=IF(B4="Base",D16,IF(B4="Downside",G16,J16))', BOLD, "0.0")
put(Sc, "A22", "Selected scenario, FY29 gap to ₹521.9 cr", BOLD); put(Sc, "B22", '=B21-521.9', BOLD, "0.0;(0.0)")
# Governance
G = sh("Governance", [26, 90]); T(G, "Forecast governance", "Categories, weekly routine, deal inspection checklist and role views")
gov = [("FORECAST CATEGORIES", ""), ("Commit", "Stage 5; economic buyer has confirmed the signature date; paper process mapped; ≥3 contacts; close date inside the quarter and never pushed more than once. Target conversion ≥70%."),
       ("Best case", "Stage 4 with a quantified business case and a mutual action plan; close date inside the quarter."), ("Pipeline", "Qualified (stage 2+) with a close date inside the quarter that does not meet Best-case rules."),
       ("Omitted", "Any hygiene flag unresolved for 2 weeks, or stage 1. Excluded from coverage and forecast."),
       ("WEEKLY ROUTINE", ""), ("Monday 10:00", "Reps update stage, close date, next step and contacts; hygiene flags auto-generated (Hygiene sheet)."),
       ("Tuesday", "Manager 1:1 deal inspection on every Commit and Best-case deal using the checklist; flags resolved or deals moved to Omitted."),
       ("Wednesday", "CRO forecast call: model p50 and p10–p90 vs manager call vs rep commit; explain any gap > 10%."),
       ("Thursday", "CFO view: forecast range, clean coverage vs required, top-10 deals; one number submitted to finance."),
       ("DEAL INSPECTION CHECKLIST", ""), ("1", "Who is the economic buyer and when did we last meet them?"), ("2", "Which buyer-supplied number is in the business case?"),
       ("3", "How many contacts, and are finance, procurement and IT security among them?"), ("4", "What is the paper process, step by step, with dates?"),
       ("5", "What happens if the buyer does nothing? What is the compelling event?"), ("6", "Which competitor is present and what is our counter?"), ("7", "Has the close date moved? Why?"),
       ("ROLE VIEWS", ""), ("Rep", "Own deals with flags, next steps, contacts gap; personal commit vs model."), ("Manager", "Team Commit/Best case, flag list, conversion vs plan, deals to inspect."),
       ("CRO", "Model p50 and range vs manager calls; coverage required vs reported by region; win rate by tier and competitor."), ("CFO", "One forecast number with range; bias history; clean coverage; bookings vs plan.")]
for i, (a, b) in enumerate(gov, 4):
    G.cell(i, 1, a).font = BOLD if a.isupper() else BLK; G.cell(i, 2, b).font = BLK; G.cell(i, 2).alignment = Alignment(wrap_text=True, vertical="top")
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if c.font and c.font.name != "Arial": c.font = BLK
wb.save("out/D4_Forecast_Dashboard.xlsx"); print(wb.sheetnames)
