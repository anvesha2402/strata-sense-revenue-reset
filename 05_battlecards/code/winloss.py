import pandas as pd, numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
q = pd.read_pickle("/home/claude/strata/d1/out/q_scored.pkl"); f = q[q.fy >= 2025].copy(); vob = pd.read_pickle("dr/vob.pkl")
CODES = ["BUNDLE-LOCKIN", "PLC-COVERAGE-GAP", "INTEGRATOR-ARCH", "SENSOR-REUSE", "PRICE-ONLY", "SINGLE-THREAD/NO-EB", "NO-BUYER-NUMBERS", "BUDGET/DEFERRAL", "IT-SECURITY", "WIN-COMPLEMENT", "WIN-BUYER-NUMBERS", "WIN-PILOT-CRITERIA", "WIN-MULTI-THREAD", "WIN-PARTNER", "WIN-DIAGNOSTIC-DEPTH"]
code = {"VOB-01": ["BUNDLE-LOCKIN", "IT-SECURITY"], "VOB-02": ["BUNDLE-LOCKIN", "SINGLE-THREAD/NO-EB"], "VOB-03": ["BUNDLE-LOCKIN", "PLC-COVERAGE-GAP", "SINGLE-THREAD/NO-EB"],
 "VOB-04": ["BUNDLE-LOCKIN"], "VOB-05": ["INTEGRATOR-ARCH"], "VOB-06": ["SINGLE-THREAD/NO-EB", "BUNDLE-LOCKIN"], "VOB-07": ["SENSOR-REUSE", "SINGLE-THREAD/NO-EB", "NO-BUYER-NUMBERS"],
 "VOB-08": ["SENSOR-REUSE"], "VOB-09": ["PRICE-ONLY", "SINGLE-THREAD/NO-EB"], "VOB-10": ["SENSOR-REUSE", "NO-BUYER-NUMBERS"], "VOB-11": ["PRICE-ONLY"], "VOB-12": ["PRICE-ONLY"],
 "VOB-13": ["BUDGET/DEFERRAL", "SINGLE-THREAD/NO-EB", "NO-BUYER-NUMBERS"], "VOB-14": ["BUDGET/DEFERRAL", "SINGLE-THREAD/NO-EB"], "VOB-15": ["BUDGET/DEFERRAL"], "VOB-16": ["NO-BUYER-NUMBERS"],
 "VOB-17": ["WIN-DIAGNOSTIC-DEPTH", "WIN-PILOT-CRITERIA", "WIN-MULTI-THREAD"], "VOB-18": ["WIN-BUYER-NUMBERS"], "VOB-19": ["WIN-COMPLEMENT", "PLC-COVERAGE-GAP"], "VOB-20": ["WIN-COMPLEMENT", "PLC-COVERAGE-GAP"],
 "VOB-21": ["WIN-DIAGNOSTIC-DEPTH", "WIN-MULTI-THREAD"], "VOB-22": ["WIN-PARTNER", "WIN-BUYER-NUMBERS", "WIN-MULTI-THREAD"], "VOB-23": ["WIN-BUYER-NUMBERS", "WIN-PILOT-CRITERIA"], "VOB-24": ["WIN-MULTI-THREAD", "IT-SECURITY"]}
rival = {"VOB-01": "Helix", "VOB-02": "Helix", "VOB-03": "Helix", "VOB-04": "Helix", "VOB-05": "Helix", "VOB-06": "Helix", "VOB-07": "TrueSense", "VOB-08": "TrueSense", "VOB-09": "TrueSense", "VOB-10": "TrueSense",
 "VOB-11": "BMI", "VOB-12": "BMI", "VOB-13": "No decision", "VOB-14": "No decision", "VOB-15": "No decision", "VOB-16": "No decision", "VOB-17": "TrueSense", "VOB-18": "TrueSense", "VOB-19": "Helix", "VOB-20": "Helix",
 "VOB-21": "BMI", "VOB-22": "None", "VOB-23": "None", "VOB-24": "TrueSense"}
vob["rival_context"] = vob.interview_id.map(rival)
for c in CODES: vob[c] = vob.interview_id.map(lambda i: 1 if c in code[i] else 0)
BLUE = Font(name="Arial", size=10, color="0000FF"); BLK = Font(name="Arial", size=10); BOLD = Font(name="Arial", size=10, bold=True); HDR = Font(name="Arial", size=10, bold=True, color="FFFFFF")
HF = PatternFill("solid", fgColor="1F3A5F"); YEL = PatternFill("solid", fgColor="FFFF00"); SM = Font(name="Arial", size=9, color="52514E")
wb = Workbook(); ws = wb.active; ws.title = "README"; ws.column_dimensions["A"].width = 24; ws.column_dimensions["B"].width = 110
for i, (a, b) in enumerate([("D5 WIN/LOSS ANALYSIS", ""), ("Company", "Strata Sense is fictional; data synthetic (MBA capstone)."),
    ("Sources", "DR1 CRM (cleaned in D1), qualified closed deals FY25–FY26; DR4 voice of buyer (24 interviews, 12 rep notes)."),
    ("Sheets", "VOB_coding · DR1_loss_reasons · Rival_evidence · Uplift_model (formulas; blue inputs) · Discount_limits · Inject2"),
    ("Caution", "The CRM competitor field is filled mostly after a loss (blank on 51% of wins, 30% of losses), so win rates 'against' a rival are biased low. Compare within rivals (strong vs weak selling), not across.")], 1):
    ws.cell(i, 1, a).font = BOLD if i == 1 else BLK; ws.cell(i, 2, b).font = BLK; ws.cell(i, 2).alignment = Alignment(wrap_text=True)
def hdr(ws, r, vals):
    for j, v in enumerate(vals, 1):
        c = ws.cell(r, j, v); c.font = HDR; c.fill = HF; c.alignment = Alignment(wrap_text=True, vertical="top")
# VOB coding
V = wb.create_sheet("VOB_coding"); cols = ["interview_id", "opp_id", "outcome", "rival_context", "interviewee_role"] + CODES
hdr(V, 1, cols)
for i, r in enumerate(vob[cols].itertuples(index=False), 2):
    for j, v in enumerate(r, 1): V.cell(i, j, v).font = BLK
n = len(vob) + 1
V.cell(n + 2, 1, "Count (losses)").font = BOLD; V.cell(n + 3, 1, "Count (wins)").font = BOLD
for j in range(6, 6 + len(CODES)):
    L = get_column_letter(j)
    V.cell(n + 2, j, f'=SUMIFS({L}2:{L}{n},$C$2:$C${n},"Lost")').font = BOLD; V.cell(n + 3, j, f'=SUMIFS({L}2:{L}{n},$C$2:$C${n},"Won")').font = BOLD
for i in range(1, 6 + len(CODES)): V.column_dimensions[get_column_letter(i)].width = 12 if i > 5 else 16
V.freeze_panes = "F2"
# DR1 loss reasons
Lr = wb.create_sheet("DR1_loss_reasons"); l = f[f.won == 0]
t = pd.crosstab(l.loss_reason.fillna("(blank)"), l.comp_group.replace({"None identified": "None / blank", "Unknown": "None / blank"}))
hdr(Lr, 1, ["Loss reason (FY25–26 qualified losses)"] + list(t.columns) + ["Total"])
for i, (idx, row) in enumerate(t.iterrows(), 2):
    Lr.cell(i, 1, idx).font = BLK
    for j, v in enumerate(row, 2): Lr.cell(i, j, int(v)).font = BLK
    Lr.cell(i, len(t.columns) + 2, f"=SUM(B{i}:{get_column_letter(len(t.columns)+1)}{i})").font = BOLD
Lr.column_dimensions["A"].width = 46
for j in range(2, len(t.columns) + 3): Lr.column_dimensions[get_column_letter(j)].width = 16
# Rival evidence
p = f[f.reached >= 4].copy(); p["strong"] = (p.business_case_attached == "Y") & (p.threading != "1 contact")
Re = wb.create_sheet("Rival_evidence"); hdr(Re, 1, ["Metric (FY25–26 unless stated)", "Helix", "TrueSense", "BMI", "Source"])
def wr(df): return round(df.won.mean(), 3) if len(df) else None
rows = [
 ("Share of FY26 qualified deals with rival recorded", 0.241, 0.222, 0.088, "DR1 clean"),
 ("Proposals: win rate with strong selling (BC + multi-threaded)", wr(p[(p.comp_group == "Helix Automation") & p.strong]), wr(p[(p.comp_group == "TrueSense AI") & p.strong]), wr(p[(p.comp_group == "Bharat Machine Intelligence") & p.strong]), "DR1 clean"),
 ("Proposals: win rate without strong selling", wr(p[(p.comp_group == "Helix Automation") & ~p.strong]), wr(p[(p.comp_group == "TrueSense AI") & ~p.strong]), wr(p[(p.comp_group == "Bharat Machine Intelligence") & ~p.strong]), "DR1 clean"),
 ("Proposals: n strong / n total", f"{int(p[(p.comp_group=='Helix Automation')&p.strong].shape[0])} / {int(p[p.comp_group=='Helix Automation'].shape[0])}", f"{int(p[(p.comp_group=='TrueSense AI')&p.strong].shape[0])} / {int(p[p.comp_group=='TrueSense AI'].shape[0])}", f"{int(p[(p.comp_group=='Bharat Machine Intelligence')&p.strong].shape[0])} / {int(p[p.comp_group=='Bharat Machine Intelligence'].shape[0])}", "Small samples"),
 ("Average discount on won proposals", round(p[(p.comp_group == "Helix Automation") & (p.won == 1)].discount_pct.mean(), 1), round(p[(p.comp_group == "TrueSense AI") & (p.won == 1)].discount_pct.mean(), 1), round(p[(p.comp_group == "Bharat Machine Intelligence") & (p.won == 1)].discount_pct.mean(), 1), "DR1 clean"),
 ("Average discount on lost proposals", round(p[(p.comp_group == "Helix Automation") & (p.won == 0)].discount_pct.mean(), 1), round(p[(p.comp_group == "TrueSense AI") & (p.won == 0)].discount_pct.mean(), 1), round(p[(p.comp_group == "Bharat Machine Intelligence") & (p.won == 0)].discount_pct.mean(), 1), "Discount did not separate wins from losses"),
 ("Win rate in Helix-incumbent accounts FY24 → FY26", "20.1% → 7.0%", "", "", "D1"),
 ("Top loss reason (coded, DR1)", "Bundled offer / existing vendor", "Existing sensors reused; price", "Price", "DR1 loss_reason"),
 ("Top loss theme (DR4 interviews)", "Bundle lock-in (5 of 6 losses)", "Sensor reuse (3 of 4 losses)", "Price only (2 of 2)", "DR4 coded"),
 ("Top win theme (DR4 interviews)", "Complement uncovered assets (2 of 2 wins)", "Diagnostic depth; pilot criteria; multi-threading", "Diagnostic depth; CFO in room", "DR4 coded"),
]
for i, r in enumerate(rows, 2):
    for j, v in enumerate(r, 1):
        c = Re.cell(i, j, v); c.font = BLK
        if isinstance(v, float) and v <= 1 and j in (2, 3, 4): c.number_format = "0.0%"
for j, w in enumerate([52, 26, 30, 22, 40], 1): Re.column_dimensions[get_column_letter(j)].width = w
# Uplift model
U = wb.create_sheet("Uplift_model"); hdr(U, 1, ["Rival", "Share of qualified deals (FY26)", "FY26 win rate in these deals (context)", "Lever", "Uplift (pts) before Inject 2", "Inject 2 effect (pts, FY27)", "FY27 uplift (pts)", "Contribution to overall win rate (pts)", "Overlap with D2 threading lift", "Incremental beyond D2 (pts)", "Assumption / evidence"])
up = [("Helix (incumbent accounts, named 40 only)", 0.10, 0.07, "Complement play on non-PLC assets; no head-on replacement; no discount matching", 3.0, -3.0, 0.0, "Helix-incumbent win 7% FY26; complement wins in DR4 (2 of 2); Inject 2 makes 'free' stronger until Mar 2027"),
      ("TrueSense", 0.222, 0.15, "Business case on buyer numbers + ≥3 contacts; sensor-data audit question; qualify out simple sites with good existing sensors", 5.0, 0.0, 0.6, "Strong selling 12% → 36% on TrueSense proposals (n=14 strong); half of the lift already in D2 threading"),
      ("BMI", 0.088, 0.10, "Qualify out price-only small sites (D2 stop-list); CFO risk case where critical assets exist", 2.0, 0.0, 0.5, "BMI losses coded 'price' (31 of 49 with a reason); stop-list reduces BMI volume"),
      ("No decision", 0.12, 0.00, "Compelling event, economic buyer by stage 2, paid pilot with written criteria", 1.5, 0.0, 0.5, "52 of 359 FY26 losses are no-decision; DR4: single-threaded and vendor numbers in 3 of 4")]
for i, (rv, sh_, w26, lev, u0, inj, ov, ev) in enumerate(up, 2):
    U.cell(i, 1, rv).font = BLK; U.cell(i, 2, sh_).font = BLUE; U.cell(i, 2).number_format = "0.0%"; U.cell(i, 3, w26).font = BLUE; U.cell(i, 3).number_format = "0.0%"
    U.cell(i, 4, lev).font = BLK; U.cell(i, 4).alignment = Alignment(wrap_text=True)
    c = U.cell(i, 5, u0); c.font = BLUE; c.fill = YEL; c = U.cell(i, 6, inj); c.font = BLUE; c.fill = YEL
    U.cell(i, 7, f"=E{i}+F{i}"); U.cell(i, 8, f"=B{i}*G{i}").number_format = "0.00"
    c = U.cell(i, 9, ov); c.font = BLUE; c.number_format = "0%"; U.cell(i, 10, f"=H{i}*(1-I{i})").number_format = "0.00"
    U.cell(i, 11, ev).font = SM; U.cell(i, 11).alignment = Alignment(wrap_text=True)
U.cell(7, 1, "Total (percentage points on overall win rate)").font = BOLD
U.cell(7, 8, "=SUM(H2:H5)").number_format = "0.00"; U.cell(7, 10, "=SUM(J2:J5)").number_format = "0.00"
for c in (U.cell(7, 8), U.cell(7, 10)): c.font = BOLD
U.cell(9, 1, "Reading: battlecards add about 1.5 points (before overlap) to the overall win rate in FY27, but most of it overlaps with the D2 multi-threading lift. Only about 0.6 points is new, and the Helix lever is cancelled in FY27 by Inject 2.").font = SM
for j, w in enumerate([34, 12, 12, 44, 12, 12, 11, 13, 12, 13, 50], 1): U.column_dimensions[get_column_letter(j)].width = w
for r in range(2, 6): U.row_dimensions[r].height = 42
# Discount limits
Dl = wb.create_sheet("Discount_limits"); hdr(Dl, 1, ["Situation", "Rep may give (max)", "Manager may approve (max)", "Must get in return", "Never"])
dl = [("Any deal (company rule)", "10%", "15%", "Give-get table: term, prepay, second site, reference", "Discount without a give; hardware below cost"),
      ("Against Helix bundle / 'free'", "0% to match free", "10% only for a 3-year term on complement scope", "Scope limited to non-PLC assets; integration pack; exec sponsor", "Match 'free'; bid for PLC-connected assets"),
      ("Against TrueSense", "5%", "12%", "Paid pilot with sensor-data audit; 3-year TCO in proposal", "Price-match their per-asset rate"),
      ("Against BMI", "0%", "5%", "CFO risk case on critical assets", "Chase price-only sites (qualify out)"),
      ("No-decision risk", "0%", "Pilot credit only", "Compelling event and economic buyer confirmed", "End-of-quarter discount to force a decision")]
for i, r in enumerate(dl, 2):
    for j, v in enumerate(r, 1): c = Dl.cell(i, j, v); c.font = BLK; c.alignment = Alignment(wrap_text=True, vertical="top")
for j, w in enumerate([30, 18, 26, 44, 40], 1): Dl.column_dimensions[get_column_letter(j)].width = w
Dl.cell(8, 1, "FY26 evidence: average discount on won and lost proposals was about the same against every rival (19–21%), so discount did not buy wins.").font = SM
# Inject 2
I2 = wb.create_sheet("Inject2"); hdr(I2, 1, ["Item", "Before (D5 v1.0)", "After Inject 2 (v1.1)", "Why"])
inj = [("Event", "Helix bundles HelixAsset free for 12 months with a 3-year MES renewal", "Helix makes HelixAsset free to ALL existing plant customers until 31 Mar 2027 (no renewal needed)", "Announcement, Week 5"),
       ("New-logo win rate, Helix-incumbent accounts (FY27)", "7% → 10% with complement play", "7% → 7% (lever cancelled); recover to ~10% in FY28 when 'free' ends", "Free removes the lock-in argument until Mar 2027"),
       ("Retention risk, Helix-incumbent customers", "NRR 92% (FY26)", "Treat ₹108.6 cr ARR as at-risk; renewals before Mar 2027 get exec sponsor + usage review 90 days ahead", "Customers may trial HelixAsset alongside us at zero cost"),
       ("Discount limit vs Helix", "Up to 10% for 3-year complement term", "Unchanged. No matching 'free'. New allowed trade: 3-month deferred start on complement scope, only with a 3-year term", "Keeps price integrity; gives buyers a reason not to wait"),
       ("Key talk track", "'Free for a year, then list price, with a 3-year lock-in'", "'Free until March. Then what? And what does it cover? Only machines wired to Helix PLCs.'", "Shift from lock-in to coverage and cost after March 2027"),
       ("Battlecard owner action", "—", "Urgent update published within 48 hours; 30-minute rep briefing; win/loss tagging 'HELIX-FREE' in CRM for 90 days", "Urgent-update rule test")]
for i, r in enumerate(inj, 2):
    for j, v in enumerate(r, 1): c = I2.cell(i, j, v); c.font = BLK; c.alignment = Alignment(wrap_text=True, vertical="top")
for j, w in enumerate([34, 40, 50, 40], 1): I2.column_dimensions[get_column_letter(j)].width = w
wb.save("out/D5_WinLoss_Analysis.xlsx"); vob.to_pickle("dr/vob_coded.pkl"); print("ok")
