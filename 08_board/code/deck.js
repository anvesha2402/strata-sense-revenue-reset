const pptxgen = require('pptxgenjs');
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.title = 'Strata Sense D8: Board Presentation';
const NAVY = '1F3A5F', BLUE = '2A78D6', ORANGE = 'EB6834', AQUA = '1BAF7A', GREY = 'A3A29C', INK = '1A1A1A', INK2 = '52514E', BG = 'F7F6F2', WHITE = 'FFFFFF';
const HF = 'Cambria', BF = 'Calibri';
function base(title, kicker) {
  const s = pres.addSlide(); s.background = { color: WHITE };
  if (kicker) s.addText(kicker.toUpperCase(), { x: 0.5, y: 0.25, w: 9, h: 0.25, fontFace: BF, fontSize: 10, bold: true, color: ORANGE, charSpacing: 2, margin: 0, isTextBox: true });
  s.addText(title, { x: 0.5, y: 0.48, w: 9, h: 0.75, fontFace: HF, fontSize: 21, bold: true, color: NAVY, margin: 0, valign: 'top', isTextBox: true });
  s.addText('Strata Sense (fictional) · D8', { x: 0.5, y: 5.3, w: 5, h: 0.2, fontFace: BF, fontSize: 8, color: GREY, margin: 0, isTextBox: true });
  return s;
}
function stat(s, x, y, w, big, label, col = NAVY) {
  s.addText(big, { x, y, w, h: 0.5, fontFace: HF, fontSize: 26, bold: true, color: col, margin: 0, isTextBox: true });
  s.addText(label, { x, y: y + 0.5, w, h: 0.55, fontFace: BF, fontSize: 10.5, color: INK2, margin: 0, valign: 'top', isTextBox: true });
}
function tbl(s, rows, x, y, w, colW, fs = 10, hl = [], rowH = 0.26) {
  const data = rows.map((r, i) => r.map((c) => ({ text: String(c), options: { fontFace: BF, fontSize: fs, bold: i === 0 || hl.includes(i), color: i === 0 ? WHITE : INK,
    fill: { color: i === 0 ? NAVY : (i % 2 ? WHITE : BG) }, valign: 'middle' } })));
  s.addTable(data, { x, y, w, colW, border: { type: 'solid', pt: 0.5, color: 'D9D8D2' }, margin: 0.04, rowH });
}
const note = (s, t) => s.addNotes(t);
const src = (s, t) => s.addText(t, { x: 0.5, y: 5.05, w: 9, h: 0.22, fontFace: BF, fontSize: 8, italic: true, color: INK2, margin: 0, isTextBox: true });
function box(s, x, y, w, h, head, body, col = NAVY) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: BG }, line: { color: 'D9D8D2' } });
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.07, h, fill: { color: col }, line: { color: col } });
  s.addText([{ text: head, options: { bold: true, fontSize: 12, color: INK, breakLine: true } }, { text: body, options: { fontSize: 11.5, color: INK2 } }],
    { x: x + 0.18, y: y + 0.08, w: w - 0.28, h: h - 0.14, fontFace: BF, margin: 0, valign: 'top', isTextBox: true });
}

const img = (s, f, x, y, w) => { const b = require('fs').readFileSync('fig/' + f); const W0 = b.readUInt32BE(16), H0 = b.readUInt32BE(20); s.addImage({ path: 'fig/' + f, x, y, w, h: w * H0 / W0 }); };
// 1
let s = pres.addSlide(); s.background = { color: NAVY };
s.addText('D8 · BOARD PRESENTATION', { x: 0.6, y: 0.7, w: 8.8, h: 0.3, fontFace: BF, fontSize: 11, bold: true, color: 'F4B393', charSpacing: 2, margin: 0 });
s.addText('Approve ₹15 crore and 6 AEs to reach ₹526 crore ARR by FY29, and accept a slower FY27', { x: 0.6, y: 1.1, w: 8.6, h: 1.5, fontFace: HF, fontSize: 28, bold: true, color: WHITE, margin: 0, valign: 'top' });
[['₹14.95 cr', 'FY27 investment, inside the ₹15 cr envelope'], ['₹526 cr', 'FY29 ARR vs ₹522 cr board path and ₹389 cr if we do nothing'], ['13.2%', 'FY27 growth: ₹5.6 cr short of 15%, by choice']].forEach((a, i) => {
  s.addText(a[0], { x: 0.6 + i * 3.0, y: 3.2, w: 2.8, h: 0.5, fontFace: HF, fontSize: 22, bold: true, color: WHITE, margin: 0 });
  s.addText(a[1], { x: 0.6 + i * 3.0, y: 3.7, w: 2.7, h: 0.6, fontFace: BF, fontSize: 11, color: 'CADCFC', margin: 0, valign: 'top' }); });
s.addText('Revenue Strategy Lead · Board meeting, Week 9 FY27 · Strata Sense Technologies is fictional; data synthetic', { x: 0.6, y: 4.9, w: 8.8, h: 0.3, fontFace: BF, fontSize: 9, color: 'CADCFC', margin: 0 });
note(s, 'One ask, one trade-off. We invest ₹15 crore, stay inside every guardrail but one, and reach the board’s FY29 ARR. The price is a slower FY27, which I think is cheaper than buying growth we cannot ramp in time.');
// 2 problem
s = base('Growth is stalling because we lose on price and packaging to Helix, sell to the wrong accounts, and discount without winning', 'Why we are here (D1)');
tbl(s, [['Root cause', 'ARR at stake / yr', 'Fixable by sales?'], ['Helix bundle (retention + new logo)', '₹34.0 cr', 'Partly: packaging decision needed'], ['Expansion stall, non-Helix accounts', '₹9.9 cr', 'Yes'], ['Wrong accounts, single-threaded deals', '₹8.0 cr', 'Yes'], ['Discount creep', '₹3.1 cr', 'Yes']], 0.5, 1.4, 5.6, [2.8, 1.3, 1.5], 11, [], 0.4);
stat(s, 6.5, 1.4, 3, '27% → 17%', 'win rate FY24 → FY26');
stat(s, 6.5, 2.55, 3, '118% → 99%', 'net revenue retention, same period', ORANGE);
stat(s, 6.5, 3.7, 3, '₹389 cr', 'FY29 ARR if nothing changes', ORANGE);
src(s, 'Source: D1 diagnostic memo; DR1 cleaned CRM; DR2/DR3.');
note(s, 'Doing nothing is not flat: the base still grows but falls ₹133 crore short of the board path by FY29.');
// 3 plan
s = base('Five programmes, each tied to a number in the model', 'The plan (D2–D6)');
tbl(s, [['Programme', 'FY27 ₹ cr', 'Moves', 'FY26 → FY29'], ['Target the right 400 + 1,100 accounts', 'existing budget', 'Win mix; pipeline supply', '+2.9 pts; 392 → 470 deals'], ['Win-rate and price discipline', '1.9', 'Win rate; discount; cycle', '17.1% → 22.5%; 19.3% → 15%'], ['Retention and Helix defence (incl. Vajra)', '5.6', 'Churn; expansion', '5.9% → 4.0%; 8.1% → 10.5%'], ['AE capacity: hire to pipeline, retain', '3.0', 'Ramped AEs; attrition', '64 → 83; 29% → 20%'], ['Selective channel: SEA, Gulf, OEM', '2.8', 'Partner ARR', '₹2.6 → 19.7 cr'], ['RevOps, forecasting, sensor-agnostic readiness', '1.6', 'Forecast; hardware mix', 'MAPE 27% → 16%']], 0.5, 1.4, 9, [3.2, 1.2, 2.2, 2.4], 10.5, [], 0.4);
src(s, 'Source: D7 Investment and Assumptions sheets.'); note(s, 'Every programme has a driver in the model and a trigger at Q2.');
// 4 ARR
s = base('The plan reaches the board’s FY29 ARR; FY27 falls short because Q1 was already locked and new AEs take a year to ramp', 'What it delivers (D7)');
img(s, 'arr_path.png', 0.5, 1.35, 5.8);
tbl(s, [['', 'FY27', 'FY28', 'FY29'], ['ARR ₹ cr', '351', '423', '526'], ['Growth', '13.2%', '20.4%', '24.3%'], ['Board path', '15%', '20%', '22%'], ['NRR', '99.1%', '101.9%', '103.8%'], ['EBITDA ₹ cr', '(25.9)', '2.6', '52.6']], 6.5, 1.4, 3, [1.2, 0.6, 0.6, 0.6], 10);
s.addText('+3 pts of win rate alone lifts FY27 to 14.9%.', { x: 6.5, y: 3.4, w: 3, h: 0.6, fontFace: BF, fontSize: 11, color: INK, margin: 0 });
src(s, 'Source: D7 ARR_bridge, Scenarios.'); note(s, 'FY27 gap ₹5.6 cr. Closing it costs the extra ₹3 cr, which does not pay back within 15 months.');
// 5 ask
s = base('The ask: ₹14.95 crore, 6 AEs, 3 channel roles, and a gated reserve', 'Exact approval requested');
tbl(s, [['Item', 'Amount', 'Timing', 'Condition'], ['Programmes (retention, win-rate, AE retention, RevOps, readiness)', '₹7.3 cr', 'From Q2 FY27', 'Approved now'], ['Channel foundation + partner incentives', '₹2.8 cr', 'From Q2 FY27', 'Approved now'], ['6 net new AEs', '₹2.0 cr', 'Start Q3 FY27', 'Offers by 31 Aug'], ['Vajra retention plan (Inject 4)', '₹0.9 cr', 'Now', 'Defensive'], ['Reserve: 2nd retention squad + SE pilots', '₹1.9 cr', 'Q3 FY27', 'Only if Q2 triggers met'], ['Total FY27', '₹14.95 cr', '', 'Envelope ₹15 cr'], ['Exception', 'Q1 FY27 CAC payback 31.0 months', '', 'Quarter already locked']], 0.5, 1.4, 9, [3.4, 1.9, 1.5, 2.2], 10.5, [6], 0.4);
src(s, 'Source: D7 Investment sheet.'); note(s, 'FY28 and FY29 hiring are not approved today; they are released against the 90% capacity-use rule.');
// 6 30/60/90 + stop
s = base('First 90 days, and what we stop doing', 'Execution');
box(s, 0.5, 1.35, 4.35, 3.55, '30 / 60 / 90 days', '• 30: tiers in territories; discount cap 15%; Commit = stage 5; P05/P11 restricted; Vajra CEO meeting\n• 60: retention squad live; value-selling training; 3 partners signed; AE offers out\n• 90: Q2 review gate: release or hold reserve; Vajra business review delivered', BLUE);
box(s, 5.15, 1.35, 4.35, 3.55, 'We stop', '• AEs on 1,600 low-touch accounts\n• Discounts above 15% without CFO; matching “free”\n• Commit calls before stage 5\n• Planning on a 6-month ramp\n• Dormant partners; partner margin hidden in S&M\n• Hiring AEs to quota rather than pipeline', ORANGE);
note(s, 'The stop list is where the real behaviour change is.');
// 7 risks
s = base('Three largest risks, and the fallback for each', 'Risk');
tbl(s, [['Risk', 'Probability', 'Impact', 'Fallback'], ['Helix pressure deeper (churn +2 pts)', '35%', '−₹23 cr FY29 ARR', 'Second squad; win-back Apr 2027; sensor-agnostic tier'], ['Win-rate programme stalls (−3 pts)', '30%', '−₹26 cr; payback breach at −0.7 pts', 'Hold reserve; CFO-capped path'], ['Hardware mix does not fall', '35%', 'GM 64.5% by FY29 (floor 66%)', 'Hardware price floor; software-led expansion; sensor-agnostic tier']], 0.5, 1.4, 9, [2.8, 1.1, 2.3, 2.8], 11, [], 0.55);
img(s, 'tornado.png', 1.5, 3.5, 6.2);
note(s, 'Win rate and churn dominate; hardware mix is the margin risk nobody priced.');
// 8 measures
s = base('Measures that tell the board to continue, adjust or stop at Q2 FY27', 'Governance');
tbl(s, [['Measure', 'Q2 threshold', 'If missed'], ['Qualified win rate (rolling 2 quarters)', '≥ 18.0%', 'Hold ₹1.9 cr reserve'], ['New qualified direct deals', '≥ 95', 'Delay Q3 hires'], ['Churn + contraction, H1', '≤ ₹13.5 cr', 'Re-deploy squads'], ['Expansion ARR, H1', '≥ ₹12.5 cr', 'Re-scope top-30'], ['Quarterly CAC payback', '≤ 30 months', 'CFO-capped path'], ['Forecast error', '≤ 15%', 'Recalibrate'], ['Vajra', 'Not shortlisted on price', 'CEO escalation']], 0.5, 1.4, 9, [4, 2, 3], 11, [], 0.38);
s.addText('Stop rule: win rate below 17% and payback above 32 months at Q2 → no Q3 hires; return to board.', { x: 0.5, y: 4.6, w: 9, h: 0.4, fontFace: BF, fontSize: 11, bold: true, color: NAVY, margin: 0 });
note(s, 'All thresholds come from the plan path in the model.');
// 9 limits
s = base('What I am least sure of', 'Limits of the evidence');
box(s, 0.5, 1.35, 9, 3.55, 'Honest limits', '• Least sure: hardware attach falling from ₹1.48 to ₹1.05 per ₹1 of ARR; it alone decides the margin floor\n• Driver sizes are judgements anchored in D1–D6, not controlled tests; the plan still pays back if a third of the improvement arrives, but payback guardrails break below 78%\n• Interviews and external benchmarks are still being completed\n• Q1 forecast (₹8.71 cr) is locked and will be scored against actuals\n• All data synthetic', GREY);
note(s, 'Say this before the board does.');
// 10 close
s = base('Why believe the plan over doing nothing', 'Close');
stat(s, 0.5, 1.5, 3, '+₹137 cr', 'FY29 ARR vs do-nothing');
stat(s, 3.6, 1.5, 3, '8 months', 'payback of ₹62 cr three-year investment (10.5 on the strict test)', BLUE);
stat(s, 6.7, 1.5, 3, '1 of 12', 'guardrails breached, disclosed, with exception requested', ORANGE);
s.addText('Decision today: approve ₹14.95 cr, 6 AEs from Q3, 3 channel roles, the Q1 payback exception, and the Q2 gate.', { x: 0.5, y: 3.4, w: 9, h: 0.8, fontFace: HF, fontSize: 16, bold: true, color: NAVY, margin: 0 });
note(s, 'End on the decision.');
pres.writeFile({ fileName: 'out/D8_Board_Deck.pptx' }).then(() => console.log('ok'));
