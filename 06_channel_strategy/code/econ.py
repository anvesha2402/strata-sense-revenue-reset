import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
signed = pd.read_pickle("dr/signed.pkl"); pros = pd.read_pickle("dr/pros.pkl")
BLUE = Font(name="Arial", size=10, color="0000FF"); BLK = Font(name="Arial", size=10); BOLD = Font(name="Arial", size=10, bold=True); GRN = Font(name="Arial", size=10, color="008000")
HDR = Font(name="Arial", size=10, bold=True, color="FFFFFF"); HF = PatternFill("solid", fgColor="1F3A5F"); YEL = PatternFill("solid", fgColor="FFFF00"); SM = Font(name="Arial", size=9, color="52514E")
wb = Workbook()
def sh(n, w):
    ws = wb.create_sheet(n)
    for i, x in enumerate(w, 1): ws.column_dimensions[get_column_letter(i)].width = x
    return ws
def hdr(ws, r, vals, c0=1):
    for j, v in enumerate(vals, c0): c = ws.cell(r, j, v); c.font = HDR; c.fill = HF; c.alignment = Alignment(wrap_text=True, vertical="top")
def put(ws, ref, v, f=BLK, fmt=None, fill=None, wrap=False):
    c = ws[ref]; c.value = v; c.font = f
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap: c.alignment = Alignment(wrap_text=True, vertical="top")
def T(ws, t, s=""): put(ws, "A1", t, Font(name="Arial", size=13, bold=True, color="1F3A5F")); put(ws, "A2", s, Font(name="Arial", size=9, italic=True, color="52514E"))
CR = "0.00;(0.00);-"; PCT = "0.0%"
ws = wb.active; ws.title = "README"; ws.column_dimensions["A"].width = 22; ws.column_dimensions["B"].width = 110
for i, (a, b) in enumerate([("D6 PARTNER ECONOMICS WORKBOOK", ""), ("Company", "Strata Sense is fictional; synthetic data (MBA capstone)."),
    ("Colour code", "Blue = input; yellow = key assumption; black = formula; green = link."),
    ("Sheets", "Inputs · Partner_ramp (active partners and partner-sourced ARR) · Channel_PL · GM_floor · Breakeven · Inject3 · Partners_14 · Prospects_12 · Checks"),
    ("Sources", "DR6 partner file; D1 (partner win rates by region, FY26 partner-sourced ARR ₹2.6 cr); D2 (FY27 partner target); D4 base scenario (FY28–29 new-logo); DR3 (gross margin, S&M)."),
    ("No double counting", "A partner-sourced deal worked by an AE is counted once in bookings, as partner-sourced. The AE receives 50% quota credit (comp only, not bookings).")], 1):
    ws.cell(i, 1, a).font = BOLD if i == 1 else BLK; ws.cell(i, 2, b).font = BLK; ws.cell(i, 2).alignment = Alignment(wrap_text=True)
# Inputs
I = sh("Inputs", [52, 12, 12, 12, 56]); T(I, "Inputs", "")
hdr(I, 4, ["Input", "FY27", "FY28", "FY29", "Source / note"])
rows = [("Total new-logo ARR in plan (₹ cr)", 46.5, 62.1, 78.0, "D2 (FY27); D4 base scenario (FY28–29)", None),
 ("Target partner-sourced share of new-logo ARR", None, None, 0.25, "Board objective 5 (FY29)", None),
 ("Productivity of a mature active partner (₹ cr sourced ARR / yr)", 1.2, 1.2, 1.2, "Assumption: ~10 qualified opps × 34% win (SEA partner deals, D1) × ₹37 lakh partner deal (FY26)", "Y"),
 ("Ramp: activation-year productivity (share of mature)", 0.15, 0.15, 0.15, "Assumption: activated mid-year on average, first deal after 6–9 months (half a year at 30%)", "Y"),
 ("Ramp: second-year productivity (share of mature)", 0.60, 0.60, 0.60, "Assumption; 100% from the third year", "Y"),
 ("Existing active partners' sourced ARR (₹ cr)", 2.6, 2.6, 2.6, "FY26 actual (D1, after re-tagging)", None),
 ("Blended gross margin before partner margin", 0.683, 0.683, 0.683, "DR3 FY26", None),
 ("Direct S&M cost per ₹1 of new-logo ARR", 1.64, 1.64, 1.64, "DR3: ~70% of ₹96 cr S&M ÷ ₹41 cr new-logo ARR (allocation assumption)", "Y"),
 ("Direct effort still needed on partner deals (share)", 0.40, 0.35, 0.30, "AE co-sell and SE support; falls as partners certify", "Y"),
 ("Mix: referral / resell / gold (share of partner ARR)", "30/50/20", "25/50/25", "20/50/30", "Design choice", None)]
ref = {}
for k, (lab, a, b, c, src, key) in enumerate(rows):
    r = 5 + k; ref[k] = r; put(I, f"A{r}", lab)
    for col, v in zip("BCD", (a, b, c)):
        if v is not None: put(I, f"{col}{r}", v, BLUE, PCT if isinstance(v, float) and v < 1 and k in (1, 3, 4, 6, 8) else ("0.00" if isinstance(v, float) else None), YEL if key else None)
    put(I, f"E{r}", src, SM)
put(I, "A17", "PROGRAMME ECONOMICS", BOLD)
hdr(I, 18, ["Role / tier", "Year-1 margin", "Renewal margin (yrs 2–3)", "Share FY27", "Share FY28", "Share FY29"])
tiers = [("Referral (registered)", 0.10, 0.0, 0.30, 0.25, 0.20), ("Silver (resell / co-sell)", 0.18, 0.08, 0.50, 0.50, 0.50), ("Gold (resell + certified services)", 0.22, 0.10, 0.20, 0.25, 0.30)]
for k, (nm, m1, m2, s1, s2, s3) in enumerate(tiers):
    r = 19 + k; put(I, f"A{r}", nm)
    for col, v in zip("BCDEF", (m1, m2, s1, s2, s3)): put(I, f"{col}{r}", v, BLUE, PCT)
put(I, "A22", "Blended year-1 margin FY27 / FY28 / FY29")
for j, col in enumerate("DEF"): put(I, f"{col}22", f"=SUMPRODUCT($B$19:$B$21,{col}19:{col}21)", BOLD, PCT)
put(I, "A23", "Blended renewal margin FY27 / FY28 / FY29")
for j, col in enumerate("DEF"): put(I, f"{col}23", f"=SUMPRODUCT($C$19:$C$21,{col}19:{col}21)", BOLD, PCT)
put(I, "A25", "CHANNEL TEAM AND PROGRAMME COSTS (₹ cr / yr)", BOLD)
hdr(I, 26, ["Item", "FY27", "FY28", "FY29", "Note"])
costs = [("VP Channel", 0.9, 0.9, 0.9, "1 role (vacant today)"), ("Partner managers (count)", 2, 4, 5, "FY27: 2 SEA; within 6 channel roles"), ("Cost per partner manager", 0.42, 0.44, 0.46, "HR benchmark ₹38–45 lakh (DR3), inflated"),
         ("Enablement and certification", 0.4, 0.5, 0.5, "Training, demo kits"), ("PRM / deal-registration tool", 0.3, 0.3, 0.3, ""), ("Partner marketing (MDF)", 1.5, 2.0, 2.5, "FY27 from the ₹24 cr programme budget (D2)")]
for k, (nm, a, b, c, n) in enumerate(costs):
    r = 27 + k; put(I, f"A{r}", nm)
    for col, v in zip("BCD", (a, b, c)): put(I, f"{col}{r}", v, BLUE, "0" if k == 1 else "0.00")
    put(I, f"E{r}", n, SM)
put(I, "A33", "Channel fixed cost (₹ cr)", BOLD)
for col in "BCD": put(I, f"{col}33", f"={col}27+{col}28*{col}29+{col}30+{col}31+{col}32", BOLD, CR)
# Partner ramp
R = sh("Partner_ramp", [44, 12, 12, 12, 50]); T(R, "Active partners and partner-sourced ARR", "Cohort ramp: recruits contribute 15% of mature productivity in the year they are activated, 60% the next year, 100% after")
hdr(R, 4, ["Line", "FY27", "FY28", "FY29", "Note"])
put(R, "A5", "New partners activated in year (count)"); [put(R, f"{c}5", v, BLUE, "0", YEL) for c, v in zip("BCD", (8, 9, 5))]; put(R, "E5", "FY27: 6 prospects (PR01, PR02, PR06, PR07, PR09, PR10) + P07, P10 reactivated; FY28: 3 held prospects + 6 new", SM)
put(R, "A6", "Existing partners retained (after keep/fix/exit and Inject 3)"); [put(R, f"{c}6", v, BLUE, "0") for c, v in zip("BCD", (6, 6, 6))]; put(R, "E6", "P02, P09, P12, P13 + P05, P11 restricted (P07, P10 counted as FY27 activations)", SM)
put(R, "A7", "Existing partners' sourced ARR after Inject 3 (₹ cr)"); put(R, "B7", "=Inputs!B10*(1-Inject3!B8)", GRN, CR); put(R, "C7", "=B7*1.1", BLK, CR); put(R, "D7", "=C7*1.1", BLK, CR)
put(R, "A8", "ARR from FY27 recruits (₹ cr)"); put(R, "B8", "=B5*Inputs!B7*Inputs!B8", BLK, CR); put(R, "C8", "=B5*Inputs!C7*Inputs!C9", BLK, CR); put(R, "D8", "=B5*Inputs!D7", BLK, CR)
put(R, "A9", "ARR from FY28 recruits (₹ cr)"); put(R, "C9", "=C5*Inputs!C7*Inputs!C8", BLK, CR); put(R, "D9", "=C5*Inputs!D7*Inputs!D9", BLK, CR)
put(R, "A10", "ARR from FY29 recruits (₹ cr)"); put(R, "D10", "=D5*Inputs!D7*Inputs!D8", BLK, CR)
put(R, "A11", "Partner-sourced new-logo ARR (₹ cr)", BOLD); [put(R, f"{c}11", f"=SUM({c}7:{c}10)", BOLD, CR) for c in "BCD"]
put(R, "A12", "Share of new-logo ARR"); [put(R, f"{c}12", f"={c}11/Inputs!{c}5", BOLD, PCT) for c in "BCD"]
put(R, "A13", "Active partners (count)"); put(R, "B13", "=B6+B5", BLK, "0"); put(R, "C13", "=B13+C5", BLK, "0"); put(R, "D13", "=C13+D5", BLK, "0")
put(R, "A14", "Surplus / (gap) vs 25% in FY29 (₹ cr)", BOLD); put(R, "D14", "=D11-Inputs!D6*Inputs!D5", BOLD, CR)
put(R, "A15", "Mature-equivalent partners needed for 25% in FY29"); put(R, "D15", "=Inputs!D6*Inputs!D5/Inputs!D7", BOLD, "0.0")
put(R, "A16", "FY29 share if mature productivity is ₹0.8 / 1.0 / 1.4 cr (recruit ARR scaled)"); [put(R, f"{c}16", f"=(D7+(D8+D9+D10)*{p}/Inputs!D7)/Inputs!D5", BLK, PCT) for c, p in zip("BCD", (0.8, 1.0, 1.4))]
put(R, "A18", "Reading: the ramp is the constraint. Partners recruited in FY29 contribute little that year, so 25% depends on 17 activations in FY27–28 reaching ~₹1.2 cr each. At ₹1.0 cr the share is ~21%.", SM)
put(R, "A19", " the ramp is the constraint. Partners recruited in FY29 contribute little that year, so the 25% goal depends on recruiting in FY27–28.", SM)
# Channel P&L
P = sh("Channel_PL", [52, 12, 12, 12, 50]); T(P, "Channel profit and loss (₹ cr)", "Two lenses: incremental (channel ARR the direct team would not win) and substitution (channel replaces direct selling cost)")
hdr(P, 4, ["Line", "FY27", "FY28", "FY29", "Note"])
L = [("Partner-sourced new-logo ARR", "=Partner_ramp!{c}11"), ("Year-1 partner margin", "={c}5*Inputs!{m}22"),
     ("Renewal margin on prior partner cohorts", "{ren}"), ("Channel fixed cost", "=Inputs!{c}33"), ("Direct effort still used on partner deals", "={c}5*Inputs!{c}13*Inputs!{c}12"),
     ("Total channel cost", "={c}6+{c}7+{c}8+{c}9"), ("Incremental lens: first-year gross profit on partner ARR", "={c}5*Inputs!{c}11"),
     ("Incremental lens: channel profit / (loss), first year", "={c}11-{c}10"), ("Substitution lens: direct S&M cost avoided", "={c}5*Inputs!{c}12"),
     ("Substitution lens: saving / (extra cost) vs direct", "={c}13-{c}10")]
mm = {"B": "D", "C": "E", "D": "F"}
for k, (lab, f) in enumerate(L):
    r = 5 + k; put(P, f"A{r}", lab, BOLD if k in (5, 7, 9) else BLK)
    for c in "BCD":
        if "{ren}" in f:
            ren = "=0" if c == "B" else ("=B5*Inputs!E23" if c == "C" else "=(B5+C5)*Inputs!F23")
            put(P, f"{c}{r}", ren, BLK, CR)
        else: put(P, f"{c}{r}", f.format(c=c, m=mm[c]), BOLD if k in (5, 7, 9) else BLK, CR)
put(P, "A16", "Three-year value of one year's partner ARR (GP × 3 − yr-1 margin − 2 yrs renewal margin), FY29 cohort"); put(P, "D16", "=D5*(3*Inputs!D11-Inputs!F22-2*Inputs!F23)", BOLD, CR)
put(P, "A17", "Reading: on a first-year basis the channel loses money until partner ARR scales; on the three-year value of each cohort it pays back comfortably.", SM)
# GM floor
G = sh("GM_floor", [52, 12, 12, 12, 50]); T(G, "Blended gross margin with partner margin included", "Guardrail: ≥66% every year, after partner margin. Today partner margin is booked in S&M, outside gross margin.")
hdr(G, 4, ["Line", "FY27", "FY28", "FY29", "Note"])
put(G, "A5", "Total revenue (₹ cr, approx.)"); [put(G, f"{c}5", v, BLUE, "0.0") for c, v in zip("BCD", (433, 510, 610))]; put(G, "E5", "Subscription ≈ average ARR (D4 base) + hardware; D7 replaces", SM)
put(G, "A6", "Gross margin before partner margin"); [put(G, f"{c}6", "=Inputs!" + c + "11", GRN, PCT) for c in "BCD"]
put(G, "A7", "Partner margin (₹ cr)"); [put(G, f"{c}7", f"=Channel_PL!{c}6+Channel_PL!{c}7", GRN, CR) for c in "BCD"]
put(G, "A8", "Gross margin after partner margin", BOLD); [put(G, f"{c}8", f"=({c}5*{c}6-{c}7)/{c}5", BOLD, PCT) for c in "BCD"]
put(G, "A9", "Headroom over 66% floor (pts)"); [put(G, f"{c}9", f"=({c}8-0.66)*100", BLK, "0.0") for c in "BCD"]
put(G, "A10", "Partner margin that would breach the floor (₹ cr)"); [put(G, f"{c}10", f"={c}5*({c}6-0.66)", BLK, CR) for c in "BCD"]
# Break-even
B = sh("Breakeven", [70, 12, 60]); T(B, "At what partner productivity does the channel lose money?", "FY29, at the planned number of active partners. Three lenses; the substitution lens is the decision lens.")
put(B, "A4", "Active partners FY29"); put(B, "B4", "=Partner_ramp!D13", GRN, "0")
put(B, "A5", "Channel fixed cost FY29 (₹ cr)"); put(B, "B5", "=Inputs!D33", GRN, CR)
put(B, "A7", "1. SUBSTITUTION (decision lens): partner deals replace direct selling", BOLD)
put(B, "A8", "Saving per ₹1 of partner ARR: direct S&M avoided × (1 − direct effort) − year-1 partner margin"); put(B, "B8", "=Inputs!D12*(1-Inputs!D13)-Inputs!F22", BLK, "0.000")
put(B, "A9", "Break-even sourced ARR per active partner (₹ cr / yr)", BOLD); put(B, "B9", "=B5/(B4*B8)", BOLD, CR); put(B, "C9", "Below this, the channel costs more than selling direct", SM)
put(B, "A11", "2. INCREMENTAL, THREE-YEAR: partner ARR the direct team would not have won", BOLD)
put(B, "A12", "Contribution per ₹1: 3 yrs gross profit − yr-1 margin − 2 yrs renewal margin − direct effort"); put(B, "B12", "=3*Inputs!D11-Inputs!F22-2*Inputs!F23-Inputs!D13*Inputs!D12", BLK, "0.000")
put(B, "A13", "Break-even sourced ARR per active partner (₹ cr / yr)", BOLD); put(B, "B13", "=B5/(B4*B12)", BOLD, CR)
put(B, "A15", "3. INCREMENTAL, FIRST YEAR ONLY (shown for completeness)", BOLD)
put(B, "A16", "Contribution per ₹1: yr-1 gross profit − yr-1 margin − direct effort"); put(B, "B16", "=Inputs!D11-Inputs!F22-Inputs!D13*Inputs!D12", BLK, "0.000")
put(B, "A17", "Break-even sourced ARR per active partner (₹ cr / yr)"); put(B, "B17", "=IF(B16<=0,\"never\",B5/(B4*B16))", BLK, CR); put(B, "C17", "Near-zero contribution: no subscription business pays back in year one", SM)
put(B, "A19", "FY26 actual: sourced ARR per active partner (₹ cr)"); put(B, "B19", "=(0.69+0.85+0+0.41)/4", BLUE, CR)
put(B, "A20", "FY26 actual: sourced ARR per signed partner (₹ cr)"); put(B, "B20", "=Inputs!D10/14", BLK, CR)
put(B, "A21", "Planned mature productivity (₹ cr)"); put(B, "B21", "=Inputs!D7", GRN, CR)
put(B, "A23", "Answer for the panel: the channel loses money if active partners average less than the substitution break-even above (about a quarter of a crore a year). FY26's active partners averaged about ₹0.5 cr, but spread across all 14 signed partners the figure falls to about ₹0.19 cr, below break-even. The risk is not the good partners; it is carrying inactive ones. Hence the exits and the two-quarter activation rule.", SM)
B["A23"].alignment = Alignment(wrap_text=True, vertical="top"); B.merge_cells("A23:C23"); B.row_dimensions[23].height = 60
# Inject 3
J = sh("Inject3", [60, 14, 50]); T(J, "Inject 3: two active partners (P05, P11) announce joint programmes with Helix", "Week 7")
put(J, "A4", "Open partner-sourced pipeline, all partners (₹ cr)"); put(J, "B4", 14.83, BLUE, CR); put(J, "C4", "DR1 open deals, partner-sourced (re-tagged)", SM)
put(J, "A5", "  of which P05 + P11 (₹ cr)"); put(J, "B5", 7.85, BLUE, CR)
put(J, "A6", "Share of open partner-sourced pipeline at risk"); put(J, "B6", "=B5/B4", BOLD, PCT)
put(J, "A7", "Haircut applied to P05/P11 pipeline (assumption)"); put(J, "B7", 0.5, BLUE, PCT, YEL); put(J, "C7", "Their deals in Helix-incumbent accounts likely switch to Helix", SM)
put(J, "A8", "Reduction to existing partners' FY27 sourced ARR"); put(J, "B8", "=B6*B7*0.5", BOLD, PCT); put(J, "C8", "P05+P11 were half of FY26 sourced ARR (₹1.26 of ₹2.61 cr); half of that at risk", SM)
put(J, "A9", "FY27 partner-sourced ARR before Inject 3 (D2)"); put(J, "B9", 4.0, BLUE, CR)
put(J, "A10", "FY27 partner-sourced ARR after Inject 3 (this model)"); put(J, "B10", "=Partner_ramp!B11", GRN, CR)
put(J, "A11", "Gap handed to D7 (₹ cr)", BOLD); put(J, "B11", "=B9-B10", BOLD, CR); put(J, "C11", "D2 direct capacity had ₹2.9 cr headroom; D7 reconciles", SM)
put(J, "A13", "Response", BOLD)
for k, t in enumerate(["P05 and P11 move to 'restricted': no deal registration in Helix-incumbent accounts; keep services and non-Helix accounts.",
    "Competing-product disclosure required at registration; conflict check by the channel manager within 48 hours.",
    "Exclusivity is not demanded (we could not enforce it); protection is earned by registered, non-conflicted deals.",
    "Accelerate non-Helix SEA recruits (PR01, PR02, PR06) to first-quarter onboarding; PR05, PR08, PR12 (Helix-affiliated) deprioritised.",
    "Review P05/P11 scorecards at the end of Q2 FY27: exit if registered-deal conversion < 15% or any Helix switch on a registered deal."], 14):
    put(J, f"A{k}", t, BLK, wrap=True); J.merge_cells(f"A{k}:C{k}")
# Partners 14
K = sh("Partners_14", [8, 30, 16, 12, 12, 12, 12, 10, 14, 58])
hdr(K, 1, ["ID", "Partner", "Status", "Sourced FY26 (₹ cr)", "Influenced FY26", "Win rate FY24–26", "Open pipeline (₹ cr)", "Helix-tied", "Decision", "Reason"])
dec = {"P01": ("Exit", "Inactive since FY24; no pipeline; Gulf coverage moves to PR07/PR08 review"), "P02": ("Keep: Gold", "22% win rate, ₹4.2 cr open pipeline, non-Helix, 6 certified engineers"),
 "P03": ("Exit", "One deal in three years"), "P04": ("Exit", "No activity"), "P05": ("Fix: restricted", "Solid (21% win) but Helix integrator; Inject 3 → no registration in Helix-incumbent accounts"),
 "P06": ("Exit", "No activity; Saudi coverage via PR07"), "P07": ("Fix: 2-quarter activation", "Vietnam access; certify 2 engineers by Q2 or exit"), "P08": ("Fix: OEM pilot", "Machine-builder embed pilot alongside PR09/PR10"),
 "P09": ("Keep: Gold (services)", "Reliability MSP; ₹7.1 cr open pipeline; strongest influence partner"), "P10": ("Fix: 2-quarter activation", "Malaysia access; joint pipeline plan by Q2 or exit"),
 "P11": ("Fix: probation", "Most volume but 13% win rate; Helix gold partner (Inject 3); referral-only until scorecard met"), "P12": ("Keep: Silver, grow", "Thailand; SEA partner deals win 34%"),
 "P13": ("Keep: Silver", "Gulf access; occasional"), "P14": ("Exit", "No activity")}
for i, r in enumerate(signed.itertuples(), 2):
    d, why = dec[r.partner_id]
    vals = [r.partner_id, r.partner_name, r.status, r.sourced_arr_fy26_cr, r.influenced_arr_fy26_cr, r.win_rate_fy24_26, r.open_pipeline_cr, "Yes" if "Helix" in r.other_vendor_lines else "No", d, why]
    for j, v in enumerate(vals, 1):
        c = K.cell(i, j, None if (isinstance(v, float) and v != v) else v); c.font = BLK; c.alignment = Alignment(wrap_text=True, vertical="top")
    K.cell(i, 6).number_format = "0%"
# Prospects 12 scoring
S = sh("Prospects_12", [8, 30, 22, 20, 9, 9, 9, 9, 9, 10, 12, 44]); T(S, "Prospective partners: scored shortlist", "Weights in row 4 (blue). Scores 1–5. Conflict: Helix-affiliated = 1.")
hdr(S, 3, ["ID", "Prospect", "Type", "Region", "Access (overlap, priority region)", "Capability (engineers)", "Vertical fit", "Conflict risk (5 = none)", "Commitment", "Weighted score", "Rank", "Decision"])
wts = [0.30, 0.20, 0.15, 0.20, 0.15]
for j, wv in enumerate(wts, 5): put(S, f"{get_column_letter(j)}4", wv, BLUE, "0%")
put(S, "A4", "Weights", BOLD)
sc = {"PR01": (5, 5, 4, 5, 5), "PR02": (5, 4, 4, 5, 5), "PR03": (4, 3, 3, 5, 3), "PR04": (3, 2, 3, 5, 3), "PR05": (4, 3, 3, 1, 3), "PR06": (5, 4, 4, 5, 4),
      "PR07": (5, 4, 4, 5, 4), "PR08": (4, 3, 4, 1, 3), "PR09": (5, 2, 5, 5, 5), "PR10": (5, 2, 4, 5, 3), "PR11": (3, 2, 4, 5, 3), "PR12": (3, 3, 3, 1, 1)}
for i, r in enumerate(pros.itertuples(), 5):
    vals = [r.prospect_id, r.name, r.type, r.region] + list(sc[r.prospect_id])
    for j, v in enumerate(vals, 1): S.cell(i, j, v).font = BLUE if j >= 5 else BLK
    S.cell(i, 10, f"=SUMPRODUCT(E{i}:I{i},$E$4:$I$4)").number_format = "0.00"
    S.cell(i, 11, f"=RANK(J{i},$J$5:$J$16)")
    S.cell(i, 12, f'=IF(K{i}<=6,"Recruit FY27",IF(H{i}=1,"Deprioritise (Helix-tied)","Hold for FY28"))')
# Risk simulation (static output of risk_sim.py / risk_sim_down.py)
import json
Z = sh("Risk_sim", [46, 12, 12, 12, 12, 14, 14, 14]); T(Z, "How likely is the channel to lose money? Monte Carlo, 20,000 runs", "Values pasted from risk_sim.py (plan case) and risk_sim_down.py (FY26-like partners). Loss = partner ARR below substitution break-even.")
hdr(Z, 4, ["Case / year", "P10 partner ARR", "P50", "P90", "Break-even ARR", "P(channel loses money)", "P(share ≥ 25%)", "Median share"])
r = 5
for nm, fn in [("Plan case: 70% activation, median ₹1.0 cr / partner", "out/risk_sim.json"), ("Downside: FY26-like partners, 45% activation, median ₹0.45 cr", "out/risk_sim_downside.json")]:
    d = json.load(open(fn)); put(Z, f"A{r}", nm, BOLD); r += 1
    for y in ["FY27", "FY28", "FY29"]:
        v = d[y]; put(Z, f"A{r}", "  " + y)
        for col, key, fmt in zip("BCDEFGH", ["p10", "p50", "p90", "breakeven_total_arr", "p_loss", "p_share25", "median_share"], [CR, CR, CR, CR, "0%", "0%", PCT]): put(Z, f"{col}{r}", round(v[key], 4), BLUE, fmt)
        r += 1
put(Z, f"A{r+1}", "Reading: FY27 loses money by design (~₹0.9 cr). With selected SEA/Gulf partners the loss risk falls to ~9% in FY28 and under 1% in FY29, but 25% in FY29 is a coin flip (46%). If recruits behave like FY26 India partners, the channel loses money in FY28 and has a 44% chance of doing so in FY29. The kill gate (Q2 FY28) stops that path.", SM)
Z[f"A{r+1}"].alignment = Alignment(wrap_text=True, vertical="top"); Z.merge_cells(f"A{r+1}:H{r+1}"); Z.row_dimensions[r+1].height = 55
# Checks
C = sh("Checks", [60, 14, 12]); hdr(C, 1, ["Check", "Value", "OK?"])
ck = [("FY29 partner share ≥ 25%", "=Partner_ramp!D12", '=IF(B2>=0.25,"OK","GAP")'), ("Blended GM after partner margin ≥ 66% (min of 3 years)", "=MIN(GM_floor!B8:D8)", '=IF(B3>=0.66,"OK","BREACH")'),
      ("Channel roles in FY27 ≤ 6 (VP + partner managers)", "=1+Inputs!B28", '=IF(B4<=6,"OK","OVER")'), ("Tier shares sum to 100% each year", "=SUM(Inputs!D19:D21)+SUM(Inputs!E19:E21)+SUM(Inputs!F19:F21)", '=IF(ABS(B5-3)<0.001,"OK","ERROR")'),
      ("Inject 3 gap handed to D7 is non-negative (model not more optimistic than D2)", "=Inject3!B11", '=IF(B6>=0,"OK","CHECK")'),
      ("FY27 channel fixed cost within Inject 1 allocation (₹2.84 cr incl. incentives, excl. MDF)", "=Inputs!B33-Inputs!B32", '=IF(B7<=2.84+0.001,"OK","OVER")')]
for k, (a, b, c) in enumerate(ck, 2): C.cell(k, 1, a).font = BLK; C.cell(k, 2, b).number_format = "0.000"; C.cell(k, 3, c).font = BOLD
wb.save("out/D6_Partner_Economics.xlsx"); print("saved")
