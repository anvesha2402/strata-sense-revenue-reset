import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
BLUE = Font(name="Arial", size=10, color="0000FF"); BLK = Font(name="Arial", size=10); BOLD = Font(name="Arial", size=10, bold=True)
HDR = Font(name="Arial", size=10, bold=True, color="FFFFFF"); HF = PatternFill("solid", fgColor="1F3A5F"); YEL = PatternFill("solid", fgColor="FFFF00")
wb = Workbook(); ws = wb.active; ws.title = "Envelope"
for i, w in enumerate([44, 11, 11, 11, 12, 13, 13, 13, 12, 58, 13], 1): ws.column_dimensions[get_column_letter(i)].width = w
ws["A1"] = "Inject 1: FY27 investment envelope, re-prioritised to Rs 15 cr"; ws["A1"].font = Font(name="Arial", size=13, bold=True, color="1F3A5F")
ws["A2"] = "Blue = input. Payback (margin-adjusted, months) = cost ÷ (annual ARR gain × contribution margin) × 12. Contribution margin = blended GM, less partner margin on partner ARR."; ws["A2"].font = Font(name="Arial", size=9, italic=True)
ws["A3"] = "Blended gross margin"; ws["B3"] = 0.68; ws["B3"].font = BLUE; ws["B3"].number_format = "0%"
ws["C3"] = "Partner margin"; ws["D3"] = 0.15; ws["D3"].font = BLUE; ws["D3"].number_format = "0%"
ws["E3"] = "Payback cap (months)"; ws["F3"] = 15; ws["F3"].font = BLUE
h = ["Initiative", "Original Rs 18 cr draft", "Rs 15 cr plan", "Change", "Partner ARR? (1=yes)", "FY27 ARR gain (Rs cr)", "Run-rate ARR gain (Rs cr)", "Payback on run-rate (months)", "Meets cap?", "Evidence / basis (D1, D2)", "Run-rate annual cost (Rs cr)"]
for j, v in enumerate(h, 1):
    c = ws.cell(5, j, v); c.font = HDR; c.fill = HF; c.alignment = Alignment(wrap_text=True, vertical="top")
rows = [
 ("Retention squad: 4 CSMs + adoption programme (low-usage & Helix-incumbent renewals)", 1.52, 1.52, 0, 3.0, 3.0, "Low-usage customers NRR 79%; Helix-incumbent NRR 92%; ₹25.6 cr Helix base erosion (D1). Target: save 12% of FY26 churn+contraction (₹25 cr)."),
 ("Top-30 expansion programme (expansion incentives + 1 solutions architect)", 0.82, 0.82, 0, 2.5, 2.5, "Top-30 expansion fell ₹21.3 → ₹9.5 cr; Lotus Motors plan alone +₹3.2 cr (D2)."),
 ("AE retention pool for tenured AEs", 1.00, 1.00, 0, 1.5, 1.5, "AE attrition 29%; tenured AE books ₹0.89 cr/yr vs ~₹0.15 cr for a first-year replacement (D1). Target: 4 fewer exits."),
 ("SEA channel foundation: VP Channel, 2 partner managers, enablement, PRM/deal registration", 2.44, 2.44, 1, 1.4, 3.5, "SEA partner deals win 34% vs 10% direct (D1). 3 of the 6 permitted channel roles."),
 ("Partner incentives: +5 pts margin on registered deals, SPIFFs", 0.40, 0.40, 1, 0.3, 0.6, "No deal registration today; partner share fell 12% → 6%."),
 ("Value-selling enablement: business-case training, value calculator, 1 value engineer", 0.92, 0.92, 0, 1.2, 1.2, "Proposals with a quantified business case win 41% vs 32% (D1)."),
 ("Solutions engineers for paid pilots", 0.96, 0.64, 0, 1.0, 0.7, "Trimmed from 3 to 2 SEs."),
 ("RevOps analysts (2) + forecasting tool", 1.00, 1.00, 0, 0.0, 0.0, "Enabler: commit miss 24%, Commit conversion 27% (D1). No direct ARR claimed."),
 ("Sensor-agnostic tier: launch readiness (Q4 FY27 at the earliest)", 0.60, 0.60, 0, 0.0, 0.0, "44% of TrueSense losses cite existing-sensor reuse (D1). Launch cost only; product build sits with R&D."),
 ("Helix-incumbent renewal protection (exec sponsor programme, MES integration pack)", 0.80, 0.80, 0, 1.0, 1.0, "₹108.6 cr of ARR sits with Helix-incumbent customers (D1)."),
 ("AE hiring", 6.00, 1.50, 0, 0.1, 2.5, "Draft: 12 AEs from H1 (₹6 cr, +₹1.1 cr FY27). Plan: 6 AEs from Q3 (₹1.5 cr FY27); ramp means FY28 payoff (D2)."),
 ("Gated reserve (released at Q2 FY27 review against triggers)", 1.54, 3.36, 0, 0.0, 0.0, "Release only if early-warning triggers are met (e.g. strategic pipeline ≥ plan, retention squad saves ≥ ₹1 cr by Q2)."),
]
for i, (nm, a, b, pp, g27, grr, ev) in enumerate(rows):
    r = 6 + i
    ws.cell(r, 1, nm).font = BLK; ws.cell(r, 1).alignment = Alignment(wrap_text=True, vertical="top")
    for col, v in ((2, a), (3, b), (5, pp), (6, g27), (7, grr)):
        c = ws.cell(r, col, v); c.font = BLUE; c.number_format = "0.00" if col != 5 else "0"
    ws.cell(r, 4, f"=C{r}-B{r}").number_format = "0.00;(0.00);-"
    rc = ws.cell(r, 11, 3.0 if nm == "AE hiring" else f"=C{r}"); rc.font = BLUE if nm == "AE hiring" else BLK; rc.number_format = "0.00"
    ws.cell(r, 8, f'=IF(G{r}>0,K{r}/(G{r}*($B$3-E{r}*$D$3))*12,"n/a")').number_format = "0.0"
    ws.cell(r, 9, f'=IF(G{r}>0,IF(H{r}<=$F$3,"Yes","No"),"Enabler")')
    ws.cell(r, 10, ev).font = Font(name="Arial", size=9); ws.cell(r, 10).alignment = Alignment(wrap_text=True, vertical="top")
    for col in (4, 8, 9): ws.cell(r, col).font = BLK
last = 6 + len(rows) - 1; t = last + 1
ws.cell(t, 1, "Total").font = BOLD
for col in (2, 3, 4, 6, 7):
    L = get_column_letter(col); c = ws.cell(t, col, f"=SUM({L}6:{L}{last})"); c.font = BOLD; c.number_format = "0.00;(0.00);-"
ws.cell(t + 2, 1, "Check: Rs 15 cr plan within cap").font = BOLD; ws.cell(t + 2, 3, f'=IF(C{t}<=15.0001,"OK","OVER")').font = BOLD
ws.cell(t + 3, 1, "Blended payback of run-rate spend with an ARR claim (months)"); ws.cell(t + 3, 3, f"=(SUM(K6:K{last-1})-K13-K14)/(SUMPRODUCT(G6:G{last-1},$B$3-E6:E{last-1}*$D$3))*12").number_format = "0.0"
ws.cell(t + 5, 1, "OPTION (not requested now): extra Rs 3 cr").font = BOLD
ws.cell(t + 6, 1, "Second retention squad for Helix-incumbent renewals (4 CSMs + renewal protection), cost Rs cr"); ws.cell(t + 6, 3, 1.6).font = BLUE
ws.cell(t + 7, 1, "ARR protected (Rs cr)"); ws.cell(t + 7, 3, 2.0).font = BLUE
ws.cell(t + 8, 1, "Payback (months)"); ws.cell(t + 8, 3, f"=C{t+6}/(C{t+7}*$B$3)*12").number_format = "0.0"
ws.cell(t + 9, 1, "Six more AEs in Q4 FY27 (FY27 cost) / FY28 ARR / payback on FY28 run-rate"); ws.cell(t + 9, 3, 0.75).font = BLUE; ws.cell(t + 9, 4, 2.5).font = BLUE
ws.cell(t + 9, 5, f"=6*0.5/(D{t+9}*$B$3)*12").number_format = "0.0"
ws.cell(t + 10, 1, "Reading: the first package clears 15 months; the second does not in FY27. We hold both for the Q2 review (and Inject 4 evidence) rather than ask now.").font = Font(name="Arial", size=9, italic=True)
for row in ws.iter_rows(min_row=6, max_row=t + 10):
    for c in row:
        if c.font is None or c.font.name != "Arial": c.font = BLK
ws.freeze_panes = "B6"
wb.save("out/Inject1_Envelope.xlsx"); print("ok", t)
