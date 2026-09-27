"""D7 integrated revenue model: one workbook owns every number. Formula-driven; blue = input, yellow = key assumption."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
import sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "out/D7_Integrated_Model.xlsx"

BLUE = Font(name="Arial", size=10, color="0000FF"); BLK = Font(name="Arial", size=10); BOLD = Font(name="Arial", size=10, bold=True)
GRN = Font(name="Arial", size=10, color="008000"); HDR = Font(name="Arial", size=10, bold=True, color="FFFFFF")
HF = PatternFill("solid", fgColor="1F3A5F"); YEL = PatternFill("solid", fgColor="FFFF00"); SUB = PatternFill("solid", fgColor="E8EEF5")
SM = Font(name="Arial", size=9, color="52514E"); TT = Font(name="Arial", size=13, bold=True, color="1F3A5F")
CR = '#,##0.00;(#,##0.00);"-"'; C1 = '#,##0.0;(#,##0.0);"-"'; PCT = "0.0%"; N0 = "0"; N1 = "0.0"
wb = Workbook()

def sh(name, widths):
    ws = wb.create_sheet(name)
    for i, w in enumerate(widths, 1): ws.column_dimensions[L(i)].width = w
    ws.freeze_panes = "C5" if name not in ("README", "Traceability", "Checks") else None
    return ws
def put(ws, ref, v, f=BLK, fmt=None, fill=None, wrap=False):
    c = ws[ref]; c.value = v; c.font = f
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap: c.alignment = Alignment(wrap_text=True, vertical="top")
    return c
def hdr(ws, r, vals, c0=1):
    for j, v in enumerate(vals, c0):
        c = ws.cell(r, j, v); c.font = HDR; c.fill = HF; c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center" if j > c0 else "left")
def title(ws, t, s): put(ws, "A1", t, TT); put(ws, "A2", s, Font(name="Arial", size=9, italic=True, color="52514E"))

Q = [f"Q{k+1} FY{27+y}" for y in range(3) for k in range(4)]
QC = [L(3 + i) for i in range(12)]            # C..N quarterly
YC = ["O", "P", "Q"]                           # annual FY27..FY29
def yq(y): return QC[4 * y:4 * y + 4]
def qhdr(ws, r=4, first="Line", b="FY26 / start"): hdr(ws, r, [first, b] + Q + ["FY27", "FY28", "FY29", "Note / source"])
def ysum(ws, r, fmt=CR, f=BLK, kind="sum"):
    for y, c in enumerate(YC):
        a, z = yq(y)[0], yq(y)[3]
        if kind == "sum": put(ws, f"{c}{r}", f"=SUM({a}{r}:{z}{r})", f, fmt)
        elif kind == "end": put(ws, f"{c}{r}", f"={z}{r}", f, fmt)
        elif kind == "start": put(ws, f"{c}{r}", f"={a}{r}", f, fmt)
        elif kind == "avg": put(ws, f"{c}{r}", f"=AVERAGE({a}{r}:{z}{r})", f, fmt)
def note(ws, r, t): put(ws, f"R{r}", t, SM)

# ---------------------------------------------------------------- README
ws = wb.active; ws.title = "README"; ws.column_dimensions["A"].width = 24; ws.column_dimensions["B"].width = 120
readme = [("D7 INTEGRATED REVENUE MODEL, FY27–FY29", ""), ("Company", "Strata Sense Technologies is fictional; all data synthetic (MBA capstone). ₹ crore unless stated."),
    ("How to use", "Pick a scenario in Assumptions!C4 (Base, Downside, Aggressive, CFO-capped). Flex any driver with the five sensitivity shift cells (Assumptions rows 60–64). Every sheet recalculates; the Cascade sheet shows what moved against the saved base run."),
    ("Colour code", "Blue = input. Yellow fill = key assumption. Black = formula. Green = link to another sheet. No hard-coded plugs: every number in a calculation sheet is a formula or a labelled input."),
    ("Flow", "Assumptions → Capacity (AE cohorts, ramp, attrition) → Bookings (capacity × win rate × deal size; pipeline required) → Channel (partner ARR, channel P&L) → ARR_bridge (quarterly) → PnL (revenue, gross margin incl. partner margin, S&M, EBITDA, CAC payback) → Investment (FY27 envelope; payback vs do-nothing) → Checks."),
    ("Snapshot sheets", "Scenarios, Sensitivity and the 'Base (saved)' column of Cascade hold values produced by running this workbook with run_scenarios.py (script in the GitHub folder). They are labelled as saved runs; the live model is unaffected by them."),
    ("Counting rule", "A partner-sourced deal worked by an AE is counted once, as partner ARR (Channel sheet). The AE gets 50% quota credit (compensation only). Direct bookings exclude partner-sourced deals."),
    ("Q1 FY27", "Q1 FY27 total new-logo ARR is the locked D4 hold-out forecast (₹8.71 cr, p50), because the quarter was already under way when the plan was set. Capacity drives bookings from Q2 FY27."),
    ("Supersedes", "D2 capacity (₹46.5 cr need), D4 scenarios and D6 share denominators. D6 partner ARR is reproduced exactly in the Base scenario (Checks)."),
    ("Injects", "Inject 1 (₹15 cr envelope): Investment sheet. Inject 2 (HelixAsset free): win rate and churn assumptions (D5). Inject 3 (partner conflict): Channel existing-partner ARR. Inject 4 (Vajra re-tender): Inject4 sheet and ARR_bridge row 'Vajra re-tender'.")]
for i, (a, b) in enumerate(readme, 1):
    ws.cell(i, 1, a).font = TT if i == 1 else BOLD; ws.cell(i, 2, b).font = BLK; ws.cell(i, 2).alignment = Alignment(wrap_text=True, vertical="top")

# ---------------------------------------------------------------- ASSUMPTIONS
A = sh("Assumptions", [50, 11] + [9.5] * 15 + [60]); A.freeze_panes = "C9"
title(A, "Assumptions and scenario switch", "Scenario drivers by year; the Live columns (O–Q) feed the model. FY26 actual (column B) is the starting point for quarterly interpolation.")
put(A, "A4", "SCENARIO (choose)", BOLD); put(A, "C4", "Base", BLUE, fill=YEL); A.merge_cells("C4:D4")
SCN = ["Base", "Downside", "Aggressive", "CFO-capped"]
for j, s in enumerate(SCN): put(A, f"{L(20 + j)}4", s, SM)
dv = DataValidation(type="list", formula1='"Base,Downside,Aggressive,CFO-capped"', allow_blank=False); A.add_data_validation(dv); dv.add("C4")
put(A, "A5", "Scenario index"); put(A, "C5", "=MATCH(C4,T4:W4,0)", BOLD, N0)
put(A, "E4", "Base = recommended plan inside the ₹15 cr envelope · Downside = same spend, weaker outcomes · Aggressive = ₹18 cr (extra ₹3 cr option) · CFO-capped = gated reserve never released, FY28–29 hiring frozen", SM)
for j, s in enumerate(SCN): put(A, f"{L(3 + 3 * j)}7", s, BOLD); A.merge_cells(f"{L(3 + 3 * j)}7:{L(5 + 3 * j)}7")
put(A, "O7", "LIVE (selected)", BOLD); A.merge_cells("O7:Q7")
hdr(A, 8, ["Driver", "FY26 actual"] + ["FY27", "FY28", "FY29"] * 5 + ["Source / reasoning"])
# driver: key, label, FY26, base, down, aggr, capped, fmt, source
DRV = [
 ("win", "Direct win rate on qualified deals", 0.171, [0.195, 0.215, 0.225], [0.165, 0.175, 0.185], [0.21, 0.23, 0.245], [0.19, 0.205, 0.215], PCT,
  "DR1 clean FY26 direct 17.1% (D1). D2 tiering mix +2.9 pts at full effect; D5 battlecards +0.6 pts beyond D2; Inject 2 holds Helix-incumbent win at 7%. Board goal 23% by FY28 not met in Base (defended in memo)."),
 ("cycle", "Sales cycle, qualified to close (months)", 8.1, [8.0, 7.6, 7.3], [8.4, 8.4, 8.2], [7.8, 7.2, 6.8], [8.1, 7.8, 7.5], N1,
  "Brief/DR1: 5.2 → 8.1 months. D4 stage-exit rules and D3 business-case discipline shorten it slowly; paid pilots (D3) add time on large deals."),
 ("list", "Average won deal at list price (₹ lakh)", 71.4, [72, 74.5, 77], [70, 71, 72], [74, 78, 81], [72, 74, 76], N1,
  "DR1 FY26 won deals: ₹57.6 lakh at 19.3% discount = ₹71.4 lakh list. D2 strategic tier deals ₹71 lakh net; multi-plant expansion raises size."),
 ("disc", "Average discount on won deals", 0.193, [0.16, 0.15, 0.15], [0.18, 0.17, 0.17], [0.15, 0.14, 0.14], [0.16, 0.15, 0.15], PCT,
  "DR1 FY26 19.3%. D3 negotiation plan and D5 discount limits: cap 15% (CFO approval above). Inject 2: no matching of free Helix offer."),
 ("supply", "Qualified direct opportunities available (per year)", 392, [380, 430, 470], [340, 370, 400], [400, 470, 540], [370, 400, 430], N0,
  "DR1 FY26: 392 qualified direct deals closed. D2: tiered accounts + ₹24 cr programme reallocation to strategic/scaled tiers; SDR capacity."),
 ("attr", "AE annual attrition", 0.29, [0.24, 0.22, 0.20], [0.29, 0.27, 0.25], [0.22, 0.20, 0.18], [0.26, 0.24, 0.22], PCT,
  "DR3 FY26: 18 exits on ~63 AEs = 29%. Inject 1 AE retention pool (₹1.0 cr) targets 6–24-month tenure exits."),
 ("exp", "Expansion ARR (% of opening ARR, annual)", 0.081, [0.085, 0.095, 0.105], [0.07, 0.075, 0.08], [0.095, 0.11, 0.12], [0.08, 0.09, 0.095], PCT,
  "DR3 FY26 ₹22 cr on ₹272 cr. D1: non-Helix expansion stall (₹9.9 cr at stake); Inject 1 top-30 expansion programme; D2 Lotus Motors-type plans."),
 ("con", "Contraction (% of opening ARR, annual)", 0.033, [0.03, 0.025, 0.025], [0.035, 0.035, 0.03], [0.025, 0.022, 0.02], [0.03, 0.028, 0.026], PCT,
  "DR3 FY26 ₹9 cr. Usage-led adoption programme (retention squad)."),
 ("churn", "Churn (% of opening ARR excl. Vajra, annual)", 0.059, [0.05, 0.045, 0.04], [0.065, 0.06, 0.055], [0.045, 0.04, 0.035], [0.055, 0.05, 0.045], PCT,
  "DR3 FY26 ₹16 cr (5.9%). Helix-incumbent churn is the driver (D1: Helix NRR 116% → 92%). Retention squads, Helix renewal protection; HelixAsset free until 31 Mar 2027 keeps FY27 elevated (Inject 2)."),
 ("pact", "Partners activated in the year (count)", 0, [8, 9, 5], [8, 9, 5], [8, 11, 6], [8, 6, 4], N0,
  "D6: FY27 six prospects + P07, P10 reactivated; FY28 three held prospects + six new."),
 ("pprod", "Mature partner productivity (₹ cr sourced ARR / year)", 0.49, [1.2, 1.2, 1.2], [0.6, 0.6, 0.6], [1.4, 1.4, 1.4], [1.2, 1.2, 1.2], CR,
  "D6: ~10 qualified deals × 34% SEA partner win rate × ₹37 lakh. FY26 actual ₹0.49 cr per active partner (India-heavy). Downside ≈ FY26 India partners."),
 ("vaj_p", "Vajra re-tender: probability of losing the account (Inject 4)", 0, [0.20, 0, 0], [0.40, 0, 0], [0.15, 0, 0], [0.30, 0, 0], PCT,
  "Inject 4 sheet: 45% without a plan (Helix-incumbent win/loss pattern, HelixAsset free); retention plan lowers it."),
 ("hwatt", "Hardware revenue per ₹1 of new + expansion ARR", 1.48, [1.40, 1.20, 1.05], [1.45, 1.35, 1.25], [1.35, 1.10, 0.95], [1.40, 1.25, 1.10], "0.00",
  "DR3: 1.34 (FY24) → 1.38 → 1.48 (FY26). Falls with software-led expansion and the sensor-agnostic tier from Q4 FY27 (reuse installed sensors, D1 SENSOR-REUSE). At FY26 attach the GM floor breaks in FY28 (memo)."),
 ("vaj_c", "Vajra: price concession if retained", 0, [0.08, 0, 0], [0.12, 0, 0], [0.06, 0, 0], [0.10, 0, 0], PCT,
  "Inject 4: 3-year renewal with price lock; concession capped by D5 discount rules."),
]
R = {}
r = 9
for key, lab, fy26, b, d, a, c, fmt, src in DRV:
    R[key] = r; put(A, f"A{r}", lab); put(A, f"B{r}", fy26, BLUE, fmt)
    for j, vals in enumerate([b, d, a, c]):
        for y, v in enumerate(vals): put(A, f"{L(3 + 3 * j + y)}{r}", v, BLUE, fmt, YEL if key in ("win", "pprod", "exp", "churn", "cycle") and j == 0 else None)
    for y in range(3):
        cs = [L(3 + 3 * j + y) for j in range(4)]
        put(A, f"{L(15 + y)}{r}", f"=CHOOSE($C$5,{cs[0]}{r},{cs[1]}{r},{cs[2]}{r},{cs[3]}{r})", BOLD, fmt)
    put(A, f"R{r}", src, SM, wrap=False); r += 1
LIVE = lambda key, y: f"Assumptions!${L(15 + y)}${R[key]}"
FY26 = lambda key: f"Assumptions!$B${R[key]}"

# net new AE hires by quarter per scenario
r += 1; put(A, f"A{r}", "NET NEW AE HIRES BY QUARTER (headcount added, on top of backfills)", BOLD); r += 1
hdr(A, r, ["Scenario", ""] + Q + ["", "", "", "Note"]); r += 1
HIRES = {"Base": [0, 0, 6, 0, 4, 0, 4, 0, 4, 0, 2, 0], "Downside": [0, 0, 6, 0, 4, 0, 4, 0, 4, 0, 2, 0],
         "Aggressive": [0, 0, 6, 6, 5, 0, 5, 0, 4, 0, 4, 0], "CFO-capped": [0, 0, 6, 0, 3, 0, 0, 0, 3, 0, 0, 0]}
hr0 = r
for s in SCN:
    put(A, f"A{r}", s)
    for i, v in enumerate(HIRES[s]): put(A, f"{QC[i]}{r}", v, BLUE, N0)
    r += 1
put(A, f"A{r}", "Live: net new AE hires", BOLD)
for i in range(12): put(A, f"{QC[i]}{r}", f"=INDEX({QC[i]}{hr0}:{QC[i]}{hr0 + 3},$C$5)", BOLD, N0)
R["hires"] = r; put(A, f"R{hr0}", "Inject 1: 6 AEs from Q3 FY27 (SEA-weighted). Aggressive adds 6 in Q4 FY27 = 12, the FY27 limit.", SM); r += 2

# global inputs
put(A, f"A{r}", "GLOBAL INPUTS", BOLD); r += 1
hdr(A, r, ["Input", "Value", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "Source / reasoning"]); r += 1
G = [("conc", "Qualified deals an AE carries at once (ramped AE)", 5.4, N1, "Calibrated: FY26 392 direct qualified closes ÷ 48.5 ramped-AE years × 8.1-month cycle ÷ 12 (DR3 ae_quarterly, DR1)", True),
 ("w0", "Ramp weight: AE tenure 0–6 months", 0.0, "0.00", "D1 productivity by tenure: ₹0 / 0.29 / 0.59 / 0.89 cr per AE-year → weights 0 / 0.33 / 0.66 / 1.0", False),
 ("w1", "Ramp weight: 6–12 months", 0.33, "0.00", "", False), ("w2", "Ramp weight: 12–24 months", 0.66, "0.00", "", False), ("w3", "Ramp weight: 24+ months", 1.0, "0.00", "", False),
 ("m0", "Attrition multiplier: 0–6 months", 0.8, "0.00", "DR3 exits concentrate at 6–24 months tenure (D1)", False), ("m1", "Attrition multiplier: 6–12 months", 1.4, "0.00", "", False),
 ("m2", "Attrition multiplier: 12–24 months", 1.3, "0.00", "", False), ("m3", "Attrition multiplier: 24+ months", 0.85, "0.00", "", False),
 ("s0", "AEs at 31 Mar 2026: 0–6 months", 9, N0, "DR3 ae_roster (64 active)", False), ("s1", "AEs at 31 Mar 2026: 6–12 months", 8, N0, "", False),
 ("s2", "AEs at 31 Mar 2026: 12–24 months", 9, N0, "", False), ("s3", "AEs at 31 Mar 2026: 24+ months", 38, N0, "", False),
 ("bf0", "Backfill hires in Q1 FY27 (for Q4 FY26 exits)", 3.8, N1, "Holds headcount at 64 before net new hires (FY26 exits averaged 4.5 a quarter; FY27 attrition lower)", False),
 ("q1nl", "Q1 FY27 total new-logo ARR (locked D4 forecast, p50)", 8.71, CR, "D4_holdout_forecast_LOCKED.json (sha256 ba5b63ad…). Quarter under way when plan set.", True),
 ("aecost", "AE loaded cost FY26 (₹ cr / AE-year)", 0.56, CR, "DR3: AE compensation ₹35.25 cr ÷ 62.9 AE-years", False),
 ("infl", "Cost inflation per year", 0.06, PCT, "Assumption (salary inflation India)", False),
 ("rec", "Recruiting cost per AE hire (₹ cr)", 0.035, "0.000", "DR3 unit costs ₹3.5 lakh", False),
 ("smoth", "S&M excl. AE pay and partner commissions, FY26 (₹ cr)", 60.33, CR, "DR3 sm_by_line FY26: ₹96.0 − 35.25 AE pay − 0.42 partner commissions", False),
 ("subr", "Subscription revenue ÷ average ARR", 1.0, "0.000", "DR3 FY26: ₹295.2 cr revenue on ₹295.2 cr average quarterly ARR", False),
 ("swc", "Software cost of revenue (% of subscription revenue)", 0.18, PCT, "DR3 FY26 ₹53.1 cr ÷ ₹295.2 cr", False),
 ("hwc", "Hardware cost of revenue (% of hardware revenue)", 0.75, PCT, "DR3 FY26; unit costs: hardware ~25% gross margin", False),
 ("rnd0", "R&D FY26 (₹ cr)", 123.32, CR, "DR3", False), ("rndg", "R&D growth per year", 0.06, PCT, "Assumption: held near inflation; no new hardware (guardrail)", False),
 ("gna0", "G&A FY26 (₹ cr)", 69.37, CR, "DR3", False), ("gnag", "G&A growth per year", 0.04, PCT, "Assumption: operating leverage", False),
 ("ex0", "Existing partners' sourced ARR FY27 after Inject 3 (₹ cr)", 2.256, CR, "D6 Partner_ramp (₹2.6 cr × (1 − 13.2%) Inject 3 haircut)", False),
 ("exg", "Existing partners' ARR growth per year", 0.10, PCT, "D6", False),
 ("r0", "Partner ramp: activation year (share of mature)", 0.15, PCT, "D6: mid-year activation, first deal after 6–12 months (DR6)", True),
 ("r1", "Partner ramp: second year", 0.60, PCT, "D6", True), ("r2", "Partner ramp: third year", 1.0, PCT, "D6", False),
 ("pwin", "Partner-deal win rate (mature SEA partners)", 0.34, PCT, "D1: SEA partner-sourced 34%. Win-rate shift applies to partners too (cascade).", False),
 ("pdeal", "Average partner deal (₹ cr)", 0.37, CR, "DR1 FY26 partner-sourced won deals", False),
 ("pq1", "Partner ARR phasing: Q1 share of year", 0.20, PCT, "Recruits back-load each year (D6 ramp)", False), ("pq2", "Q2 share", 0.23, PCT, "", False), ("pq3", "Q3 share", 0.27, PCT, "", False), ("pq4", "Q4 share", 0.30, PCT, "", False),
 ("m1y27", "Blended year-1 partner margin FY27", 0.164, PCT, "D6 tiers 10% / 18% / 22% × mix", False), ("m1y28", "Blended year-1 partner margin FY28", 0.17, PCT, "D6", False), ("m1y29", "Blended year-1 partner margin FY29", 0.176, PCT, "D6", False),
 ("mr28", "Blended renewal margin FY28", 0.065, PCT, "D6", False), ("mr29", "Blended renewal margin FY29", 0.07, PCT, "D6", False),
 ("cf27", "Channel fixed cost excl. MDF FY27 (₹ cr)", 2.44, CR, "D6 Inputs (VP Channel, partner managers, enablement, PRM) = Inject 1 envelope line", False),
 ("cf28", "Channel fixed cost excl. MDF FY28", 3.46, CR, "D6", False), ("cf29", "Channel fixed cost excl. MDF FY29", 4.00, CR, "D6", False),
 ("mdf27", "Partner MDF FY27 (inside existing ₹24 cr programme budget)", 1.5, CR, "D6; reallocated, not incremental", False), ("mdf28", "Partner MDF FY28", 2.0, CR, "D6", False), ("mdf29", "Partner MDF FY29", 2.5, CR, "D6", False),
 ("de27", "Direct effort share on partner deals FY27", 0.40, PCT, "D6", False), ("de28", "FY28", 0.35, PCT, "D6", False), ("de29", "FY29", 0.30, PCT, "D6", False),
 ("dsm", "Direct S&M cost per ₹1 of new-logo ARR", 1.64, CR, "DR3 allocation (70% of ₹96 cr S&M ÷ ₹41 cr); D6", False),
 ("el", "Win-rate response to discount (pts of win per pt of discount)", 0.10, "0.00", "D1/D5: discount creep bought little (DISCOUNT-NO-EFFECT); assumption for the trade-off", True),
 ("vaj", "Vajra Auto Components ARR (₹ cr, renewal Q4 FY27)", 9.5, CR, "Inject 4; DR2 CU-1095", False),
 ("dn_nl", "Do-nothing: FY26 new-logo ARR (₹ cr)", 41.0, CR, "DR3", False), ("dn_nlg", "Do-nothing: new-logo change per year", -0.05, PCT, "Win rate fell 27% → 17% over FY24–26 (D1); trend continues without action", True),
 ("dn_nrr", "Do-nothing: FY26 NRR", 0.989, PCT, "D1", False), ("dn_nrrg", "Do-nothing: NRR change per year (pts)", -0.01, PCT, "D1: 118% → 112% → 98.9%; Helix pressure continues", True),
 ("env", "FY27 investment envelope (Base, Downside, CFO-capped)", 15.0, CR, "Inject 1: CFO cap accepted", False), ("envA", "FY27 envelope (Aggressive)", 18.0, CR, "Original guardrail; requires payback ≤ 15 months on the extra ₹3 cr", False),
 ("g27", "Board growth path FY27", 0.15, PCT, "Brief guardrail", False), ("g28", "Board growth path FY28", 0.20, PCT, "", False), ("g29", "Board growth path FY29", 0.22, PCT, "", False),
 ("nrrT", "Board NRR goal FY29", 1.08, PCT, "Brief objectives", False), ("gmf", "Gross margin floor", 0.66, PCT, "Guardrail", False),
 ("pb1", "CAC payback cap, every quarter (months)", 30, N0, "Guardrail", False), ("pb2", "CAC payback cap by Q4 FY28 (months)", 24, N0, "Guardrail", False),
 ("smcap", "S&M as % of ARR, FY29 cap", 0.30, PCT, "Guardrail (from 31%)", False), ("aecap", "Net new AEs in FY27, cap", 12, N0, "Guardrail", False), ("chcap", "New channel roles, cap", 6, N0, "Guardrail", False),
]
for key, lab, v, fmt, src, key_ in G:
    R[key] = r; put(A, f"A{r}", lab); put(A, f"B{r}", v, BLUE, fmt, YEL if key_ else None); put(A, f"R{r}", src, SM); r += 1
GI = lambda key: f"Assumptions!$B${R[key]}"
r += 1; put(A, f"A{r}", "SENSITIVITY SHIFTS (leave at 0 for the plan; applied on top of the selected scenario)", BOLD); r += 1
for key, lab, fmt, src in [("dwin", "Win-rate shift (percentage points, direct and partner)", "0.0", "Cascade test: set to 3"), ("dcyc", "Sales-cycle shift (months)", "0.0", ""),
                           ("ddisc", "Discount shift (percentage points)", "0.0", "Also moves win rate by the response above"), ("dpp", "Partner productivity shift (%)", "0%", ""),
                           ("dchurn", "Churn shift (percentage points of annual churn)", "0.0", ""),
                           ("ddel", "Share of planned improvement delivered (1 = plan; 0 = FY26 levels)", "0%", "Applies to win, cycle, deal, discount, supply, attrition, retention rates and partner productivity")]:
    R[key] = r; put(A, f"A{r}", lab, BOLD); put(A, f"B{r}", 1 if key == "ddel" else 0, BLUE, fmt, YEL); put(A, f"R{r}", src, SM); r += 1
ENVLIVE = f'IF(Assumptions!$C$5=3,{GI("envA")},{GI("env")})'

# helper: delivery-adjusted live value and quarterly interpolation of an annual driver
DELK = {"win", "cycle", "list", "disc", "supply", "attr", "exp", "con", "churn", "pprod"}
def LV(key, y):
    if key not in DELK: return LIVE(key, y)
    return f"({FY26(key)}+({LIVE(key, y)}-{FY26(key)})*Assumptions!$B${R['ddel']})"
def interp(key, i, shift=""):
    y, k = divmod(i, 4)
    prev = FY26(key) if y == 0 else LV(key, y - 1)
    return f"({prev}+({LV(key, y)}-{prev})*{k + 1}/4){shift}"

# ---------------------------------------------------------------- CAPACITY
C = sh("Capacity", [46, 11] + [9.5] * 15 + [55])
title(C, "AE capacity: hiring, ramp, attrition", "Cohorts by tenure band. Hires enter the 0–6 month band; half of each 6-month band and a quarter of the 12–24 band move up each quarter. Leavers are backfilled the next quarter.")
qhdr(C)
rows = {}
def crow(key, lab, r, f=BLK, fmt=N1): rows[key] = r; put(C, f"A{r}", lab, f); return r
crow("hire", "Net new AE hires", 5); crow("bf", "Backfill hires (last quarter's leavers)", 6); crow("att", "Quarterly attrition rate (base)", 7)
for i in range(12):
    c = QC[i]; put(C, f"{c}5", f"=Assumptions!{c}{R['hires']}", GRN, N0)
    put(C, f"{c}6", f"={GI('bf0')}" if i == 0 else f"={QC[i-1]}{{EX}}", BLK, N1)
    put(C, f"{c}7", f"={LV('attr', i // 4)}/4", BLK, PCT)
r = 9
for b in range(4):
    put(C, f"A{r}", f"Band {['0–6', '6–12', '12–24', '24+'][b]} months", BOLD, fill=SUB); r += 1
    for sub in ["start", "exits", "moving up", "end"]:
        rows[(b, sub)] = r; put(C, f"A{r}", f"  {sub}"); r += 1
for b in range(4):
    put(C, f"B{rows[(b, 'end')]}", f"={GI('s' + str(b))}", GRN, N1)
frac = [0.5, 0.5, 0.25, 0]
for i in range(12):
    c = QC[i]; p = "B" if i == 0 else QC[i - 1]
    for b in range(4):
        st, ex, up, en = (rows[(b, s)] for s in ["start", "exits", "moving up", "end"])
        start = f"={p}{en}" + (f"+{c}5+{c}6" if b == 0 else "")
        put(C, f"{c}{st}", start, BLK, N1)
        put(C, f"{c}{ex}", f"={c}{st}*{c}7*{GI('m' + str(b))}", BLK, N1)
        put(C, f"{c}{up}", f"=({c}{st}-{c}{ex})*{frac[b]}", BLK, N1)
        inflow = f"+{c}{rows[(b - 1, 'moving up')]}" if b > 0 else ""
        put(C, f"{c}{en}", f"={c}{st}-{c}{ex}-{c}{up}{inflow}", BLK, N1)
r += 1
crow("hc", "AE headcount, end of quarter", r, BOLD); crow("ex", "Leavers in quarter", r + 1); crow("aey", "AE-years in quarter (for cost)", r + 2, fmt="0.00")
crow("rea", "Ramped-AE equivalents (quarter average)", r + 3, BOLD); crow("eff", "Effective annual attrition", r + 4); crow("cum", "Cumulative net new AEs (from 64)", r + 5)
put(C, f"B{rows['hc']}", f"=SUM(B{rows[(0,'end')]},B{rows[(1,'end')]},B{rows[(2,'end')]},B{rows[(3,'end')]})", BOLD, N1)
for i in range(12):
    c = QC[i]
    put(C, f"{c}{rows['hc']}", "=" + "+".join(f"{c}{rows[(b, 'end')]}" for b in range(4)), BOLD, N1)
    put(C, f"{c}{rows['ex']}", "=" + "+".join(f"{c}{rows[(b, 'exits')]}" for b in range(4)), BLK, N1)
    put(C, f"{c}{rows['aey']}", "=(" + "+".join(f"{c}{rows[(b, 'start')]}-{c}{rows[(b, 'exits')]}/2" for b in range(4)) + ")/4", BLK, "0.00")
    put(C, f"{c}{rows['rea']}", "=" + "+".join(f"({c}{rows[(b, 'start')]}-{c}{rows[(b, 'exits')]}/2)*{GI('w' + str(b))}" for b in range(4)), BOLD, N1)
    put(C, f"{c}{rows['eff']}", f"={c}{rows['ex']}*4/({c}{rows['hc']}+{c}{rows['ex']})", BLK, PCT)
    put(C, f"{c}{rows['cum']}", f"=SUM($C$5:{c}5)", BLK, N0)
for i in range(1, 12): C[f"{QC[i]}6"].value = f"={QC[i-1]}{rows['ex']}"
ysum(C, rows["hire"], N0); ysum(C, rows["ex"], N1); ysum(C, rows["aey"], "0.00"); ysum(C, rows["hc"], N1, BOLD, "end"); ysum(C, rows["rea"], N1, BOLD, "avg")
note(C, rows["rea"], "Weights 0 / 0.33 / 0.66 / 1.0 by tenure band (D1). FY26 actual: 48.5 ramped-AE years.")
note(C, rows["hc"], "Guardrail: ≤ 76 at end-FY27 (64 + 12)")
CAP = rows

# ---------------------------------------------------------------- BOOKINGS
B = sh("Bookings", [50, 11] + [9.5] * 15 + [55])
title(B, "Direct new-logo bookings and pipeline required", "Capacity (ramped AEs × deals carried × 3 ÷ cycle) meets pipeline supply; bookings = deals worked × win rate × net deal size. Q1 FY27 = locked D4 forecast.")
qhdr(B)
br = {}
lines = [("win", "Win rate (incl. shifts)", PCT), ("cyc", "Sales cycle (months)", N1), ("disc", "Discount", PCT), ("deal", "Net won deal (₹ cr)", CR),
         ("cap", "AE deal capacity (qualified deals closed / quarter)", N1), ("sup", "Qualified pipeline supply (deals / quarter)", N1), ("work", "Qualified deals worked to close", N1),
         ("bind", "Binding constraint", None), ("wins", "Deals won", N1), ("dir", "Direct new-logo ARR (₹ cr)", CR), ("pipe", "Pipeline required = direct ARR ÷ win rate (₹ cr)", CR),
         ("util", "AE capacity used", PCT)]
for k, (key, lab, fmt) in enumerate(lines): br[key] = 5 + k; put(B, f"A{5 + k}", lab, BOLD if key in ("dir", "pipe") else BLK)
WS = f"Assumptions!$B${R['dwin']}/100"; CS = f"Assumptions!$B${R['dcyc']}"; DS = f"Assumptions!$B${R['ddisc']}/100"
for i in range(12):
    c = QC[i]; y = i // 4
    put(B, f"{c}{br['win']}", "=MAX(0.01," + interp("win", i) + f"+{WS}+{GI('el')}*{DS}*100/100)", BLK, PCT)
    put(B, f"{c}{br['cyc']}", "=MAX(3," + interp("cycle", i) + f"+{CS})", BLK, N1)
    put(B, f"{c}{br['disc']}", "=" + interp("disc", i) + f"+{DS}", BLK, PCT)
    put(B, f"{c}{br['deal']}", "=" + interp("list", i) + f"*(1-{c}{br['disc']})/100", BLK, CR)
    put(B, f"{c}{br['cap']}", f"=Capacity!{c}{CAP['rea']}*{GI('conc')}*3/{c}{br['cyc']}", BLK, N1)
    put(B, f"{c}{br['sup']}", f"={LV('supply', y)}/4", BLK, N1)
    put(B, f"{c}{br['work']}", f"=MIN({c}{br['cap']},{c}{br['sup']})", BLK, N1)
    put(B, f"{c}{br['bind']}", f'=IF({c}{br["cap"]}<{c}{br["sup"]},"AE capacity","Pipeline")', SM)
    put(B, f"{c}{br['wins']}", f"={c}{br['dir']}/{c}{br['deal']}" if i == 0 else f"={c}{br['work']}*{c}{br['win']}", BLK, N1)
    put(B, f"{c}{br['dir']}", f"={GI('q1nl')}-Channel!{c}{{PQ}}" if i == 0 else f"={c}{br['work']}*{c}{br['win']}*{c}{br['deal']}", BOLD, CR)
    put(B, f"{c}{br['pipe']}", f"={c}{br['dir']}/{c}{br['win']}", BOLD, CR)
    put(B, f"{c}{br['util']}", f"={c}{br['work']}/{c}{br['cap']}", BLK, PCT)
for key in ("sup", "work", "wins", "dir", "pipe", "cap"): ysum(B, br[key], CR if key in ("dir", "pipe") else N1, BOLD if key in ("dir", "pipe") else BLK)
for key in ("win", "cyc", "disc", "deal"): ysum(B, br[key], PCT if key in ("win", "disc") else (N1 if key == "cyc" else CR), BLK, "avg")
note(B, br["dir"], "Q1 FY27: D4 locked p50 ₹8.71 cr total new-logo less partner ARR. Win-rate shifts do not move Q1 (already forecast).")
note(B, br["win"], "Linear path from FY26 actual to each year's scenario value")
# board-path requirement (annual)
r = 19; put(B, f"A{r}", "BOARD GROWTH PATH: WHAT IT WOULD TAKE", BOLD); r += 1
bp = {}
for k, (key, lab, fmt) in enumerate([("need", "Total new-logo ARR needed for board path (₹ cr)", CR), ("needd", "Direct new-logo ARR needed (₹ cr)", CR), ("reqd", "Qualified deals needed at plan win rate and deal size", N0),
                                   ("capy", "AE deal capacity in the year", N0), ("gap", "Capacity surplus / (gap), deals", N0), ("aes", "Extra ramped AEs needed to close the gap", N1),
                                   ("winreq", "Or: win rate needed with plan capacity", PCT)]):
    bp[key] = r + k; put(B, f"A{r + k}", lab, BOLD if key in ("gap", "winreq") else BLK)
for y, col in enumerate(YC):
    put(B, f"{col}{bp['need']}", f"=ARR_bridge!{col}{{BOARD}}-(ARR_bridge!{col}{{OPEN}}+ARR_bridge!{col}{{EXPN}}-ARR_bridge!{col}{{CONT}}-ARR_bridge!{col}{{CHRN}}-ARR_bridge!{col}{{VAJ}})", BLK, CR)
    put(B, f"{col}{bp['needd']}", f"={col}{bp['need']}-Channel!{col}{{PQ}}", BLK, CR)
    put(B, f"{col}{bp['reqd']}", f"={col}{bp['needd']}/({col}{br['win']}*{col}{br['deal']})", BLK, N0)
    put(B, f"{col}{bp['capy']}", f"={col}{br['cap']}", BLK, N0)
    put(B, f"{col}{bp['gap']}", f"={col}{bp['capy']}-{col}{bp['reqd']}", BOLD, '#,##0;(#,##0)')
    put(B, f"{col}{bp['aes']}", f"=MAX(0,-{col}{bp['gap']})/({GI('conc')}*12/{col}{br['cyc']})", BLK, N1)
    put(B, f"{col}{bp['winreq']}", f"={col}{bp['needd']}/(MIN({col}{br['cap']},{col}{br['sup']})*{col}{br['deal']})", BOLD, PCT)
note(B, bp["gap"], "Negative = the board path needs more AE capacity or pipeline than the plan funds")

# ---------------------------------------------------------------- CHANNEL
H = sh("Channel", [52, 11] + [9.5] * 15 + [55])
title(H, "Channel: partner-sourced ARR and channel P&L", "Reproduces D6 in the Base scenario. Partner ARR is counted once (not in direct bookings). Win-rate shift scales partner win rate too.")
hdr(H, 4, ["Line", ""] + [""] * 12 + ["FY27", "FY28", "FY29", "Note / source"])
hc = {}
labs = [("act", "Partners activated in year", N0), ("actv", "Active partners, end of year", N0), ("prod", "Mature productivity, after shifts (₹ cr)", CR), ("exist", "Existing partners' ARR", CR),
        ("c27", "FY27 recruits' ARR", CR), ("c28", "FY28 recruits' ARR", CR), ("c29", "FY29 recruits' ARR", CR), ("parr", "Partner-sourced new-logo ARR (₹ cr)", CR),
        ("share", "Share of total new-logo ARR", PCT), ("m1", "Year-1 partner margin", CR), ("mr", "Renewal margin on earlier partner cohorts", CR), ("pm", "Total partner margin (in gross margin)", CR),
        ("fix", "Channel fixed cost excl. MDF (incremental)", CR), ("mdf", "Partner MDF (inside existing programme budget)", CR), ("de", "Direct effort on partner deals (AE, SE, 50% credit)", CR),
        ("tc", "Total channel cost", CR), ("sav", "Direct S&M cost avoided", CR), ("net", "Saving / (extra cost) vs selling direct", CR), ("inc", "Incremental lens, first year: gross profit − total cost", CR),
        ("be", "Break-even sourced ARR per active partner (substitution, ₹ cr)", CR), ("preq", "Partner pipeline required = partner ARR ÷ partner win rate (₹ cr)", CR),
        ("pcap", "Partner pipeline capacity: mature-equivalent partners × 10 deals × deal (₹ cr)", CR)]
for k, (key, lab, fmt) in enumerate(labs): hc[key] = 5 + k; put(H, f"A{5 + k}", lab, BOLD if key in ("parr", "net", "pm", "be") else BLK)
WM = f"(({GI('pwin')}+{WS})/{GI('pwin')})"; PP = f"(1+Assumptions!$B${R['dpp']})"
ramp = [GI("r0"), GI("r1"), GI("r2")]
for y, col in enumerate(YC):
    put(H, f"{col}{hc['act']}", f"={LIVE('pact', y)}", GRN, N0)
    put(H, f"{col}{hc['actv']}", f"=6+SUM($O${hc['act']}:{col}{hc['act']})", BLK, N0)
    put(H, f"{col}{hc['prod']}", f"={LV('pprod', y)}*{PP}*{WM}", BLK, CR)
    put(H, f"{col}{hc['exist']}", f"={GI('ex0')}*(1+{GI('exg')})^{y}*{WM}", BLK, CR)
    for c_ in range(3):
        key = ["c27", "c28", "c29"][c_]
        if y >= c_: put(H, f"{col}{hc[key]}", f"={YC[c_]}{hc['act']}*{col}{hc['prod']}*{ramp[y - c_]}", BLK, CR)
        else: put(H, f"{col}{hc[key]}", 0, BLK, CR)
    put(H, f"{col}{hc['parr']}", f"=SUM({col}{hc['exist']}:{col}{hc['c29']})", BOLD, CR)
    put(H, f"{col}{hc['share']}", f"={col}{hc['parr']}/({col}{hc['parr']}+Bookings!{col}{br['dir']})", BOLD, PCT)
    put(H, f"{col}{hc['m1']}", f"={col}{hc['parr']}*{GI('m1y' + str(27 + y))}", BLK, CR)
    put(H, f"{col}{hc['mr']}", "=0" if y == 0 else (f"=O{hc['parr']}*{GI('mr28')}" if y == 1 else f"=(O{hc['parr']}+P{hc['parr']})*{GI('mr29')}"), BLK, CR)
    put(H, f"{col}{hc['pm']}", f"={col}{hc['m1']}+{col}{hc['mr']}", BOLD, CR)
    put(H, f"{col}{hc['fix']}", f"={GI('cf' + str(27 + y))}", GRN, CR)
    put(H, f"{col}{hc['mdf']}", f"={GI('mdf' + str(27 + y))}", GRN, CR)
    put(H, f"{col}{hc['de']}", f"={col}{hc['parr']}*{GI('de' + str(27 + y))}*{GI('dsm')}", BLK, CR)
    put(H, f"{col}{hc['tc']}", f"={col}{hc['pm']}+{col}{hc['fix']}+{col}{hc['mdf']}+{col}{hc['de']}", BOLD, CR)
    put(H, f"{col}{hc['sav']}", f"={col}{hc['parr']}*{GI('dsm')}", BLK, CR)
    put(H, f"{col}{hc['net']}", f"={col}{hc['sav']}-{col}{hc['tc']}", BOLD, CR)
    put(H, f"{col}{hc['inc']}", f"={col}{hc['parr']}*PnL!{col}{{GMPRE}}-{col}{hc['tc']}", BLK, CR)
    put(H, f"{col}{hc['be']}", f"=({col}{hc['fix']}+{col}{hc['mdf']})/({col}{hc['actv']}*({GI('dsm')}*(1-{GI('de' + str(27 + y))})-{GI('m1y' + str(27 + y))}))", BOLD, CR)
    put(H, f"{col}{hc['preq']}", f"={col}{hc['parr']}/({GI('pwin')}+{WS})", BLK, CR)
    put(H, f"{col}{hc['pcap']}", f"={col}{hc['parr']}/MAX(0.01,{col}{hc['prod']})*10*{GI('pdeal')}", BLK, CR)
note(H, hc["parr"], "D6 Base: ₹3.70 / 9.86 / 19.71 cr"); note(H, hc["be"], "D6 panel answer (~₹0.24 cr in FY29)"); note(H, hc["actv"], "6 retained existing partners (D6 keep/fix) + activations")
note(H, hc["pcap"], "Mature-equivalent partners × 10 qualified deals a year × average partner deal")
# quarterly partner ARR
put(H, "A28", "Quarterly partner-sourced ARR (₹ cr)", BOLD); hc["pq"] = 28
put(H, "A29", "Quarterly partner margin (₹ cr)"); hc["pmq"] = 29
for i in range(12):
    c = QC[i]; y, k = divmod(i, 4)
    put(H, f"{c}28", f"={YC[y]}{hc['parr']}*{GI('pq' + str(k + 1))}", BOLD, CR)
    put(H, f"{c}29", f"={YC[y]}{hc['pm']}*{GI('pq' + str(k + 1))}", BLK, CR)
for i, c in enumerate(QC): H[f"{c}4"].value = Q[i]
put(H, "A30", "Check: quarterly phasing sums to annual"); put(H, "O30", f"=ABS(SUM(C28:N28)-SUM(O{hc['parr']}:Q{hc['parr']}))", BLK, "0.000")

# ---------------------------------------------------------------- ARR BRIDGE
Br = sh("ARR_bridge", [48, 11] + [9.5] * 15 + [55])
title(Br, "Quarterly ARR bridge, FY27–FY29", "Opening + new logo (direct + partner) + expansion − contraction − churn − Vajra re-tender = closing. Retention rates apply to opening ARR excluding Vajra until its Q4 FY27 renewal.")
qhdr(Br)
ab = {}
blines = [("open", "Opening ARR"), ("dir", "New logo: direct"), ("par", "New logo: partner-sourced"), ("expn", "Expansion"), ("cont", "Contraction"), ("chrn", "Churn"),
          ("vaj", "Vajra re-tender (Inject 4): expected ARR lost"), ("close", "Closing ARR"), ("chk", "Check: bridge ties (should be 0)"), ("base", "ARR base for retention rates (excl. Vajra in FY27)")]
for k, (key, lab) in enumerate(blines): ab[key] = 5 + k; put(Br, f"A{5 + k}", lab, BOLD if key in ("open", "close") else BLK)
put(Br, f"B{ab['close']}", 310.0, BLUE, C1); note(Br, ab["close"], "FY26 closing ARR ₹310 cr (DR3)")
CH = f"Assumptions!$B${R['dchurn']}/100"
for i in range(12):
    c = QC[i]; p = "B" if i == 0 else QC[i - 1]; y = i // 4
    put(Br, f"{c}{ab['open']}", f"={p}{ab['close']}", BLK, C1)
    put(Br, f"{c}{ab['base']}", f"={c}{ab['open']}-" + (GI("vaj") if y == 0 else "0"), BLK, C1)
    put(Br, f"{c}{ab['dir']}", f"=Bookings!{c}{br['dir']}", GRN, CR)
    put(Br, f"{c}{ab['par']}", f"=Channel!{c}{hc['pq']}", GRN, CR)
    put(Br, f"{c}{ab['expn']}", f"={c}{ab['base']}*" + interp("exp", i) + "/4", BLK, CR)
    put(Br, f"{c}{ab['cont']}", f"={c}{ab['base']}*" + interp("con", i) + "/4", BLK, CR)
    put(Br, f"{c}{ab['chrn']}", f"={c}{ab['base']}*MAX(0," + interp("churn", i) + f"+{CH})/4", BLK, CR)
    put(Br, f"{c}{ab['vaj']}", f"=Inject4!$C$14" if i == 3 else "=0", GRN if i == 3 else BLK, CR)
    put(Br, f"{c}{ab['close']}", f"={c}{ab['open']}+{c}{ab['dir']}+{c}{ab['par']}+{c}{ab['expn']}-{c}{ab['cont']}-{c}{ab['chrn']}-{c}{ab['vaj']}", BOLD, C1)
    put(Br, f"{c}{ab['chk']}", f"=ROUND({c}{ab['close']}-({c}{ab['open']}+{c}{ab['dir']}+{c}{ab['par']}+{c}{ab['expn']}-{c}{ab['cont']}-{c}{ab['chrn']}-{c}{ab['vaj']}),6)", BLK, "0.000000")
ysum(Br, ab["open"], C1, BOLD, "start"); ysum(Br, ab["close"], C1, BOLD, "end")
for key in ("dir", "par", "expn", "cont", "chrn", "vaj", "chk"): ysum(Br, ab[key], CR)
r = 17; ann = {}
for k, (key, lab, fmt) in enumerate([("nl", "Total new-logo ARR", CR), ("growth", "ARR growth", PCT), ("board", "Board-path closing ARR", C1), ("gapb", "Closing ARR vs board path", C1),
                                     ("nrr", "Net revenue retention (opening-base approximation)", PCT), ("grr", "Gross revenue retention", PCT), ("dn", "Do-nothing closing ARR", C1), ("inc", "Incremental ARR vs do-nothing", C1)]):
    ann[key] = r + k; put(Br, f"A{r + k}", lab, BOLD)
for y, col in enumerate(YC):
    put(Br, f"{col}{ann['nl']}", f"={col}{ab['dir']}+{col}{ab['par']}", BOLD, CR)
    put(Br, f"{col}{ann['growth']}", f"={col}{ab['close']}/{col}{ab['open']}-1", BOLD, PCT)
    put(Br, f"{col}{ann['board']}", f"={'B' + str(ab['close']) if y == 0 else YC[y-1] + str(ann['board'])}*(1+{GI('g' + str(27 + y))})", BLK, C1)
    put(Br, f"{col}{ann['gapb']}", f"={col}{ab['close']}-{col}{ann['board']}", BOLD, '#,##0.0;(#,##0.0)')
    put(Br, f"{col}{ann['nrr']}", f"=({col}{ab['open']}+{col}{ab['expn']}-{col}{ab['cont']}-{col}{ab['chrn']}-{col}{ab['vaj']})/{col}{ab['open']}", BOLD, PCT)
    put(Br, f"{col}{ann['grr']}", f"=({col}{ab['open']}-{col}{ab['cont']}-{col}{ab['chrn']}-{col}{ab['vaj']})/{col}{ab['open']}", BLK, PCT)
    put(Br, f"{col}{ann['dn']}", f"=Do_nothing!{L(3 + y)}8", GRN, C1)
    put(Br, f"{col}{ann['inc']}", f"={col}{ab['close']}-{col}{ann['dn']}", BOLD, C1)
put(Br, f"B{ann['growth']}", "=310/272-1", BLK, PCT); note(Br, ann["growth"], "FY26: 14.0%. Board path 15% / 20% / 22%.")
note(Br, ann["nrr"], "FY26 98.9% (D1). Board goal 108% by FY29.")

# ---------------------------------------------------------------- DO NOTHING
Dn = sh("Do_nothing", [48, 11, 11, 11, 11, 60])
title(Dn, "Counterfactual: do nothing", "64 AEs, no investment, FY24–26 trends continue (win rate falling, Helix pressure on NRR). Used for investment payback and the CEO's question.")
hdr(Dn, 4, ["Line", "FY26", "FY27", "FY28", "FY29", "Note"])
put(Dn, "A5", "New-logo ARR"); put(Dn, "B5", f"={GI('dn_nl')}", GRN, CR)
put(Dn, "A6", "NRR"); put(Dn, "B6", f"={GI('dn_nrr')}", GRN, PCT)
put(Dn, "A7", "Opening ARR"); put(Dn, "A8", "Closing ARR", BOLD); put(Dn, "B8", 310, BLUE, C1); put(Dn, "A9", "Growth")
for y in range(3):
    c = L(3 + y); p = L(2 + y)
    put(Dn, f"{c}5", f"={p}5*(1+{GI('dn_nlg')})", BLK, CR); put(Dn, f"{c}6", f"={p}6+{GI('dn_nrrg')}", BLK, PCT)
    put(Dn, f"{c}7", f"={p}8", BLK, C1); put(Dn, f"{c}8", f"={c}7*{c}6+{c}5", BOLD, C1); put(Dn, f"{c}9", f"={c}8/{c}7-1", BLK, PCT)
put(Dn, "A11", "CONSERVATIVE COUNTERFACTUAL: FY26 rates held flat (no further decline)", BOLD)
put(Dn, "A12", "New-logo ARR"); put(Dn, "B12", f"={GI('dn_nl')}", GRN, CR); put(Dn, "A13", "NRR"); put(Dn, "B13", f"={GI('dn_nrr')}", GRN, PCT)
put(Dn, "A14", "Closing ARR", BOLD); put(Dn, "B14", 310, BLUE, C1)
for y in range(3):
    c = L(3 + y); p = L(2 + y)
    put(Dn, f"{c}12", f"={p}12", BLK, CR); put(Dn, f"{c}13", f"={p}13", BLK, PCT); put(Dn, f"{c}14", f"={p}14*{c}13+{c}12", BOLD, C1)
put(Dn, "F14", "Stricter test: credits the plan only with gains beyond FY26 performance", SM)
put(Dn, "F8", "Do-nothing still grows (~9–10% a year) because the base renews; it misses the board path by more each year.", SM)

# ---------------------------------------------------------------- INVESTMENT
I = sh("Investment", [58, 9, 9, 9, 8, 8, 8, 8, 10, 10, 10, 10, 50])
title(I, "Investment: FY27 envelope and run-rate cost of initiatives", "Costs in ₹ cr. Flags (1/0) say which scenarios include a line. Q2 lines start once the plan is approved (Q2 FY27); H2 lines start in Q3 FY27. AE hiring and channel lines link to the model.")
hdr(I, 4, ["Initiative", "FY27", "FY28", "FY29", "Base", "Down", "Aggr", "Capped", "Phasing FY27", "Live FY27", "Live FY28", "Live FY29", "Source / what it buys"])
INV = [("Retention squad: 4 CSMs + adoption programme", 1.52, 1.61, 1.71, [1, 1, 1, 1], "Even", "S&M", "Inject 1; churn and contraction assumptions"),
 ("Top-30 expansion programme (incentives + 1 solutions architect)", 0.82, 0.87, 0.92, [1, 1, 1, 1], "Q2", "S&M", "Inject 1; expansion assumption"),
 ("AE retention pool (tenured AEs)", 1.00, 1.06, 1.12, [1, 1, 1, 1], "Q2", "S&M", "Inject 1; AE attrition assumption"),
 ("Partner incentives and SPIFFs", 0.40, 0.50, 0.60, [1, 1, 1, 1], "Q2", "S&M", "Inject 1 / D6"),
 ("Value-selling enablement (training, calculator, 1 value engineer)", 0.92, 0.60, 0.64, [1, 1, 1, 1], "Q2", "S&M", "Inject 1 / D3; win rate and discount"),
 ("Solutions engineers for paid pilots", 0.64, 0.68, 0.72, [1, 1, 1, 1], "Q2", "S&M", "Inject 1; proof-of-value (D1 driver)"),
 ("RevOps analysts (2) + forecasting tool", 1.00, 0.85, 0.90, [1, 1, 1, 1], "Q2", "S&M", "Inject 1 / D4"),
 ("Sensor-agnostic tier: launch readiness (no earlier than Q4 FY27)", 0.60, 0.00, 0.00, [1, 1, 1, 1], "Even", "R&D", "Inject 1; guardrail; cannibalisation plan in D8"),
 ("Helix-incumbent renewal protection (exec sponsors, MES pack)", 0.80, 0.85, 0.90, [1, 1, 1, 1], "Q2", "S&M", "Inject 1 / D5; churn"),
 ("RESERVE: Vajra retention plan (Inject 4)", 0.90, 0.00, 0.00, [1, 1, 1, 1], "H2", "S&M", "Inject 4 sheet; released at Q2 review (defensive, all scenarios)"),
 ("RESERVE: second retention squad for Helix-incumbent renewals", 1.60, 1.70, 1.80, [1, 1, 1, 0], "H2", "S&M", "Inject 1 option (payback 14.1 months); released only if Q2 triggers met"),
 ("RESERVE: restore SE pilot capacity cut in Inject 1", 0.32, 0.34, 0.36, [1, 1, 1, 0], "H2", "S&M", "Inject 1"),
 ("AGGRESSIVE ONLY: extra ₹3 cr items (demand generation for SEA/Gulf)", 1.20, 1.30, 1.40, [0, 0, 1, 0], "H2", "S&M", "Original ₹18 cr draft")]
ir = {}
r = 5
for lab, a, b, c, fl, ph, cat, src in INV:
    put(I, f"A{r}", lab)
    for col, v in zip("BCD", (a, b, c)): put(I, f"{col}{r}", v, BLUE, CR)
    for col, v in zip("EFGH", fl): put(I, f"{col}{r}", v, BLUE, N0)
    put(I, f"I{r}", ph, BLUE)
    for col, src_c in zip("JKL", "BCD"): put(I, f"{col}{r}", f"={src_c}{r}*INDEX(E{r}:H{r},Assumptions!$C$5)", BLK, CR)
    put(I, f"M{r}", src, SM); I[f"N{r}"] = cat
    for k_, col in enumerate("PQRS"):
        sh_ = (("0.5" if k_ >= 2 else "0") if ph == "H2" else (("1/3" if k_ >= 1 else "0") if ph == "Q2" else "0.25"))
        put(I, f"{col}{r}", f'=J{r}*{sh_}*IF(N{r}="S&M",1,0)', BLK, CR)
    r += 1
last_fixed = r - 1
for k_, col in enumerate("PQRS"): put(I, f"{col}4", f"Q{k_+1} FY27 S&M", HDR, fill=HF)
ir["ae"] = r; put(I, f"A{r}", "Net new AEs: pay and recruiting (from Capacity)", BOLD)
for y, col in enumerate("JKL"):
    qs = yq(y)
    # incremental AE cost = cumulative net new × 0.25 yr per quarter × cost + recruiting per net new hire
    put(I, f"{col}{r}", "=(" + "+".join(f"Capacity!{q}{CAP['cum']}*0.25" for q in qs) + f")*{GI('aecost')}*(1+{GI('infl')})^{y + 1}" + f"+SUM(Capacity!{qs[0]}5:Capacity!{qs[3]}5)*{GI('rec')}", GRN, CR)
put(I, f"M{r}", "Cumulative net new AEs × loaded cost (inflated) + ₹3.5 lakh per hire", SM); I[f"N{r}"] = "S&M"; I[f"I{r}"] = "Model"
r += 1; ir["ch"] = r; put(I, f"A{r}", "Channel foundation: VP Channel, partner managers, enablement, PRM (from Channel)", BOLD)
for y, col in enumerate("JKL"): put(I, f"{col}{r}", f"=Channel!{YC[y]}{hc['fix']}", GRN, CR)
put(I, f"M{r}", "D6; 3 channel roles in FY27 (cap 6)", SM); I[f"N{r}"] = "S&M"; I[f"I{r}"] = "Model"
r += 1; ir["tot"] = r; put(I, f"A{r}", "Total incremental investment", BOLD)
for col in "JKL": put(I, f"{col}{r}", f"=SUM({col}5:{col}{r - 1})", BOLD, CR)
r += 1; ir["env"] = r; put(I, f"A{r}", "FY27 envelope for the selected scenario"); put(I, f"J{r}", f"={ENVLIVE}", GRN, CR)
r += 1; ir["head"] = r; put(I, f"A{r}", "Headroom / (over) in FY27", BOLD); put(I, f"J{r}", f"=J{ir['env']}-J{ir['tot']}", BOLD, CR)
r += 1; ir["rnd"] = r; put(I, f"A{r}", "of which R&D (outside S&M)")
for col in "JKL": put(I, f"{col}{r}", f'=SUMIF($N$5:$N${ir["ch"]},"R&D",{col}5:{col}{ir["ch"]})', BLK, CR)
r += 1; ir["sm"] = r; put(I, f"A{r}", "of which S&M, excluding net new AE pay (already in S&M AE pay line)")
for col in "JKL": put(I, f"{col}{r}", f"={col}{ir['tot']}-{col}{ir['rnd']}-{col}{ir['ae']}", BLK, CR)
r += 2; put(I, f"A{r}", "PAYBACK OF THE INVESTMENT AGAINST DOING NOTHING", BOLD); r += 1
ir["cum"] = r; put(I, f"A{r}", "Cumulative incremental investment (₹ cr)")
put(I, f"J{r}", f"=J{ir['tot']}", BLK, CR); put(I, f"K{r}", f"=J{r}+K{ir['tot']}", BLK, CR); put(I, f"L{r}", f"=K{r}+L{ir['tot']}", BLK, CR)
r += 1; ir["incarr"] = r; put(I, f"A{r}", "Incremental ARR vs do-nothing, end of year (₹ cr)")
for y, col in enumerate("JKL"): put(I, f"{col}{r}", f"=ARR_bridge!{YC[y]}{ann['inc']}", GRN, CR)
r += 1; ir["pbk"] = r; put(I, f"A{r}", "Investment payback (months) = cumulative investment ÷ (incremental ARR × gross margin) × 12", BOLD)
for y, col in enumerate("JKL"): put(I, f"{col}{r}", f"=IF({col}{ir['incarr']}<=0,\"never\",{col}{ir['cum']}/({col}{ir['incarr']}*PnL!{YC[y]}{{GMPOST}})*12)", BOLD, N1)
r += 1; ir["inc2"] = r; put(I, f"A{r}", "Incremental ARR vs conservative counterfactual (FY26 rates held)")
for y, col in enumerate("JKL"): put(I, f"{col}{r}", f"=ARR_bridge!{YC[y]}{ab['close']}-Do_nothing!{L(3 + y)}14", GRN, CR)
r += 1; ir["pbk2"] = r; put(I, f"A{r}", "Investment payback vs conservative counterfactual (months)", BOLD)
for y, col in enumerate("JKL"): put(I, f"{col}{r}", f"=IF({col}{ir['inc2']}<=0,\"never\",{col}{ir['cum']}/({col}{ir['inc2']}*PnL!{YC[y]}{{GMPOST}})*12)", BOLD, N1)
put(I, f"M{ir['pbk']}", "Stops paying back when incremental ARR ≤ 0, or payback > 30 months (see Sensitivity break-even)", SM)
I.column_dimensions["N"].hidden = True

# ---------------------------------------------------------------- P&L
P = sh("PnL", [52, 11] + [9.5] * 15 + [55])
title(P, "Profit and loss, gross margin and CAC payback", "Partner margin is charged to gross margin for the 66% floor test (today it sits in S&M). CAC payback uses the board-pack definition (DR3).")
qhdr(P)
pl = {}
pls = [("avg", "Average ARR in quarter", C1), ("sub", "Subscription revenue", CR), ("hw", "Hardware revenue", CR), ("rev", "Total revenue", CR), ("swc", "Software cost of revenue", CR), ("hwc", "Hardware cost of revenue", CR),
       ("gpp", "Gross profit before partner margin", CR), ("gmpre", "Gross margin before partner margin", PCT), ("pm", "Partner margin", CR), ("gp", "Gross profit after partner margin", CR), ("gmpost", "Gross margin after partner margin", PCT),
       ("smo", "S&M: existing lines excl. AE pay (inflated)", CR), ("sma", "S&M: AE pay (all AEs)", CR), ("smi", "S&M: initiatives (excl. net new AE pay)", CR), ("sm", "Total S&M", CR),
       ("rnd", "R&D (incl. sensor-agnostic readiness)", CR), ("gna", "G&A", CR), ("ebitda", "EBITDA", CR), ("em", "EBITDA margin", PCT),
       ("cac", "CAC payback, margin-adjusted (months)", N1), ("smarr", "S&M as % of closing ARR (annualised)", PCT)]
for k, (key, lab, fmt) in enumerate(pls): pl[key] = 5 + k; put(P, f"A{5 + k}", lab, BOLD if key in ("rev", "gmpost", "sm", "ebitda", "cac") else BLK)
def ph(i, colI):  # FY27 H2-phased lines vs even, for investment rows
    return None
for i in range(12):
    c = QC[i]; y, k = divmod(i, 4); yc = "JKL"[y]
    put(P, f"{c}{pl['avg']}", f"=(ARR_bridge!{c}{ab['open']}+ARR_bridge!{c}{ab['close']})/2", BLK, C1)
    put(P, f"{c}{pl['sub']}", f"={c}{pl['avg']}*{GI('subr')}/4", BLK, CR)
    put(P, f"{c}{pl['hw']}", f"=(ARR_bridge!{c}{ab['dir']}+ARR_bridge!{c}{ab['par']}+ARR_bridge!{c}{ab['expn']})*" + interp("hwatt", i), BLK, CR)
    put(P, f"{c}{pl['rev']}", f"={c}{pl['sub']}+{c}{pl['hw']}", BOLD, CR)
    put(P, f"{c}{pl['swc']}", f"={c}{pl['sub']}*{GI('swc')}", BLK, CR)
    put(P, f"{c}{pl['hwc']}", f"={c}{pl['hw']}*{GI('hwc')}", BLK, CR)
    put(P, f"{c}{pl['gpp']}", f"={c}{pl['rev']}-{c}{pl['swc']}-{c}{pl['hwc']}", BLK, CR)
    put(P, f"{c}{pl['gmpre']}", f"={c}{pl['gpp']}/{c}{pl['rev']}", BLK, PCT)
    put(P, f"{c}{pl['pm']}", f"=Channel!{c}{hc['pmq']}", GRN, CR)
    put(P, f"{c}{pl['gp']}", f"={c}{pl['gpp']}-{c}{pl['pm']}", BLK, CR)
    put(P, f"{c}{pl['gmpost']}", f"={c}{pl['gp']}/{c}{pl['rev']}", BOLD, PCT)
    put(P, f"{c}{pl['smo']}", f"={GI('smoth')}/4*(1+{GI('infl')})^{y + 1}", BLK, CR)
    put(P, f"{c}{pl['sma']}", f"=Capacity!{c}{CAP['aey']}*{GI('aecost')}*(1+{GI('infl')})^{y + 1}", BLK, CR)
    if y == 0:
        smi = f"=SUM(Investment!{'PQRS'[k]}5:{'PQRS'[k]}{last_fixed})+Investment!$J${ir['ch']}/4"
    else:
        smi = f"=(Investment!{yc}{ir['sm']})/4"
    put(P, f"{c}{pl['smi']}", smi, BLK, CR)
    put(P, f"{c}{pl['sm']}", f"={c}{pl['smo']}+{c}{pl['sma']}+{c}{pl['smi']}", BOLD, CR)
    put(P, f"{c}{pl['rnd']}", f"={GI('rnd0')}/4*(1+{GI('rndg')})^{y + 1}+Investment!{yc}{ir['rnd']}/4", BLK, CR)
    put(P, f"{c}{pl['gna']}", f"={GI('gna0')}/4*(1+{GI('gnag')})^{y + 1}", BLK, CR)
    put(P, f"{c}{pl['ebitda']}", f"={c}{pl['gp']}-{c}{pl['sm']}-{c}{pl['rnd']}-{c}{pl['gna']}", BOLD, CR)
    put(P, f"{c}{pl['em']}", f"={c}{pl['ebitda']}/{c}{pl['rev']}", BLK, PCT)
    put(P, f"{c}{pl['cac']}", f"={c}{pl['sm']}/((ARR_bridge!{c}{ab['dir']}+ARR_bridge!{c}{ab['par']}+ARR_bridge!{c}{ab['expn']})*{c}{pl['gmpost']})*12", BOLD, N1)
    put(P, f"{c}{pl['smarr']}", f"={c}{pl['sm']}*4/ARR_bridge!{c}{ab['close']}", BLK, PCT)
for key in ("sub", "hw", "rev", "swc", "hwc", "gpp", "pm", "gp", "smo", "sma", "smi", "sm", "rnd", "gna", "ebitda"): ysum(P, pl[key], CR, BOLD if key in ("rev", "sm", "ebitda") else BLK)
ysum(P, pl["avg"], C1, BLK, "avg")
for y, col in enumerate(YC):
    put(P, f"{col}{pl['gmpre']}", f"={col}{pl['gpp']}/{col}{pl['rev']}", BLK, PCT); put(P, f"{col}{pl['gmpost']}", f"={col}{pl['gp']}/{col}{pl['rev']}", BOLD, PCT)
    put(P, f"{col}{pl['em']}", f"={col}{pl['ebitda']}/{col}{pl['rev']}", BLK, PCT)
    put(P, f"{col}{pl['cac']}", f"={col}{pl['sm']}/((ARR_bridge!{col}{ab['dir']}+ARR_bridge!{col}{ab['par']}+ARR_bridge!{col}{ab['expn']})*{col}{pl['gmpost']})*12", BOLD, N1)
    put(P, f"{col}{pl['smarr']}", f"={col}{pl['sm']}/ARR_bridge!{col}{ab['close']}", BOLD, PCT)
fy26 = {"rev": 388.52, "gmpost": "=(388.52-53.13-70.02)/388.52", "sm": 96.0, "ebitda": -23.31, "cac": "=96/((41+22)*0.683)*12", "smarr": "=96/310"}
for key, v in fy26.items(): put(P, f"B{pl[key]}", v, BLUE if not str(v).startswith("=") else BLK, PCT if key in ("gmpost", "smarr") else (N1 if key == "cac" else CR))
note(P, pl["cac"], "S&M ÷ ((new + expansion ARR) × GM) × 12 (DR3 definition). Cap 30 every quarter, 24 by Q4 FY28.")
note(P, pl["gmpost"], "Floor 66% every year incl. partner margin"); note(P, pl["smarr"], "FY26 31.0%; ≤ 30% by FY29")
note(P, pl["hw"], "Hardware attaches to new and expansion ARR (DR3 FY26 ratio); not in ARR")

# ---------------------------------------------------------------- INJECT 4
J = sh("Inject4", [62, 12, 12, 12, 12, 50])
title(J, "Inject 4: Vajra Auto Components (₹9.5 cr ARR) asks for a competitive re-tender against Helix", "Week 8. Renewal due Q4 FY27. Top-five customer (DR2 CU-1095).")
put(J, "A4", "ARR at stake (₹ cr)"); put(J, "C4", f"={GI('vaj')}", GRN, CR)
put(J, "A5", "Share of FY26 closing ARR"); put(J, "C5", "=C4/310", BLK, PCT)
put(J, "A6", "Probability of loss WITHOUT a retention plan"); put(J, "C6", 0.45, BLUE, PCT, YEL); put(J, "F6", "D5: Helix-incumbent re-tenders; HelixAsset free until 31 Mar 2027 (Inject 2); Helix bundle is the #1 churn driver (D1)", SM)
put(J, "A7", "Price concession if retained WITHOUT a plan"); put(J, "C7", 0.15, BLUE, PCT); put(J, "F7", "Reactive discounting at the D5 ceiling", SM)
put(J, "A8", "Probability of loss WITH the retention plan (selected scenario)"); put(J, "C8", f"={LIVE('vaj_p', 0)}", GRN, PCT)
put(J, "A9", "Price concession WITH the plan (selected scenario)"); put(J, "C9", f"={LIVE('vaj_c', 0)}", GRN, PCT)
put(J, "A10", "Cost of the retention plan, FY27 (₹ cr)"); put(J, "C10", f"=Investment!J{5 + [x[0] for x in INV].index('RESERVE: Vajra retention plan (Inject 4)')}", GRN, CR)
put(J, "A12", "Expected ARR lost WITHOUT plan (₹ cr)"); put(J, "C12", "=C4*C6+C4*(1-C6)*C7", BOLD, CR)
put(J, "A13", "Expected ARR lost WITH plan (₹ cr)"); put(J, "C13", "=C4*C8+C4*(1-C8)*C9", BOLD, CR)
put(J, "A14", "Used in ARR bridge, Q4 FY27 (₹ cr)", BOLD); put(J, "C14", "=C13", BOLD, CR)
put(J, "A15", "Expected ARR saved by the plan (₹ cr)"); put(J, "C15", "=C12-C13", BOLD, CR)
put(J, "A16", "Payback of the plan (months, margin-adjusted)"); put(J, "C16", "=C10/(C15*PnL!O{GMPOST})*12", BOLD, N1)
hdr(J, 18, ["Outcome", "Q4 FY27 ARR lost", "FY27 closing ARR", "FY27 NRR", "FY27 growth", "Reading"])
outs = [("Expected (plan, selected scenario)", "=C13"), ("Retained at plan concession", "=C4*C9"), ("Lost", "=C4"), ("Expected WITHOUT plan", "=C12")]
for k, (lab, f) in enumerate(outs):
    rr = 19 + k; put(J, f"A{rr}", lab); put(J, f"B{rr}", f, BLK, CR)
    put(J, f"C{rr}", f"=ARR_bridge!O{ab['close']}+ARR_bridge!O{ab['vaj']}-B{rr}", BLK, C1)
    put(J, f"D{rr}", f"=ARR_bridge!O{ann['nrr']}+(ARR_bridge!O{ab['vaj']}-B{rr})/ARR_bridge!O{ab['open']}", BLK, PCT)
    put(J, f"E{rr}", f"=C{rr}/ARR_bridge!O{ab['open']}-1", BLK, PCT)
put(J, "F21", "Losing Vajra costs ~3 pts of FY27 NRR on its own", SM)
put(J, "A24", "Forecast effect: Q4 FY27 net new ARR, expected vs retained vs lost (₹ cr)", BOLD)
put(J, "A25", "Q4 FY27 net ARR added (model, expected)"); put(J, "C25", f"=ARR_bridge!F{ab['close']}-ARR_bridge!F{ab['open']}", BLK, CR)
put(J, "A26", "If lost"); put(J, "C26", "=C25+C14-C4", BLK, CR); put(J, "A27", "If retained at plan concession"); put(J, "C27", "=C25+C14-C4*C9", BLK, CR)
put(J, "A29", "RETENTION PLAN", BOLD)
plan = ["Week 8–9: CEO and CRO meet Vajra's MD and CFO; agree re-tender scope and evaluation criteria before Helix sets them.",
        "Business review from Vajra's own usage data: assets monitored, failures caught, downtime avoided (D3 value model applied to their plants).",
        "Offer a 3-year renewal with price lock and a capped concession (8% base, within the D5 15% limit), plus expansion to the two plants not yet covered.",
        "MES integration pack and named executive sponsor (Helix-incumbent renewal protection line); dedicated CSM from the retention squad.",
        "Do not match 'free': HelixAsset is free only until 31 Mar 2027; show the three-year total cost and switching risk (D5 Helix battlecard).",
        "Triggers: exec meeting held by week 10; business review delivered by end-Q2; if Vajra shortlists Helix on price alone, escalate to CEO with the 3-year offer; decision expected Jan 2027."]
for k, t in enumerate(plan): put(J, f"A{30 + k}", f"{k + 1}. {t}", BLK, wrap=True); J.merge_cells(f"A{30 + k}:F{30 + k}"); J.row_dimensions[30 + k].height = 28

# ---------------------------------------------------------------- CHECKS
K = sh("Checks", [70, 16, 12, 50])
title(K, "Checks and guardrails", "Every guardrail in the brief. A failed test is disclosed with its fix in the memo, not hidden.")
hdr(K, 4, ["Check", "Value", "Result", "Threshold / note"])
ck = [
 ("ARR bridge ties every quarter (sum of absolute differences)", f"=SUMPRODUCT(ABS(ARR_bridge!C{ab['chk']}:N{ab['chk']}))", 'IF(B{r}<0.0001,"OK","ERROR")', "Opening + new + expansion − contraction − churn = closing", "0.000000"),
 ("No formula errors in model sheets", "=SUMPRODUCT(--ISERROR(Capacity!C5:Q40))+SUMPRODUCT(--ISERROR(Bookings!C5:Q30))+SUMPRODUCT(--ISERROR(ARR_bridge!C5:Q30))+SUMPRODUCT(--ISERROR(PnL!C5:Q30))+SUMPRODUCT(--ISERROR(Channel!O5:Q30))", 'IF(B{r}=0,"OK","ERROR")', "", N0),
 ("Total new logo = direct + partner (counted once)", f"=ABS(SUM(ARR_bridge!O{ann['nl']}:Q{ann['nl']})-SUM(Bookings!O{br['dir']}:Q{br['dir']})-SUM(Channel!O{hc['parr']}:Q{hc['parr']}))", 'IF(B{r}<0.0001,"OK","ERROR")', "No double counting", "0.000"),
 ("Investment within FY27 envelope", f"=Investment!J{ir['tot']}", 'IF(B{r}<=Investment!J' + str(ir['env']) + '+0.0001,"OK","OVER")', "₹15 cr (₹18 cr Aggressive)", CR),
 ("Gross margin after partner margin ≥ 66%, lowest year", f"=MIN(PnL!O{pl['gmpost']}:Q{pl['gmpost']})", f'IF(B{{r}}>={GI("gmf")},"OK","BREACH")', "Every year", PCT),
 ("CAC payback ≤ 30 months, worst quarter", f"=MAX(PnL!C{pl['cac']}:N{pl['cac']})", f'IF(B{{r}}<={GI("pb1")},"OK","BREACH")', "Every quarter", N1),
 ("CAC payback ≤ 24 months by Q4 FY28", f"=PnL!J{pl['cac']}", f'IF(B{{r}}<={GI("pb2")},"OK","BREACH")', "Q4 FY28", N1),
 ("S&M ≤ 30% of ARR by FY29", f"=PnL!Q{pl['smarr']}", f'IF(B{{r}}<={GI("smcap")},"OK","BREACH")', "FY26 31%", PCT),
 ("Net new AEs in FY27 ≤ 12", f"=Capacity!F{CAP['cum']}", f'IF(B{{r}}<={GI("aecap")},"OK","OVER")', "64 → 76 at most", N0),
 ("AE headcount end-FY27 ≤ 76", f"=Capacity!F{CAP['hc']}", 'IF(B{r}<=76.0001,"OK","OVER")', "", N1),
 ("New channel roles FY27 ≤ 6", "=3", f'IF(B{{r}}<={GI("chcap")},"OK","OVER")', "VP Channel + 2 partner managers (D6)", N0),
 ("Pipeline arithmetic: deals worked ≤ AE capacity every quarter", f"=SUMPRODUCT(--(Bookings!D{br['work']}:N{br['work']}>Bookings!D{br['cap']}:N{br['cap']}+0.0001))", 'IF(B{r}=0,"OK","ERROR")', "Required pipeline = bookings ÷ win rate (Bookings row 15)", N0),
 ("Pipeline arithmetic: deals worked ≤ pipeline supply every quarter", f"=SUMPRODUCT(--(Bookings!D{br['work']}:N{br['work']}>Bookings!D{br['sup']}:N{br['sup']}+0.0001))", 'IF(B{r}=0,"OK","ERROR")', "", N0),
 ("Partner pipeline required ≤ partner capacity, every year", f"=SUMPRODUCT(--(Channel!O{hc['preq']}:Q{hc['preq']}>Channel!O{hc['pcap']}:Q{hc['pcap']}+0.0001))", 'IF(B{r}=0,"OK","CHECK")', "", N0),
 ("Growth FY27 ≥ 15%", f"=ARR_bridge!O{ann['growth']}", f'IF(B{{r}}>={GI("g27")},"OK","SHORTFALL")', "Or defended shortfall (memo §4)", PCT),
 ("Growth FY28 ≥ 20%", f"=ARR_bridge!P{ann['growth']}", f'IF(B{{r}}>={GI("g28")},"OK","SHORTFALL")', "", PCT),
 ("Growth FY29 ≥ 22%", f"=ARR_bridge!Q{ann['growth']}", f'IF(B{{r}}>={GI("g29")},"OK","SHORTFALL")', "", PCT),
 ("FY29 NRR vs 108% goal", f"=ARR_bridge!Q{ann['nrr']}", f'IF(B{{r}}>={GI("nrrT")},"OK","SHORTFALL")', "", PCT),
 ("Partner share of new logo FY29 ≥ 25%", f"=Channel!Q{hc['share']}", 'IF(B{r}>=0.25,"OK","SHORTFALL")', "Board objective 5", PCT),
 ("D6 reconciliation: Base partner ARR FY27+FY28+FY29 = ₹33.27 cr", f"=SUM(Channel!O{hc['parr']}:Q{hc['parr']})", 'IF(Assumptions!$C$5<>1,"n/a",IF(ABS(B{r}-33.268)<0.01,"OK","DIFF"))', "Only tested in Base with shifts at 0", CR),
 ("Sensitivity shifts all zero (plan view)", f"=ABS(Assumptions!B{R['dwin']})+ABS(Assumptions!B{R['dcyc']})+ABS(Assumptions!B{R['ddisc']})+ABS(Assumptions!B{R['dpp']})+ABS(Assumptions!B{R['dchurn']})+ABS(1-Assumptions!B{R['ddel']})", 'IF(B{r}=0,"OK","SHIFTED")', "Reminder when flexing", "0.00"),
]
for k, (lab, f, res, th, fmt) in enumerate(ck):
    r = 5 + k; put(K, f"A{r}", lab); put(K, f"B{r}", f, BLK, fmt); put(K, f"C{r}", "=" + res.replace("{r}", str(r)), BOLD); put(K, f"D{r}", th, SM)
put(K, f"A{6 + len(ck)}", "Count of failed guardrails (ERROR / OVER / BREACH)", BOLD)
put(K, f"C{6 + len(ck)}", f'=COUNTIF(C5:C{4 + len(ck)},"ERROR")+COUNTIF(C5:C{4 + len(ck)},"OVER")+COUNTIF(C5:C{4 + len(ck)},"BREACH")', BOLD, N0)
put(K, f"A{7 + len(ck)}", "Count of shortfalls against board goals (disclosed and defended)", BOLD)
put(K, f"C{7 + len(ck)}", f'=COUNTIF(C5:C{4 + len(ck)},"SHORTFALL")', BOLD, N0)

# ---------------------------------------------------------------- CASCADE
X = sh("Cascade", [58, 16, 14, 14, 14, 14, 44]); X.freeze_panes = "B5"
title(X, "Cascade test: change the win rate by 3 points and every number that moves", "Set Assumptions!B" + str(R["dwin"]) + " to 3. 'Live' recalculates; 'Base (saved)' and '+3 pts (saved)' are values from run_scenarios.py for reference.")
hdr(X, 4, ["Metric", "Where it shows", "Base (saved)", "+3 pts (saved)", "Live", "Live − Base", "Why it moves"])
CASC = [
 ("AE deal capacity FY27 (qualified deals)", "D2 capacity", f"=Bookings!O{br['cap']}", "Does not move: capacity is AEs × deals carried ÷ cycle"),
 ("Qualified deals worked FY27", "D2 capacity", f"=Bookings!O{br['work']}", "Does not move"),
 ("Deals won FY27", "D2 / D4", f"=Bookings!O{br['wins']}", "More of the same deals close"),
 ("Direct new-logo ARR FY27 (₹ cr)", "D4 forecast", f"=Bookings!O{br['dir']}", "Q2–Q4 move; Q1 is the locked forecast"),
 ("Direct new-logo ARR Q2 FY27 (₹ cr)", "D4 next-quarter forecast", f"=Bookings!D{br['dir']}", ""),
 ("Pipeline required FY27 (₹ cr)", "D4 coverage", f"=Bookings!O{br['pipe']}", "Required pipeline = bookings ÷ win rate"),
 ("Board path FY27: capacity surplus / (gap), deals", "D2 account plan capacity", f"=Bookings!O{bp['gap']}", "Fewer deals needed at a higher win rate"),
 ("Board path FY27: extra ramped AEs needed", "D2 / Inject 1 hiring", f"=Bookings!O{bp['aes']}", ""),
 ("Board path FY28: capacity surplus / (gap), deals", "D2 account plan capacity", f"=Bookings!P{bp['gap']}", ""),
 ("Partner-sourced ARR FY27 (₹ cr)", "D6 channel", f"=Channel!O{hc['parr']}", "Partner win rate 34% → 37% scales partner productivity"),
 ("Partner-sourced ARR FY29 (₹ cr)", "D6 channel", f"=Channel!Q{hc['parr']}", ""),
 ("Partner share of new logo FY29", "D6 / board objective 5", f"=Channel!Q{hc['share']}", "Both numerator and denominator rise"),
 ("Channel saving vs direct FY29 (₹ cr)", "D6 channel P&L", f"=Channel!Q{hc['net']}", ""),
 ("Partner pipeline required FY29 (₹ cr)", "D6 channel", f"=Channel!Q{hc['preq']}", ""),
 ("Total new-logo ARR FY29 (₹ cr)", "D7 bridge", f"=ARR_bridge!Q{ann['nl']}", ""),
 ("Closing ARR FY27 (₹ cr)", "D7 bridge", f"=ARR_bridge!O{ab['close']}", ""),
 ("Closing ARR FY28 (₹ cr)", "D7 bridge", f"=ARR_bridge!P{ab['close']}", ""),
 ("Closing ARR FY29 (₹ cr)", "D7 bridge / D8", f"=ARR_bridge!Q{ab['close']}", "Also compounds: more customers expand and renew"),
 ("Growth FY27", "Growth guardrail", f"=ARR_bridge!O{ann['growth']}", ""),
 ("Growth FY29", "Growth guardrail", f"=ARR_bridge!Q{ann['growth']}", ""),
 ("Closing ARR FY29 vs board path (₹ cr)", "D8", f"=ARR_bridge!Q{ann['gapb']}", ""),
 ("NRR FY29", "Retention", f"=ARR_bridge!Q{ann['nrr']}", "Does not move: win rate affects new logos only"),
 ("Revenue FY29 (₹ cr)", "P&L", f"=PnL!Q{pl['rev']}", "Subscription and hardware both rise"),
 ("Gross margin after partner margin FY29", "GM guardrail", f"=PnL!Q{pl['gmpost']}", "More hardware (25% margin) dilutes GM slightly"),
 ("EBITDA FY27 (₹ cr)", "P&L", f"=PnL!O{pl['ebitda']}", ""),
 ("EBITDA FY29 (₹ cr)", "P&L", f"=PnL!Q{pl['ebitda']}", ""),
 ("CAC payback, worst quarter (months)", "Payback guardrail", f"=MAX(PnL!C{pl['cac']}:N{pl['cac']})", "Q1 FY27 is locked, so the worst quarter barely moves"),
 ("CAC payback Q4 FY28 (months)", "Payback guardrail", f"=PnL!J{pl['cac']}", ""),
 ("S&M as % of ARR FY29", "S&M guardrail", f"=PnL!Q{pl['smarr']}", ""),
 ("Investment payback vs do-nothing, FY29 (months)", "Inject 1 / D8", f"=Investment!L{ir['pbk']}", ""),
]
for k, (lab, where, f, why) in enumerate(CASC):
    rr = 5 + k; fmt = PCT if ("share" in lab or "Growth" in lab or "NRR" in lab or "margin" in lab or "%" in lab) else CR
    put(X, f"A{rr}", lab); put(X, f"B{rr}", where, SM); put(X, f"E{rr}", f, GRN, fmt); put(X, f"F{rr}", f"=IF(ISNUMBER(C{rr}),E{rr}-C{rr},\"\")", BOLD, fmt)
    X[f"C{rr}"].number_format = fmt; X[f"D{rr}"].number_format = fmt; put(X, f"G{rr}", why, SM)
json_casc = [c[0] for c in CASC]

# ---------------------------------------------------------------- resolve placeholders
subs = {"{EX}": str(CAP["ex"]), "{PQ}": str(hc.get("pq", 28)), "{BOARD}": str(ann["board"]), "{OPEN}": str(ab["open"]), "{EXPN}": str(ab["expn"]), "{CONT}": str(ab["cont"]),
        "{CHRN}": str(ab["chrn"]), "{VAJ}": str(ab["vaj"]), "{GMPRE}": str(pl["gmpre"]), "{GMPOST}": str(pl["gmpost"])}
for w in wb.worksheets:
    for row in w.iter_rows():
        for c in row:
            if isinstance(c.value, str) and "{" in c.value and c.value.startswith("="):
                v = c.value
                for a_, b_ in subs.items(): v = v.replace(a_, b_)
                c.value = v
# partner Q in Channel row 'pq' for annual (used in Bookings board-path)
for y, col in enumerate(YC): put(H, f"{col}28", f"=SUM({yq(y)[0]}28:{yq(y)[3]}28)", BOLD, CR)
wb.save(OUT)
import json; json.dump(dict(casc=json_casc, R=R, CAP={str(k): v for k, v in CAP.items()}, br=br, bp=bp, hc=hc, ab=ab, ann=ann, pl=pl, ir=ir), open("out/rowmap.json", "w"))
print("saved", OUT)
