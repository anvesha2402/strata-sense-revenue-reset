"""D2 tiering & coverage workbook (formulas; blue = inputs)."""
import pandas as pd, numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
t = pd.read_pickle("out/targets_tiered.pkl"); S = pd.read_pickle("out/score.pkl"); C = pd.read_pickle("out/capacity.pkl")
BLUE = Font(name="Arial", size=10, color="0000FF"); BLK = Font(name="Arial", size=10); BOLD = Font(name="Arial", size=10, bold=True)
GRN = Font(name="Arial", size=10, color="008000"); HDR = Font(name="Arial", size=10, bold=True, color="FFFFFF")
HFILL = PatternFill("solid", fgColor="1F3A5F"); YEL = PatternFill("solid", fgColor="FFFF00"); SUB = PatternFill("solid", fgColor="E8EEF5")
wb = Workbook()
def sheet(name, widths):
    ws = wb.create_sheet(name)
    for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
    return ws
def hdr(ws, row, vals):
    for j, v in enumerate(vals, 1):
        c = ws.cell(row, j, v); c.font = HDR; c.fill = HFILL; c.alignment = Alignment(wrap_text=True, vertical="top")
def put(ws, ref, v, font=BLK, fmt=None, fill=None):
    c = ws[ref]; c.value = v; c.font = font
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    return c
def title(ws, t, sub=None):
    put(ws, "A1", t, Font(name="Arial", size=13, bold=True, color="1F3A5F"))
    if sub: put(ws, "A2", sub, Font(name="Arial", size=9, italic=True, color="52514E"))
PCT = "0.0%;(0.0%);-"; CR = "#,##0.0;(#,##0.0);-"; CR2 = "#,##0.00;(#,##0.00);-"; INT = "#,##0;(#,##0);-"; LK = "#,##0.0"
# ---------------- README
ws = wb.active; ws.title = "README"; ws.column_dimensions["A"].width = 26; ws.column_dimensions["B"].width = 110
rows = [("D2 TIERING & COVERAGE WORKBOOK", ""), ("Company", "Strata Sense Technologies is fictional; all data synthetic (MBA capstone)."),
 ("Colour code", "Blue text = input you can change. Black = formula. Green = link to another sheet. Yellow fill = key assumption to validate."),
 ("How to use", "Change inputs on 'Inputs' (target, NRR, tier win rates, threading target, AE scenario, source mix, budget). Coverage, Funnel, Budget and Checks update."),
 ("Cascade test", "Change the tier win rates on Inputs by 3 points: capacity, required opportunities, leads and programme cost all move on Coverage and Funnel."),
 ("Sources", "DR1 CRM (cleaned in D1), DR2 targets and customers, DR3 finance pack (AE roster, marketing programmes). Productivity by tenure from D1 (DR3 ae_quarterly)."),
 ("Score", "EV = P(win | qualified) × expected first-year ARR. P(win): firmographic logit trained on FY24–FY25 deals. Expected ARR: log-linear model on won deals (R² 0.51). Condition-monitoring field excluded from the score (it is blank for every account that became a customer, so it would leak the outcome)."),
 ("Tiers", "1 Strategic = top 400 by EV (Helix-incumbent capped at the 40 highest-EV; the other 85 held in Scaled until a pricing decision). 2 Scaled = next 1,100. 3 Low-touch = remaining 1,600 (SDR, inside sales, marketing nurture; SEA via partners)."),
 ("SHEETS", ""), ("Inputs", "All assumptions"), ("Coverage", "Capacity vs target, AEs by tier, accounts per AE"), ("Funnel", "Target → won deals → qualified opps → opps → leads by source; programme cost"),
 ("Budget", "Rs 24 cr programme budget: FY26 vs FY27 proposal"), ("Backtest", "Does the score predict past wins?"), ("Tiering", "The 3,100 accounts with score, tier and play"), ("Checks", "Integrity checks")]
for i, (a, b) in enumerate(rows, 1):
    ws.cell(i, 1, a).font = BOLD if a.isupper() or i == 1 else BLK; ws.cell(i, 2, b).font = BLK; ws.cell(i, 2).alignment = Alignment(wrap_text=True, vertical="top")
# ---------------- Tiering (values)
tg = sheet("Tiering", [10, 34, 22, 11, 16, 8, 11, 18, 22, 9, 11, 10, 8, 12, 32, 9, 10, 9, 9, 9])
cols = ["account_id", "account_name", "segment", "region", "revenue_band", "plant_count", "installed_rotating_assets_est", "incumbent_automation_vendor",
        "existing_condition_monitoring", "fit_score", "exp_arr_lakh", "ev_lakh", "ev_rank", "tier", "play", "need_signal", "assigned_ae_id", "ae_touches_fy26", "distinct_contacts_engaged_fy26", "open_opportunity"]
hdr(tg, 1, ["account_id", "account_name", "segment", "region", "revenue_band", "plants", "installed assets (est)", "incumbent automation", "existing condition monitoring",
            "P(win|qualified)", "expected 1st-yr ARR (lakh)", "EV (lakh)", "EV rank", "tier", "play", "need signal", "assigned AE", "AE touches FY26", "contacts FY26", "open opp"])
tt = t.sort_values("ev_rank")[cols]
for i, r in enumerate(tt.itertuples(index=False), 2):
    for j, v in enumerate(r, 1):
        c = tg.cell(i, j, v.item() if hasattr(v, "item") else v); c.font = BLK
    tg.cell(i, 10).number_format = "0.000"; tg.cell(i, 11).number_format = LK; tg.cell(i, 12).number_format = LK
tg.freeze_panes = "C2"; tg.auto_filter.ref = f"A1:T{len(tt)+1}"
NT = len(tt) + 1
# ---------------- Inputs
I = sheet("Inputs", [46, 13, 13, 13, 13, 13, 13, 13, 60]); title(I, "Inputs", "Blue = change me. Yellow = key assumption to validate in interviews / D7.")
def inp(r, label, v, fmt, src, key=False):
    put(I, f"A{r}", label); put(I, f"B{r}", v, BLUE, fmt, YEL if key else None); put(I, f"I{r}", src, Font(name="Arial", size=9, color="52514E"))
put(I, "A4", "TARGET", BOLD)
inp(5, "FY26 closing ARR (Rs cr)", 310, CR, "DR3 pl_quarterly")
inp(6, "FY27 ARR growth target", 0.15, PCT, "Board ask (brief s.2)")
inp(7, "FY27 net revenue retention assumption", 1.00, PCT, "Provisional: FY26 actual 98.9%; retention plan must lift it to 100%. Reconcile in D7.", True)
put(I, "A8", "FY27 new-logo ARR needed (Rs cr)"); put(I, "B8", "=B5*(1+B6)-B5*B7", BLK, CR2)
inp(9, "Partner-sourced new-logo ARR, SEA-led (Rs cr)", 4.0, CR2, "FY26 adj. 2.6 cr (D1); SEA partner deals win 34% vs 10% direct", True)
put(I, "A10", "Direct new-logo ARR needed (Rs cr)"); put(I, "B10", "=B8-B9", BLK, CR2)
put(I, "A12", "TIERS", BOLD)
I.column_dimensions["J"].width = 13
c = I.cell(13, 10, "FY26 AE effort weight"); c.font = HDR; c.fill = HFILL; c.alignment = Alignment(wrap_text=True)
for j, h in enumerate(["Tier", "Accounts", "FY26 win rate", "FY26 avg won deal (lakh)", "Plan AE effort weight", "FY26 share of qual. opps", "Plan share of qual. opps", "3+ contact share FY26"], 1):
    c = I.cell(13, j, h); c.font = HDR; c.fill = HFILL; c.alignment = Alignment(wrap_text=True)
tiers = [("1 Strategic", 0.259, 82.24, 2.0, 0.1875, 0.35, 0.185), ("2 Scaled", 0.196, 59.64, 1.0, 0.3426, 0.45, 0.149), ("3 Low-touch", 0.113, 27.97, 0.3, 0.4699, 0.20, 0.241)]
for k, (nm, wr, dl, ef, s26, sp, t3) in enumerate(tiers):
    r = 14 + k
    put(I, f"A{r}", nm); put(I, f"B{r}", f'=COUNTIF(Tiering!$N$2:$N${NT},A{r})', GRN, INT)
    put(I, f"C{r}", wr, BLUE, PCT); put(I, f"D{r}", dl, BLUE, LK); put(I, f"E{r}", ef, BLUE, "0.0", YEL); put(I, f"F{r}", s26, BLUE, PCT); put(I, f"G{r}", sp, BLUE, PCT, YEL); put(I, f"H{r}", t3, BLUE, PCT); put(I, f"J{r}", 1.0, BLUE, "0.0")
put(I, "I14", "Win rate, deal and shares: FY26 qualified closed deals scored with the D2 tiers. Effort weights = AE time per opp vs a scaled opp (assumption). FY26: every account AE-owned, no tiering, so equal effort. Plan: strategic deals get deeper work (2.0); low-touch moves to SDR / inside sales / partners (0.3 AE effort). Plan share = target mix after re-tiering.", Font(name="Arial", size=9, color="52514E"))
I["I14"].alignment = Alignment(wrap_text=True, vertical="top")
put(I, "A18", "Total"); put(I, "B18", "=SUM(B14:B16)", BLK, INT); put(I, "F18", "=SUM(F14:F16)", BLK, PCT); put(I, "G18", "=SUM(G14:G16)", BLK, PCT)
put(I, "A20", "MULTI-THREADING (win-rate lift)", BOLD)
for j, h in enumerate(["Tier", "Win 3+ contacts", "Win <3 contacts", "Target 3+ share", "Realisation", "Win-rate uplift (pts)"], 1):
    c = I.cell(21, j, h); c.font = HDR; c.fill = HFILL; c.alignment = Alignment(wrap_text=True)
thr = [("1 Strategic", 0.500, 0.291, 0.50), ("2 Scaled", 0.295, 0.186, 0.35), ("3 Low-touch", 0.186, 0.103, 0.24)]
for k, (nm, w3, wl, tgt) in enumerate(thr):
    r = 22 + k
    put(I, f"A{r}", nm); put(I, f"B{r}", w3, BLUE, PCT); put(I, f"C{r}", wl, BLUE, PCT); put(I, f"D{r}", tgt, BLUE, PCT, YEL); put(I, f"E{r}", 0.5, BLUE, PCT, YEL)
    put(I, f"F{r}", f"=MAX(0,(D{r}-H{14+k}))*(B{r}-C{r})*E{r}", BLK, PCT)
put(I, "I22", "FY24–26 qualified deals by tier. Realisation 50%: part of the 3+ contact advantage is selection (good deals attract more contacts), not cause.", Font(name="Arial", size=9, color="52514E")); I["I22"].alignment = Alignment(wrap_text=True, vertical="top")
put(I, "A26", "AE SUPPLY FY27 (AE-years by tenure band)", BOLD)
for j, h in enumerate(["Tenure band", "Productivity (Rs cr / AE-yr)", "Scenario A: hold 64", "Scenario B: 76 (+12 in H1)"], 1):
    c = I.cell(27, j, h); c.font = HDR; c.fill = HFILL; c.alignment = Alignment(wrap_text=True)
for k, b in enumerate(["0-6", "6-12", "12-24", "24+"]):
    r = 28 + k
    put(I, f"A{r}", f"{b} months"); put(I, f"B{r}", C["PROD"][b], BLUE, CR2)
    put(I, f"C{r}", round(C["A"][f"ae_years_{b}"].sum(), 2), BLUE, CR2); put(I, f"D{r}", round(C["B"][f"ae_years_{b}"].sum(), 2), BLUE, CR2)
put(I, "A32", "Total AE-years"); put(I, "C32", "=SUM(C28:C31)", BLK, CR2); put(I, "D32", "=SUM(D28:D31)", BLK, CR2)
put(I, "I28", "Productivity: DR3 ae_quarterly FY24–26 (D1). Supply: cohort model from DR3 roster, 29% annual attrition skewed to 6–20 months, leavers backfilled at quarter end.", Font(name="Arial", size=9, color="52514E")); I["I28"].alignment = Alignment(wrap_text=True, vertical="top")
inp(33, "AE scenario (A or B)", "A", None, "B adds 12 AEs; ramp means little FY27 capacity", True)
dv = DataValidation(type="list", formula1='"A,B"', allow_blank=False); I.add_data_validation(dv); dv.add("B33")
inp(34, "Loaded cost per AE (Rs cr / yr)", 0.50, CR2, "DR3 unit_costs (India ~Rs 50 lakh)")
inp(35, "Share of FY27 bookings from pipeline created after re-tiering", 0.40, PCT, "8-month cycle: most H1 FY27 bookings come from pipeline already created. Full effect from FY28.", True)
put(I, "A36", "COVERAGE RATIOS", BOLD)
inp(37, "Strategic accounts per AE", 14, INT, "Assumption: named accounts with written plans; validate with RevOps interviews", True)
inp(38, "Scaled accounts per AE", 50, INT, "Assumption: territory accounts with SDR support", True)
inp(39, "Inside-sales AEs for low-touch pool", 4, INT, "Low-touch: SDR + inside AEs + marketing nurture; SEA via partners")
inp(40, "AEs in first 6 months (not given named accounts)", 9, INT, "DR3 roster: 9 AEs under 6 months at 31 Mar 2026")
put(I, "A42", "LEAD SOURCES (qualified opportunities)", BOLD)
for j, h in enumerate(["Source", "Plan mix of qual. opps", "Opp → qualified", "Lead → opp", "FY26 programme spend (Rs cr)", "FY26 qual. opps created", "Cost per qual. opp (lakh)"], 1):
    c = I.cell(43, j, h); c.font = HDR; c.fill = HFILL; c.alignment = Alignment(wrap_text=True)
src = [("ABM (strategic tier)", 0.12, 0.70, 0.25, 0.0, 0, 10.0), ("SDR / digital / outbound", 0.40, 0.67, 0.15, 11.48, 160, None),
       ("Events", 0.03, 0.70, 0.10, 9.6, 26, None), ("Customer referral", 0.10, 0.66, 0.50, 1.2, 29, None),
       ("AE self-sourced", 0.25, 0.68, 1.00, 0.0, 96, 0.0), ("Partner-sourced", 0.10, 0.58, 0.40, 0.6, 33, None)]
for k, (nm, mix, oq, lo, sp, n, cpo) in enumerate(src):
    r = 44 + k
    put(I, f"A{r}", nm); put(I, f"B{r}", mix, BLUE, PCT, YEL); put(I, f"C{r}", oq, BLUE, PCT); put(I, f"D{r}", lo, BLUE, PCT, YEL)
    put(I, f"E{r}", sp, BLUE, CR2); put(I, f"F{r}", n, BLUE, INT)
    if cpo is None: put(I, f"G{r}", f"=IF(F{r}>0,E{r}*100/F{r},0)", BLK, LK)
    else: put(I, f"G{r}", cpo, BLUE, LK, YEL)
put(I, "A50", "Total"); put(I, "B50", "=SUM(B44:B49)", BLK, PCT)
put(I, "I44", "Opp → qualified: DR1 FY26 created opps by source. Lead → opp: assumption (MQL data not in CRM). SDR spend = digital 5.3 + outbound tools 3.1 + SDR pay 3.08. ABM cost per opp: assumption.", Font(name="Arial", size=9, color="52514E")); I["I44"].alignment = Alignment(wrap_text=True, vertical="top")
I.freeze_panes = "A4"
# ---------------- Coverage
Cv = sheet("Coverage", [52, 15, 15, 15, 15, 50]); title(Cv, "Coverage and capacity", "Can 64–76 AEs deliver the direct target?")
put(Cv, "A4", "CAPACITY", BOLD)
put(Cv, "A5", "Direct new-logo ARR needed (Rs cr)"); put(Cv, "B5", "=Inputs!B10", GRN, CR2)
put(Cv, "A6", "Baseline capacity at FY26 productivity (Rs cr)"); put(Cv, "B6", '=IF(Inputs!B33="B",SUMPRODUCT(Inputs!B28:B31,Inputs!D28:D31),SUMPRODUCT(Inputs!B28:B31,Inputs!C28:C31))', BLK, CR2)
put(Cv, "A7", "ARR per effort unit, FY26 mix (lakh)"); put(Cv, "B7", "=SUMPRODUCT(Inputs!F14:F16,Inputs!C14:C16,Inputs!D14:D16)/SUMPRODUCT(Inputs!F14:F16,Inputs!J14:J16)", BLK, LK)
put(Cv, "A8", "Plan win rate: Strategic / Scaled / Low-touch"); put(Cv, "B8", "=Inputs!C14+Inputs!F22", BLK, PCT); put(Cv, "C8", "=Inputs!C15+Inputs!F23", BLK, PCT); put(Cv, "D8", "=Inputs!C16+Inputs!F24", BLK, PCT)
put(Cv, "A9", "ARR per effort unit, plan mix + threading (lakh)"); put(Cv, "B9", "=(Inputs!G14*B8*Inputs!D14+Inputs!G15*C8*Inputs!D15+Inputs!G16*D8*Inputs!D16)/SUMPRODUCT(Inputs!G14:G16,Inputs!E14:E16)", BLK, LK)
put(Cv, "A10", "Productivity multiplier, full year (FY28 run-rate)"); put(Cv, "B10", "=B9/B7", BLK, "0.00x")
put(Cv, "A11", "  of which re-tiering only"); put(Cv, "B11", "=(SUMPRODUCT(Inputs!G14:G16,Inputs!C14:C16,Inputs!D14:D16)/SUMPRODUCT(Inputs!G14:G16,Inputs!E14:E16))/B7", BLK, "0.00x")
put(Cv, "A12", "Direct capacity with plan, FY27 (Rs cr)"); put(Cv, "B12", "=B6*(1+(B10-1)*Inputs!B35)", BLK, CR2)
put(Cv, "C12", "=B6*B10", BLK, CR2); put(Cv, "D12", "← FY28 run-rate at same AE supply", Font(name="Arial", size=9, color="52514E"))
put(Cv, "A13", "Surplus / (gap) vs direct need (Rs cr)", BOLD); put(Cv, "B13", "=B12-B5", BOLD, CR2)
put(Cv, "A15", "CAPACITY BRIDGE (Rs cr)", BOLD)
put(Cv, "A16", "Baseline (FY26 productivity, chosen AE scenario)"); put(Cv, "B16", "=B6", BLK, CR2)
put(Cv, "A17", "+ Re-tiering (effort to higher-EV accounts)"); put(Cv, "B17", "=B6*(B11-1)*Inputs!B35", BLK, CR2)
put(Cv, "A18", "+ Multi-threading lift"); put(Cv, "B18", "=B12-B6-B17", BLK, CR2)
put(Cv, "A19", "Direct capacity (subtotal)"); put(Cv, "B19", "=SUM(B16:B18)", BOLD, CR2)
put(Cv, "A20", "+ Partner-sourced (SEA-led)"); put(Cv, "B20", "=Inputs!B9", GRN, CR2)
put(Cv, "A21", "Total new-logo capacity"); put(Cv, "B21", "=B19+B20", BOLD, CR2)
put(Cv, "A22", "New-logo ARR needed"); put(Cv, "B22", "=Inputs!B8", GRN, CR2)
put(Cv, "A24", "AE ALLOCATION", BOLD)
for j, h in enumerate(["Tier", "Accounts", "Accounts per AE", "AEs needed", "Note"], 1):
    c = Cv.cell(25, j, h); c.font = HDR; c.fill = HFILL
put(Cv, "A26", "1 Strategic"); put(Cv, "B26", "=Inputs!B14", GRN, INT); put(Cv, "C26", "=Inputs!B37", GRN, INT); put(Cv, "D26", "=ROUNDUP(B26/C26,0)", BLK, INT); put(Cv, "E26", "Named; written account plan; ≥4 contacts")
put(Cv, "A27", "2 Scaled"); put(Cv, "B27", "=Inputs!B15", GRN, INT); put(Cv, "C27", "=Inputs!B38", GRN, INT); put(Cv, "D27", "=ROUNDUP(B27/C27,0)", BLK, INT); put(Cv, "E27", "Territory; SDR-supported")
put(Cv, "A28", "3 Low-touch (inside pool)"); put(Cv, "B28", "=Inputs!B16", GRN, INT); put(Cv, "C28", "=IF(D28>0,B28/D28,0)", BLK, INT); put(Cv, "D28", "=Inputs!B39", GRN, INT); put(Cv, "E28", "No named AE; SDR + nurture; SEA via partners")
put(Cv, "A29", "Ramping AEs (first 6 months)"); put(Cv, "D29", "=Inputs!B40", GRN, INT); put(Cv, "E29", "Shadow strategic AEs; own Scaled overflow")
put(Cv, "A30", "AEs needed"); put(Cv, "D30", "=SUM(D26:D29)", BOLD, INT)
put(Cv, "A31", "AEs available (64, or 76 in scenario B)"); put(Cv, "D31", '=IF(Inputs!B33="B",76,64)', BLK, INT)
put(Cv, "A32", "Spare / (short) AEs"); put(Cv, "D32", "=D31-D30", BOLD, INT)
put(Cv, "A34", "OPPORTUNITIES NEEDED FOR DIRECT TARGET", BOLD)
for j, h in enumerate(["Tier", "Share of direct bookings", "Bookings (Rs cr)", "Won deals", "Qualified opps", "Per account per year"], 1):
    c = Cv.cell(35, j, h); c.font = HDR; c.fill = HFILL; c.alignment = Alignment(wrap_text=True)
for k, (nm, wc) in enumerate([("1 Strategic", "B8"), ("2 Scaled", "C8"), ("3 Low-touch", "D8")]):
    r = 36 + k; ir = 14 + k
    put(Cv, f"A{r}", nm)
    put(Cv, f"B{r}", f"=Inputs!G{ir}*{wc}*Inputs!D{ir}/(Inputs!G14*$B$8*Inputs!D14+Inputs!G15*$C$8*Inputs!D15+Inputs!G16*$D$8*Inputs!D16)", BLK, PCT)
    put(Cv, f"C{r}", f"=B{r}*$B$5", BLK, CR2); put(Cv, f"D{r}", f"=C{r}*100/Inputs!D{ir}", BLK, "0.0")
    put(Cv, f"E{r}", f"=D{r}/{wc}", BLK, "0"); put(Cv, f"F{r}", f"=E{r}/Inputs!B{ir}", BLK, "0.00")
put(Cv, "A39", "Total"); put(Cv, "C39", "=SUM(C36:C38)", BOLD, CR2); put(Cv, "D39", "=SUM(D36:D38)", BOLD, "0.0"); put(Cv, "E39", "=SUM(E36:E38)", BOLD, "0")
put(Cv, "A40", "FY26 actual qualified closed deals (reference)"); put(Cv, "E40", 432, BLUE, "0")
Cv["F41"] = "Strategic-tier accounts generated 81 qualified deals in FY26 (0.2 per account). The plan needs roughly double: that is what ABM, account plans and SDR focus must deliver."
Cv["F41"].font = Font(name="Arial", size=9, color="52514E"); Cv["F41"].alignment = Alignment(wrap_text=True, vertical="top")
# ---------------- Funnel
Fn = sheet("Funnel", [30, 14, 14, 14, 14, 14, 14, 16]); title(Fn, "Lead-generation funnel", "Qualified opps needed (direct + partner) → opps → leads → programme cost")
put(Fn, "A4", "Qualified opps needed, direct (Coverage)"); put(Fn, "B4", "=Coverage!E39", GRN, "0")
put(Fn, "A5", "Partner-sourced qualified opps needed"); put(Fn, "B5", "=Inputs!B9*100/(0.34*Inputs!D14*0.6+0.34*Inputs!D15*0.4)", BLK, "0")
put(Fn, "C5", "partner deals: 34% win (SEA), deal size weighted 60/40 strategic/scaled", Font(name="Arial", size=9, color="52514E"))
put(Fn, "A6", "Total qualified opps needed", BOLD); put(Fn, "B6", "=B4+B5", BOLD, "0")
for j, h in enumerate(["Source", "Qualified opps", "Opps created", "Leads needed", "Cost per qual. opp (lakh)", "Cost (Rs cr)", "Budget available (Rs cr)", "Headroom (Rs cr)"], 1):
    c = Fn.cell(8, j, h); c.font = HDR; c.fill = HFILL; c.alignment = Alignment(wrap_text=True)
for k in range(6):
    r = 9 + k; ir = 44 + k
    put(Fn, f"A{r}", f"=Inputs!A{ir}", GRN)
    put(Fn, f"B{r}", f"=IF(Inputs!A{ir}=\"Partner-sourced\",$B$5,$B$4*Inputs!B{ir}/(1-Inputs!B49))", BLK, "0")
    put(Fn, f"C{r}", f"=B{r}/Inputs!C{ir}", BLK, "0"); put(Fn, f"D{r}", f"=C{r}/Inputs!D{ir}", BLK, "0")
    put(Fn, f"E{r}", f"=Inputs!G{ir}", GRN, LK); put(Fn, f"F{r}", f"=B{r}*E{r}/100", BLK, CR2)
    put(Fn, f"G{r}", ["=Budget!C5", "=Budget!C6+Budget!C7+3.08", "=Budget!C4", "=Budget!C8", "=0", "=Budget!C9+0.15*Inputs!B9"][k], GRN, CR2)
    put(Fn, f"H{r}", f"=G{r}-F{r}", BLK, CR2)
put(Fn, "A15", "Total", BOLD); put(Fn, "B15", "=SUM(B9:B14)", BOLD, "0"); put(Fn, "C15", "=SUM(C9:C14)", BOLD, "0"); put(Fn, "D15", "=SUM(D9:D14)", BOLD, "0"); put(Fn, "F15", "=SUM(F9:F14)", BOLD, CR2); put(Fn, "G15", "=SUM(G9:G14)", BOLD, CR2); put(Fn, "H15", "=SUM(H9:H14)", BOLD, CR2)
put(Fn, "A16", "Sources over budget"); put(Fn, "B16", "=COUNTIF(H9:H14,\"<0\")", BOLD, "0")
put(Fn, "A17", "Attributable programme cost excl. SDR pay (Rs cr)"); put(Fn, "B17", "=F15-3.08*MIN(1,F10/G10)", BLK, CR2)
put(Fn, "C17", "SDR pay (Rs 3.08 cr) sits outside the Rs 24 cr programme budget", Font(name="Arial", size=9, color="52514E"))
put(Fn, "A18", "Programme budget proposed (Budget)"); put(Fn, "B18", "=Budget!C12", GRN, CR2)
put(Fn, "A19", "Headroom / (over) (Rs cr)", BOLD); put(Fn, "B19", "=B18-B17", BOLD, CR2)
put(Fn, "C19", "=\"of which brand lines not tied to a source (analyst/PR + other): Rs \"&TEXT(Budget!C10+Budget!C11,\"0.0\")&\" cr\"", Font(name="Arial", size=9, color="52514E"))
put(Fn, "A21", "Note: Events cost Rs 36.9 lakh per qualified opp in FY26 and event-sourced deals won 9% — the costliest source by far. ABM cost per opp is an assumption to test in Q1.", Font(name="Arial", size=9, color="52514E"))
# ---------------- Budget
Bg = sheet("Budget", [34, 14, 14, 14, 60]); title(Bg, "Programme budget reallocation (Rs cr)", "Same Rs 24 cr; moved from low-yield events to strategic ABM, referrals and SEA partner marketing")
for j, h in enumerate(["Line", "FY26 actual", "FY27 proposed", "Change", "Reason"], 1):
    c = Bg.cell(3, j, h); c.font = HDR; c.fill = HFILL
bud = [("Trade events", 9.6, 4.5, "Keep 2–3 flagship events tied to strategic accounts; FY26 cost Rs 37 lakh per qualified opp"),
       ("ABM for 400 strategic accounts", 0.0, 4.0, "New: account research, exec events, targeted content for named plans"),
       ("Digital & content", 5.3, 4.5, "Refocus on Scaled tier and business-case content"),
       ("Outbound data & tools", 3.1, 3.1, "Re-point SDR sequences at Scaled accounts; stop-list removes 781 accounts"),
       ("Customer marketing & referral", 1.2, 2.5, "Referral deals win 24–38%; also supports expansion in top 30"),
       ("SEA partner marketing (MDF)", 0.0, 1.5, "Partner-sourced SEA deals win 34% vs 10% direct"),
       ("Analyst & PR", 1.9, 1.2, "Hold core analyst coverage"),
       ("Other programmes", 2.9, 2.7, "")]
for k, (nm, a, b, why) in enumerate(bud):
    r = 4 + k; put(Bg, f"A{r}", nm); put(Bg, f"B{r}", a, BLUE, CR2); put(Bg, f"C{r}", b, BLUE, CR2); put(Bg, f"D{r}", f"=C{r}-B{r}", BLK, CR2); put(Bg, f"E{r}", why)
put(Bg, "A12", "Total", BOLD); put(Bg, "B12", "=SUM(B4:B11)", BOLD, CR2); put(Bg, "C12", "=SUM(C4:C11)", BOLD, CR2); put(Bg, "D12", "=C12-B12", BOLD, CR2)
put(Bg, "A14", "FY26 actuals: DR3 marketing_programmes (FY26 total Rs 24.0 cr).", Font(name="Arial", size=9, color="52514E"))
# ---------------- Backtest
Bt = sheet("Backtest", [30, 12, 12, 16, 16, 18]); title(Bt, "Does the score predict past wins?", "Tiers applied to FY24–26 qualified closed deals (score trained on FY24–25 only)")
hdr(Bt, 4, ["Tier", "Deals", "Win rate", "Avg won deal (lakh)", "Won ARR (Rs cr)", "ARR per qual. opp (lakh)"])
bt = S["bt"]
for k, (tr, r_) in enumerate(bt.iterrows()):
    r = 5 + k; put(Bt, f"A{r}", tr); put(Bt, f"B{r}", int(r_.deals), BLUE, INT); put(Bt, f"C{r}", round(r_.win_rate, 4), BLUE, PCT)
    put(Bt, f"D{r}", round(r_.avg_won_lakh, 2), BLUE, LK); put(Bt, f"E{r}", round(r_.won_arr_cr, 2), BLUE, CR2); put(Bt, f"F{r}", f"=E{r}*100/B{r}", BLK, LK)
put(Bt, "A8", "Total"); put(Bt, "B8", "=SUM(B5:B7)", BOLD, INT); put(Bt, "E8", "=SUM(E5:E7)", BOLD, CR2)
put(Bt, "A10", "Share of won ARR, Strategic tier"); put(Bt, "B10", "=E5/E8", BLK, PCT); put(Bt, "C10", "vs share of deals"); put(Bt, "D10", "=B5/B8", BLK, PCT)
hdr(Bt, 12, ["FY26 only (out of time)", "Deals", "Win rate"])
for k, (tr, r_) in enumerate(S["bt26"].iterrows()):
    r = 13 + k; put(Bt, f"A{r}", tr); put(Bt, f"B{r}", int(r_["size"]), BLUE, INT); put(Bt, f"C{r}", round(r_["mean"], 4), BLUE, PCT)
put(Bt, "A17", "AUC, FY26 out of time: P(win) score"); put(Bt, "B17", round(S["auc"][0], 3), BLUE, "0.000")
put(Bt, "A18", "Current effort: share of FY26 AE touches"); 
for k, tr in enumerate(["1 Strategic", "2 Scaled", "3 Low-touch"]):
    put(Bt, f"A{19+k}", f"  {tr}"); put(Bt, f"B{19+k}", f'=SUMIF(Tiering!$N$2:$N${NT},A{19+k},Tiering!$R$2:$R${NT})/SUM(Tiering!$R$2:$R${NT})', BLK, PCT)
    Bt[f"A{19+k}"].value = tr
# ---------------- Checks
Ck = sheet("Checks", [60, 14, 12]); title(Ck, "Checks")
hdr(Ck, 3, ["Check", "Value", "OK?"])
checks = [("Tier accounts sum to 3,100", "=Inputs!B18", "=IF(B4=3100,\"OK\",\"ERROR\")"),
          ("Plan share of qualified opps = 100%", "=Inputs!G18", "=IF(ABS(B5-1)<0.0001,\"OK\",\"ERROR\")"),
          ("Source mix = 100%", "=Inputs!B50", "=IF(ABS(B6-1)<0.0001,\"OK\",\"ERROR\")"),
          ("Programme budget = Rs 24.0 cr", "=Budget!C12", "=IF(ABS(B7-24)<0.001,\"OK\",\"ERROR\")"),
          ("Direct bookings by tier = direct target", "=Coverage!C39-Coverage!B5", "=IF(ABS(B8)<0.001,\"OK\",\"ERROR\")"),
          ("AEs needed within AEs available", "=Coverage!D32", "=IF(B9>=0,\"OK\",\"SHORT\")"),
          ("Total capacity covers new-logo need (Rs cr)", "=Coverage!B21-Coverage!B22", "=IF(B10>=0,\"OK\",\"GAP\")"),
          ("Programme cost within budget (Rs cr)", "=Funnel!B19", "=IF(B11>=0,\"OK\",\"OVER\")"),
          ("No source over its budget line (count over)", "=Funnel!B16", "=IF(B12=0,\"OK\",\"OVER\")")]
for k, (a, b, c) in enumerate(checks):
    r = 4 + k; put(Ck, f"A{r}", a); put(Ck, f"B{r}", b, BLK, CR2); put(Ck, f"C{r}", c, BOLD)
wb.save("out/D2_Tiering_Coverage_Workbook.xlsx"); print("saved")
