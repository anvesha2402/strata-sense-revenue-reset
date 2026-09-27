const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, LevelFormat, AlignmentType, BorderStyle, Footer, PageNumber, ImageRun } = require('docx');
const W = 10206, r = (t, o = {}) => new TextRun({ text: t, ...o });
const P = (x, o = {}) => new Paragraph({ spacing: { after: 80, line: 259 }, ...o, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const H1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 150, after: 60 }, keepNext: true, children: [r(t)] });
const B = t => r(t, { bold: true });
const bul = x => new Paragraph({ numbering: { reference: 'b', level: 0 }, spacing: { after: 40, line: 252 }, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const bd = { style: BorderStyle.SINGLE, size: 4, color: 'C9C8C2' };
const cell = (t, w, h, hl) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders: { top: bd, bottom: bd, left: bd, right: bd }, shading: h ? { type: ShadingType.CLEAR, fill: '1F3A5F', color: 'auto' } : (hl ? { type: ShadingType.CLEAR, fill: 'E8EEF5', color: 'auto' } : undefined), margins: { top: 35, bottom: 35, left: 70, right: 70 }, children: [new Paragraph({ children: [r(String(t), { bold: h || hl, color: h ? 'FFFFFF' : undefined, size: 16 })] })] });
const table = (rows, cols, hlRow = -1) => new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cols, rows: rows.map((rw, i) => new TableRow({ cantSplit: true, children: rw.map((t, j) => cell(t, cols[j], i === 0, i === hlRow)) })) });
const img = (f, w0, h0) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new ImageRun({ type: 'png', data: fs.readFileSync('fig/' + f), transformation: { width: 620, height: Math.round(620 * h0 / w0) } })] });
const small = t => P([r(t, { size: 15, italics: true, color: '52514E' })]);
const H = JSON.parse(fs.readFileSync('out/D4_holdout_forecast_LOCKED.json'));
const kids = [
  new Paragraph({ spacing: { after: 30 }, children: [r('D4 · Pipeline and forecasting: method note', { bold: true, size: 30, color: '1F3A5F' })] }),
  P([r('Strata Sense is fictional; all data synthetic (MBA capstone). Dashboard: D4_Forecast_Dashboard.xlsx. Code: d4_prep.py, d4_methods.py, d4_final.py, d4_views.py.', { italics: true, size: 16, color: '52514E' })], { border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '1F3A5F', space: 4 } } }),
  H1('1. The number, and why to believe it'),
  P([B(`Q1 FY27 forecast (locked): p50 ₹${H.p50_cr} cr, p10 ₹${H.p10_cr} cr, p90 ₹${H.p90_cr} cr. `), `That is below the reps’ month-1 commit of ₹${H.cross_checks.rep_commit_m1_cr} cr and roughly half of the ₹17.15 cr quota. The forecast was fixed from the 1 April 2026 snapshot before any Q1 outcome was seen (file hash ${H.sha256.slice(0, 12)}…).`]),
  P([B('Why believe it when the last forecast missed by 24%? '), 'Because it was tested the way it will be used. For each of the last eight quarters I rebuilt the forecast using only data available on the first day of that quarter. The final method missed by 15.6% on average with almost no bias (+4%); the reps’ commits missed by 26.6% and were too high in seven of eight quarters.']),
  img('backtest.png', 1440, 560),
  H1('2. Data and definitions'),
  bul([B('Target: '), 'new-logo bookings in the quarter from the cleaned CRM (D1), which match DR3 new-logo ARR to the rupee. Against these cleaned bookings the FY26 commit miss is 34%; the 24% in the brief is measured against reported bookings that include duplicate deals.']),
  bul([B('Inputs: '), 'the 12 quarter-start pipeline snapshots (stage, expected close date, value, category) plus deal age and close-date pushes rebuilt from the CRM history. No field that is only known later (for example contacts logged by the export date) is used.']),
  bul([B('No look-ahead: '), 'each quarter is trained on the four previous snapshots and their outcomes, which were all known before the quarter began.']),
  H1('3. Methods compared'),
  table([['Method', 'How it works', 'MAPE', 'Bias', 'Worst miss'],
    ['Rep commit (baseline)', 'Month-1 commit call submitted by the sales team', '26.6%', '+25.0%', '60.7%'],
    ['Stage-weighted', 'Value × historical in-quarter win rate by stage and close-date bucket (in quarter, later, already past)', '19.6%', '+16.3%', '58.9%'],
    ['Cohort-age conversion', 'Value × win rate by deal age (0–3 … 12+ months) and stage group; ignores rep close dates', '25.7%', '+22.9%', '65.3%'],
    ['Logistic simulation', 'Deal-level win probability (stage, age, pushes, close-date bucket, size); 4,000 Monte Carlo draws give a range', '22.6%', '+21.3%', '56.1%'],
    ['Ensemble of the three', 'Simple average', '22.6%', '+20.2%', '60.1%'],
    ['Final: stage-weighted, calibrated', 'Stage-weighted × median (actual ÷ forecast) over the previous four quarters', '15.6%', '+4.4%', '49.5%']], [2000, 5006, 1000, 1000, 1200], 6),
  P([B('Why calibration is needed. '), 'Every method based on history over-forecasts, because pipeline conversion has fallen year after year (in-quarter conversion of reported pipeline went from 32% in FY24 to 19% in FY26). Calibration scales the forecast by how much the method over-shot in the last four quarters, using past quarters only. Two cautions: I chose calibration after seeing the back-test, so 15.6% is slightly optimistic; and if conversion stops falling, calibration will under-forecast for a quarter or two before it corrects.']),
  P([B('Range. '), 'p10 and p90 combine the calibrated method’s past errors with the spread from the simulation. In the back-test the p10–p90 band contained the actual in 6 of 8 quarters (75% vs 80% intended), so the range is slightly too narrow.']),
  H1('4. The Q1 FY27 hold-out forecast'),
  table([['Component', 'Value'], ['Raw stage-weighted forecast', `₹${H.raw_stage_weighted_cr} cr`], ['Calibration factor (last four quarters)', `${H.calibration_factor}`], ['Final p50 (p10–p90)', `₹${H.p50_cr} cr (₹${H.p10_cr}–${H.p90_cr} cr)`],
    ['Cross-checks: cohort-age / simulation (p10–p90)', `₹${H.cross_checks.cohort_age_cr} cr / ₹${H.cross_checks.simulation_expected_cr} cr (₹${H.cross_checks.simulation_p10_p90[0]}–${H.cross_checks.simulation_p10_p90[1]} cr)`],
    ['Rep commit (month 1) / quota', `₹${H.cross_checks.rep_commit_m1_cr} cr / ₹17.15 cr`], ['Snapshot pipeline: total / in quarter / in quarter with no hygiene flag', '₹124.6 cr / ₹78.0 cr / ₹34.1 cr']], [5500, 4706]),
  P('The uncalibrated methods agree with the reps (₹10.6–12.7 cr). They have been too high in six of the last seven quarters for the same reason: conversion keeps falling. I am backing the calibrated number and naming the risk: if the new stage-exit rules and tiering lift conversion faster than expected, Q1 could land nearer the rep commit.'),
  H1('5. Coverage: reported vs required'),
  img('coverage.png', 1440, 500),
  P('Reported in-quarter coverage is 3.5x quota for Q1 FY27, but trailing conversion implies 5.6x is needed to hit quota. Counting only deals with no hygiene flag, clean coverage is 2.0x. Planning against 3x is planning to miss.'),
  H1('6. Pipeline hygiene rules'),
  table([['Stage', 'Ageing limit', 'Exit criteria'],
    ['1 Qualify', '75 days', 'Pain and asset scope confirmed; economic buyer named; budget route known'],
    ['2 Solution design', '65 days', '≥3 contacts incl. finance or procurement; security requirements captured'],
    ['3 Proof of value', '65 days', 'Paid pilot signed with written success criteria and conversion price'],
    ['4 Proposal', '60 days', 'Business case on buyer numbers; finance engaged; mutual action plan'],
    ['5 Negotiation', '80 days', 'Paper process mapped; legal and security cleared; signature date confirmed by the economic buyer']], [1800, 1300, 7106]),
  P('Ageing limits are the 75th percentile of days won deals spent in each stage (FY25–26). Flags: close date already past (27 deals, ₹12.8 cr), pushed 2+ times (18, ₹8.2 cr), over the ageing limit (86, ₹41.1 cr), single-threaded at stage 3+ (74, ₹36.3 cr), no activity for 90 days (11, ₹6.0 cr), Commit below stage 5 (27, ₹11.5 cr). In total, 57% of snapshot value carries at least one flag.'),
  H1('7. Performance views (FY26)'),
  bul([B('Tier: '), 'strategic-tier deals win 26% at ₹82 lakh; low-touch 11% at ₹28 lakh. Scaled has the highest velocity (₹7.6 lakh a day) because of volume.']),
  bul([B('Source: '), 'events are the slowest source (9% win, ₹0.7 lakh a day of velocity); referrals win 24%.']),
  bul([B('Tenure: '), 'AEs with more than 24 months produce ₹9.7 lakh a day of velocity; under 9 months, ₹2.2 lakh.']),
  bul('Every cut is available on the Dashboard selector (segment, source, competitor, tenure, region, tier; FY24–FY26).'),
  H1('8. Three-year scenarios'),
  table([['Ending ARR (₹ cr)', 'FY27', 'FY28', 'FY29', 'Key drivers'],
    ['Base', '356.4', '432.8', '541.2', 'Win 21.8% → 23.5%; NRR 100% → 107%; partner ₹4 → 18 cr (D2, D3, Inject 1)'],
    ['Downside', '333.0', '365.7', '409.9', 'Win stays ~17–18%; NRR 97% → 101%; partner flat'],
    ['Aggressive', '364.5', '458.5', '600.2', 'Win 23% → 26%; NRR 101% → 108%; partner ₹4.5 → 22 cr'],
    ['Board path', '356.5', '427.8', '521.9', '']], [2000, 1100, 1100, 1100, 4906]),
  small('The base case meets the board path only if the qualified-opportunity volumes in FY28–29 are funded with capacity; D7 tests that.'),
  H1('9. Governance'),
  bul([B('Categories: '), 'Commit = stage 5, signature date confirmed by the economic buyer, ≥3 contacts, close date pushed at most once. Best case = stage 4 with a business case and mutual action plan. Pipeline = other qualified in-quarter deals. Omitted = any flag unresolved for two weeks.']),
  bul([B('Weekly routine: '), 'Monday reps update and flags run; Tuesday managers inspect every Commit and Best-case deal with a 7-question checklist; Wednesday the CRO compares model p50 and range with manager calls; Thursday finance receives one number with a range.']),
  bul([B('Views: '), 'rep (own flags and gaps), manager (team categories and deals to inspect), CRO (model vs calls, coverage by region, win rate by tier), CFO (one number, range, bias history, clean coverage).']),
  H1('10. Limits'),
  P('Eight quarters is a small test; one quarter (Q3 FY26) was missed by 50%. The calibration assumes conversion keeps drifting down. Redefining Commit will change rep behaviour, which may break the historical rates for a quarter. The hold-out result, scored after the quarter closes, is the honest test.'),
];
const doc = new Document({ styles: { default: { document: { run: { font: 'Arial', size: 18 } } }, paragraphStyles: [{ id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 21, bold: true, color: '1F3A5F' }, paragraph: { outlineLevel: 0 } }] },
  numbering: { config: [{ reference: 'b', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 220 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 800, bottom: 800, left: 850, right: 850 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [r('Strata Sense · D4 method note · page ', { size: 14, color: '52514E' }), new TextRun({ children: [PageNumber.CURRENT], size: 14, color: '52514E' })] })] }) }, children: kids }] });
Packer.toBuffer(doc).then(b => fs.writeFileSync('out/D4_Method_Note.docx', b));
// ---------- forecast call script
const call = [
  new Paragraph({ spacing: { after: 40 }, children: [r('D4 · 10-minute forecast call: Q1 FY27', { bold: true, size: 28, color: '1F3A5F' })] }),
  P([r('Speaker notes. Fictional company; synthetic data.', { italics: true, size: 16, color: '52514E' })]),
  table([['Min', 'Say', 'Show'],
    ['0–1', `"My Q1 number is ₹${H.p50_cr} crore, with an 80% range of ₹${H.p10_cr} to ₹${H.p90_cr} crore. It is below the team commit of ₹${H.cross_checks.rep_commit_m1_cr} crore and about half of quota."`, 'Dashboard tiles'],
    ['1–3', '"Why believe it: I re-ran the last eight quarters as if I were standing on day one of each. This method missed by 16% on average; our commits missed by 27% and were high seven times out of eight."', 'Back-test chart'],
    ['3–5', '"Why it is lower: every history-based method is too high because conversion keeps falling, from 32% of in-quarter pipeline in FY24 to 19% in FY26. I correct for that using only the last four quarters."', 'Backtest table'],
    ['5–7', '"The pipeline behind it: ₹78 crore in quarter, but only ₹34 crore has no hygiene flag. Clean coverage is 2.0x; we need 5.6x at today’s conversion."', 'Coverage chart; Hygiene sheet'],
    ['7–8', '"What would move it: 27 deals in Commit are not at stage 5. If the Tuesday inspections confirm them, I will move toward ₹10 crore; if not, toward ₹7 crore."', 'Top flagged deals'],
    ['8–10', '"Asks: adopt the new Commit definition this week; run the Monday–Thursday routine; plan FY27 against about 5x coverage, not 3x. I will score this forecast when Q1 closes, whatever the result."', 'Governance sheet']], [800, 7206, 2200]),
  P([B('Likely challenge and answer. '), '"Your model under-forecast Q1 FY26 by 22%." Yes, and that quarter fell outside my range, as did Q3 FY26: the band caught 6 of 8 quarters, so I treat it as slightly too narrow and say so. "Why not trust the reps?" Their commits have been high by 25% on average; the model is a check on that bias, not a replacement for deal inspection.'], { spacing: { before: 100 } }),
];
Packer.toBuffer(new Document({ styles: { default: { document: { run: { font: 'Arial', size: 19 } } } }, sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 850, bottom: 850, left: 850, right: 850 } } }, children: call }] })).then(b => fs.writeFileSync('out/D4_Forecast_Call_Script.docx', b));
