const pptxgen = require('pptxgenjs');
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.title = 'Strata Sense D2: Account Planning and Lead Generation';
const NAVY = '1F3A5F', BLUE = '2A78D6', ORANGE = 'EB6834', AQUA = '1BAF7A', GREY = 'A3A29C', INK = '1A1A1A', INK2 = '52514E', BG = 'F7F6F2', WHITE = 'FFFFFF';
const HF = 'Cambria', BF = 'Calibri';
function base(title, kicker) {
  const s = pres.addSlide(); s.background = { color: WHITE };
  if (kicker) s.addText(kicker.toUpperCase(), { x: 0.5, y: 0.25, w: 9, h: 0.25, fontFace: BF, fontSize: 10, bold: true, color: ORANGE, charSpacing: 2, margin: 0, isTextBox: true });
  s.addText(title, { x: 0.5, y: 0.48, w: 9, h: 0.75, fontFace: HF, fontSize: 22, bold: true, color: NAVY, margin: 0, valign: 'top', isTextBox: true });
  s.addText('Strata Sense (fictional) · D2', { x: 0.5, y: 5.3, w: 5, h: 0.2, fontFace: BF, fontSize: 8, color: GREY, margin: 0, isTextBox: true });
  return s;
}
function stat(s, x, y, w, big, label, col = NAVY) {
  s.addText(big, { x, y, w, h: 0.55, fontFace: HF, fontSize: 28, bold: true, color: col, margin: 0, isTextBox: true });
  s.addText(label, { x, y: y + 0.55, w, h: 0.5, fontFace: BF, fontSize: 11, color: INK2, margin: 0, valign: 'top', isTextBox: true });
}
function tbl(s, rows, x, y, w, colW, fs = 10.5, hl = []) {
  const data = rows.map((r, i) => r.map((c, j) => ({ text: String(c), options: { fontFace: BF, fontSize: fs, bold: i === 0 || hl.includes(i), color: i === 0 ? WHITE : INK,
    fill: { color: i === 0 ? NAVY : (i % 2 ? WHITE : BG) }, align: j === 0 ? 'left' : 'left', valign: 'middle' } })));
  s.addTable(data, { x, y, w, colW, border: { type: 'solid', pt: 0.5, color: 'D9D8D2' }, margin: 0.05, rowH: 0.26 });
}
const note = (s, t) => s.addNotes(t);
const src = (s, t) => s.addText(t, { x: 0.5, y: 5.05, w: 9, h: 0.22, fontFace: BF, fontSize: 8, italic: true, color: INK2, margin: 0, isTextBox: true });

// 1 Title
let s = pres.addSlide(); s.background = { color: NAVY };
s.addText('D2 · ENTERPRISE ACCOUNT PLANNING AND LEAD GENERATION', { x: 0.6, y: 0.7, w: 8.8, h: 0.3, fontFace: BF, fontSize: 11, bold: true, color: 'F4B393', charSpacing: 2, margin: 0, isTextBox: true });
s.addText('Put 64 AEs on the 400 accounts that pay back, and stop working the 1,600 that don’t', { x: 0.6, y: 1.1, w: 8.6, h: 1.5, fontFace: HF, fontSize: 30, bold: true, color: WHITE, margin: 0, valign: 'top', isTextBox: true });
[['400 / 1,100 / 1,600', 'strategic / scaled / low-touch accounts'], ['34% vs 12%', 'past win rate, strategic vs low-touch tier'], ['₹49.4 cr', 'FY27 new-logo capacity vs ₹46.5 cr needed']].forEach((a, i) => {
  s.addText(a[0], { x: 0.6 + i * 3.0, y: 3.2, w: 2.8, h: 0.5, fontFace: HF, fontSize: 22, bold: true, color: WHITE, margin: 0, isTextBox: true });
  s.addText(a[1], { x: 0.6 + i * 3.0, y: 3.7, w: 2.7, h: 0.5, fontFace: BF, fontSize: 11, color: 'CADCFC', margin: 0, valign: 'top', isTextBox: true }); });
s.addText('Revenue Strategy Lead · Office of the CRO · Week 3, FY27 · Strata Sense Technologies is fictional; data synthetic', { x: 0.6, y: 4.9, w: 8.8, h: 0.3, fontFace: BF, fontSize: 9, color: 'CADCFC', margin: 0, isTextBox: true });
note(s, 'D1 found that effort goes to the wrong accounts: low-fit accounts get most AE time and win about 10%. D2 fixes where we play. Headline: tier the 3,100 accounts, put named AEs on 400 strategic accounts, run 1,100 as scaled territory, and move 1,600 to SDR, inside sales, marketing and SEA partners. With the same 64 AEs this covers the FY27 new-logo need with a thin margin, and only if multi-threading improves.');

// 2 Problem
s = base('AE time goes where the revenue isn’t: low-touch accounts take 63% of touches but yield 12% of won ARR', 'The problem (from D1)');
s.addChart(pres.charts.BAR, [{ name: 'Share of FY26 AE touches', labels: ['Strategic (400)', 'Scaled (1,100)', 'Low-touch (1,600)'], values: [0.085, 0.290, 0.625] },
  { name: 'Share of FY24–26 won ARR', labels: ['Strategic (400)', 'Scaled (1,100)', 'Low-touch (1,600)'], values: [0.511, 0.365, 0.124] }],
  { x: 0.5, y: 1.35, w: 5.6, h: 3.6, barDir: 'col', barGrouping: 'clustered', chartColors: [GREY, BLUE], showValue: true, dataLabelFormatCode: '0%', dataLabelFontSize: 10, dataLabelColor: INK,
    valAxisHidden: true, valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, catAxisLabelColor: INK2, catAxisLabelFontSize: 10, showLegend: true, legendPos: 'b', legendFontSize: 10, barGapWidthPct: 60 });
stat(s, 6.5, 1.5, 3, '8.5%', 'of AE touches went to the strategic tier, which produced half of past won ARR');
stat(s, 6.5, 2.7, 3, '61%', 'of touches went to low-fit accounts, which win about 10% (D1)', ORANGE);
stat(s, 6.5, 3.9, 3, '23.7%', 'of target accounts have more than one contact engaged');
src(s, 'Source: DR2 target_accounts (touches FY26); DR1 clean qualified deals FY24–26 scored with the D2 tiers.');
note(s, 'Same tiers applied backwards to past deals. The strategic tier held 21% of past qualified deals but 51% of won ARR. Today it gets 8.5% of AE touches. The low-touch tier gets 62.5% of touches and produced 12% of won ARR. This is the H1 finding in one picture.');

// 3 Scoring model
s = base('One score: probability of winning × likely first-year value, built only from firmographics', 'Ideal customer profile and scoring model');
const comp = [['Fit: P(win | qualified)', 'Logit on segment, revenue band, installed assets, Helix incumbent, region. Trained FY24–25; out-of-time AUC 0.65 on FY26.', BLUE],
  ['Whitespace: expected 1st-yr ARR', 'Log-linear model on won deals: installed assets drive deal size (R² 0.51). Strategic median ≈ ₹1 cr.', AQUA],
  ['Helix exposure', 'Helix-incumbent win rate fell 20% → 7%. Cap at 40 named accounts; 85 held until a pricing decision.', ORANGE],
  ['Likely need (overlay)', 'Existing monitoring: none/route-based = high need; wireless third-party = TrueSense risk. Not in the score (see below).', GREY]];
comp.forEach((c, i) => { const y = 1.35 + i * 0.82;
  s.addShape(pres.shapes.OVAL, { x: 0.5, y: y + 0.08, w: 0.42, h: 0.42, fill: { color: c[2] }, line: { color: c[2] } });
  s.addText(String(i + 1), { x: 0.5, y: y + 0.08, w: 0.42, h: 0.42, fontFace: HF, fontSize: 14, bold: true, color: WHITE, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
  s.addText(c[0], { x: 1.1, y, w: 4.6, h: 0.3, fontFace: BF, fontSize: 13, bold: true, color: INK, margin: 0, isTextBox: true });
  s.addText(c[1], { x: 1.1, y: y + 0.3, w: 4.6, h: 0.5, fontFace: BF, fontSize: 10.5, color: INK2, margin: 0, valign: 'top', isTextBox: true }); });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.0, y: 1.35, w: 3.5, h: 3.2, fill: { color: BG }, line: { color: 'D9D8D2' }, rectRadius: 0.08 });
s.addText([{ text: 'Score = P(win) × expected ARR', options: { bold: true, fontSize: 13, color: NAVY, breakLine: true } },
  { text: ' ', options: { fontSize: 6, breakLine: true } },
  { text: 'Why need is not in the score: ', options: { bold: true, fontSize: 10.5, color: INK } },
  { text: 'the monitoring field is blank for every account that became a customer. Using it would make the back-test look perfect for the wrong reason (data leakage). It guides the play, not the rank.', options: { fontSize: 10.5, color: INK2, breakLine: true } },
  { text: ' ', options: { fontSize: 6, breakLine: true } },
  { text: 'What the score cannot see: ', options: { bold: true, fontSize: 10.5, color: INK } },
  { text: 'buying intent and relationships. Tiers are reviewed each quarter with AE input.', options: { fontSize: 10.5, color: INK2 } }],
  { x: 6.2, y: 1.5, w: 3.1, h: 2.9, fontFace: BF, margin: 0, valign: 'top', isTextBox: true });
src(s, 'Source: DR1 clean deals, DR2 firmographics. Models in D2 workbook (README) and d2_score.py.');
note(s, 'Four ingredients the brief asks for: fit, likely need, whitespace and Helix exposure. Fit and whitespace are in the score. Helix exposure is a cap because the evidence says those deals rarely win today. Need is an overlay only: the condition-monitoring field is missing for all customers, so including it would leak the outcome.');

// 4 Backtest
s = base('The score predicts past wins: strategic-tier deals won 3x as often and were 3x larger than low-touch deals', 'Back-test');
s.addChart(pres.charts.BAR, [{ name: 'FY24–26 (all)', labels: ['Strategic', 'Scaled', 'Low-touch'], values: [0.340, 0.206, 0.122] },
  { name: 'FY26 only (out of time)', labels: ['Strategic', 'Scaled', 'Low-touch'], values: [0.259, 0.196, 0.113] }],
  { x: 0.5, y: 1.35, w: 5.4, h: 3.6, barDir: 'col', barGrouping: 'clustered', chartColors: [NAVY, BLUE], showValue: true, dataLabelFormatCode: '0%', dataLabelFontSize: 10,
    valAxisHidden: true, valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, catAxisLabelColor: INK2, showLegend: true, legendPos: 'b', legendFontSize: 10, showTitle: true, title: 'Win rate on qualified deals', titleFontSize: 11, titleColor: INK2, barGapWidthPct: 60 });
tbl(s, [['Tier', 'Deals', 'Avg won deal', 'ARR per qual. opp'], ['Strategic', '256', '₹71 lakh', '₹24.3 lakh'], ['Scaled', '480', '₹45 lakh', '₹9.3 lakh'], ['Low-touch', '482', '₹26 lakh', '₹3.1 lakh']], 6.2, 1.5, 3.3, [0.95, 0.6, 0.85, 0.9], 10);
s.addText('A qualified opportunity in a strategic account is worth 8x one in a low-touch account. Out-of-time AUC 0.65: good enough to tier accounts, not to predict single deals.', { x: 6.2, y: 2.75, w: 3.3, h: 1.4, fontFace: BF, fontSize: 11, color: INK, margin: 0, valign: 'top', isTextBox: true });
src(s, 'Source: 1,218 qualified closed deals FY24–26 (DR1 clean). Score trained on FY24–25 only; FY26 is the honest test.');
note(s, 'The panel asked for a test showing the score predicts past wins. FY26 is out of time: the model never saw it. Win rate falls steadily from strategic to low-touch, and deal size too, so value per qualified opportunity differs eight-fold.');

// 5 Tiering
s = base('Tiering the 3,100 accounts: 400 named, 1,100 territory, 1,600 off the AE’s desk', 'Tiers and plays');
tbl(s, [['Tier', 'Accounts', 'Who covers', 'Plays inside the tier'],
  ['1 Strategic', '400', 'Named AE (14 each) + SE + ABM', '40 named Helix displacements; written account plans; ≥4 contacts'],
  ['2 Scaled', '1,100', 'Territory AE (50 each) + SDR', '85 Helix accounts held for pricing decision; 348 with wireless sensors flagged TrueSense-risk (all tiers)'],
  ['3 Low-touch', '1,600', 'SDR, inside sales, marketing, partners', '488 SEA accounts partner-led; 781 India low-fit accounts on a stop-list (nurture only)']], 0.5, 1.4, 9, [1.2, 0.9, 2.5, 4.4], 10.5);
[['298 / 72 / 30', 'strategic accounts: India / Middle East / SEA'], ['₹96.5 cr', 'expected value in the strategic tier (EV = P(win) × ARR)'], ['781', 'accounts AEs stop prospecting']].forEach((a, i) => stat(s, 0.5 + i * 3.1, 3.35, 2.9, a[0], a[1], i === 2 ? ORANGE : NAVY));
src(s, 'Source: D2 workbook, Tiering sheet (all 3,100 accounts with score, tier, play and assigned AE).');
note(s, 'Thresholds: top 400 by expected value are strategic, next 1,100 scaled, remaining 1,600 low-touch. Helix-incumbent accounts are capped at 40 in the strategic tier because the FY26 win rate there was 7%. 99 accounts still sit with departed AEs and are reassigned in the new model.');

// 6 Coverage
s = base('Coverage: 64 AEs are enough if nobody carries low-touch accounts', 'Coverage model');
tbl(s, [['Role', 'AEs', 'Accounts', 'Accounts per AE'], ['Strategic named AEs', '29', '400', '14'], ['Scaled territory AEs', '22', '1,100', '50'], ['Inside-sales pool (low-touch)', '4', '1,600', '400 (no named owner)'],
  ['Ramping AEs (first 6 months)', '9', '—', 'shadow strategic; scaled overflow'], ['Total', '64', '3,100', '']], 0.5, 1.4, 5.4, [2.3, 0.7, 1.0, 1.4], 11, [5]);
s.addText([{ text: 'Rules', options: { bold: true, fontSize: 13, color: NAVY, breakLine: true } },
  { text: 'Strategic AEs carry no inbound from low-touch accounts.', options: { bullet: true, breakLine: true } },
  { text: 'SEA: partners lead; 2 of today’s SEA AEs become partner-facing co-sellers (channel roles sit in D6).', options: { bullet: true, breakLine: true } },
  { text: 'Tier review each quarter; an account moves up only with a qualified opportunity or new intent signal.', options: { bullet: true, breakLine: true } },
  { text: 'Accounts per AE (14 / 50) are assumptions to test in RevOps interviews.', options: { bullet: true } }],
  { x: 6.2, y: 1.4, w: 3.3, h: 3.4, fontFace: BF, fontSize: 11, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 6, isTextBox: true });
src(s, 'Source: D2 workbook, Coverage sheet. Ramping AEs: DR3 roster (9 AEs hired in the last 6 months).');
note(s, 'The brief asks to prove 64 to 76 AEs can cover the plan. At 14 strategic accounts and 50 scaled accounts per AE we need 51 AEs with named accounts, plus a 4-person inside pool and 9 ramping reps: exactly 64.');

// 7 Capacity
s = base('Capacity: ₹49.4 cr of new-logo capacity vs ₹46.5 cr needed; hiring 12 more AEs adds only ₹1.1 cr in FY27', 'Can the plan be delivered?');
const wlab = ['Baseline (64 AEs)', '+ Re-tiering', '+ Multi-threading', '+ SEA partners', 'FY27 capacity', 'Need (15% growth)'];
const vis = [40.9, 2.7, 1.8, 4.0, 49.4, 46.5], basev = [0, 40.9, 43.6, 45.4, 0, 0];
s.addChart(pres.charts.BAR, [{ name: 'base', labels: wlab, values: basev }, { name: 'value', labels: wlab, values: vis }],
  { x: 0.5, y: 1.35, w: 6.0, h: 3.6, barDir: 'col', barGrouping: 'stacked', chartColors: ['FFFFFF', BLUE], showValue: false, valAxisHidden: true, valGridLine: { style: 'none' },
    catGridLine: { style: 'none' }, catAxisLabelColor: INK2, catAxisLabelFontSize: 9, showLegend: false, barGapWidthPct: 40 });
vis.forEach((v, i) => s.addText((i > 0 && i < 4 ? '+' : '') + '₹' + v.toFixed(1), { x: 0.5 + 0.35 + i * 0.93, y: 1.45 + (1 - (basev[i] + v) / 55) * 3.0 - 0.28, w: 0.8, h: 0.25, fontFace: BF, fontSize: 10, bold: true, color: INK, align: 'center', margin: 0, isTextBox: true }));
s.addText([{ text: 'Margin is thin: ₹2.9 cr (6%).', options: { bold: true, breakLine: true } },
  { text: 'Only 40% of FY27 bookings come from pipeline created after re-tiering (8-month cycle). The full effect arrives in FY28: ₹52 cr direct at the same headcount.', options: { breakLine: true } },
  { text: ' ', options: { fontSize: 5, breakLine: true } },
  { text: 'Hiring: ', options: { bold: true } }, { text: '12 extra AEs cost ~₹6 cr a year but add ₹1.1 cr in FY27 because new AEs book nothing for 6 months. Decide in D7 whether to hire in H2 for FY28.', options: {} }],
  { x: 6.7, y: 1.4, w: 2.8, h: 3.5, fontFace: BF, fontSize: 11, color: INK, margin: 0, valign: 'top', isTextBox: true });
src(s, 'Baseline: DR3 productivity by tenure × FY27 AE supply (29% attrition, backfilled). Need assumes FY27 NRR 100% (provisional; D7 reconciles).');
note(s, 'Baseline equals FY26 productivity applied to the FY27 tenure mix: 40.9 crore, about the same as FY26 actual of 41. Re-tiering adds 2.7 because AEs stop spending time on low-touch accounts. Multi-threading adds 1.8 using half of the observed win-rate gap. SEA partners add 4.0, up from 2.6. If NRR stays at 99%, the need rises by about 3.4 crore and the margin disappears: retention is part of the new-logo plan.');

// 8 Lead gen
s = base('Working backwards from ₹46.5 cr: 307 qualified opportunities and about 1,900 leads', 'Lead-generation plan');
[['₹46.5 cr', 'new-logo ARR needed'], ['≈ 70', 'won deals (63 direct, ~6 partner)'], ['307', 'qualified opportunities'], ['458', 'opportunities created'], ['≈ 1,935', 'leads']].forEach((a, i) => {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5 + i * 1.83, y: 1.35, w: 1.7, h: 0.95, fill: { color: i === 0 ? NAVY : BG }, line: { color: 'D9D8D2' }, rectRadius: 0.06 });
  s.addText(a[0], { x: 0.5 + i * 1.83, y: 1.4, w: 1.7, h: 0.45, fontFace: HF, fontSize: 18, bold: true, color: i === 0 ? WHITE : NAVY, align: 'center', margin: 0, isTextBox: true });
  s.addText(a[1], { x: 0.55 + i * 1.83, y: 1.85, w: 1.6, h: 0.4, fontFace: BF, fontSize: 9.5, color: i === 0 ? 'CADCFC' : INK2, align: 'center', margin: 0, valign: 'top', isTextBox: true }); });
tbl(s, [['Source', 'Qual. opps', 'Opp → qual.', 'Lead → opp', 'Cost / qual. opp', 'Cost'],
  ['ABM (strategic)', '39', '70%', '25%', '₹10.0 lakh', '₹3.9 cr'], ['SDR / digital / outbound', '129', '67%', '15%', '₹7.2 lakh', '₹9.3 cr'],
  ['Events', '10', '70%', '10%', '₹36.9 lakh', '₹3.6 cr'], ['Customer referral', '32', '66%', '50%', '₹4.1 lakh', '₹1.3 cr'],
  ['AE self-sourced', '81', '68%', '—', 'AE time', '—'], ['Partner-sourced (SEA)', '16', '58%', '40%', '₹1.8 lakh', '₹0.3 cr']], 0.5, 2.5, 9, [2.4, 1.1, 1.1, 1.1, 1.5, 1.8], 10);
src(s, 'Opp → qualified: DR1 FY26 by source. Lead → opp and ABM cost: assumptions (the CRM has no lead data). SDR cost includes SDR pay (₹3.08 cr). Funnel sheet in the D2 workbook.');
note(s, 'The plan needs fewer qualified opportunities than FY26 (307 vs 432) because the mix shifts to higher-value accounts: about 100 strategic, 130 scaled and under 60 low-touch, versus 203 low-touch in FY26. That is the stop-doing in numbers. Events cost 37 lakh per qualified opportunity and event deals won 9% in FY26, so event volume is cut hardest.');

// 9 Budget
s = base('Same ₹24 cr programme budget, moved from trade events to ABM, referrals and SEA partners', 'Budget reallocation');
const bl = ['Trade events', 'ABM (strategic)', 'Digital & content', 'Outbound data & tools', 'Customer & referral', 'SEA partner MDF', 'Analyst & PR', 'Other'];
s.addChart(pres.charts.BAR, [{ name: 'FY26 actual', labels: bl, values: [9.6, 0, 5.3, 3.1, 1.2, 0, 1.9, 2.9] }, { name: 'FY27 proposed', labels: bl, values: [4.5, 4.0, 4.5, 3.1, 2.5, 1.5, 1.2, 2.7] }],
  { x: 0.5, y: 1.3, w: 6.2, h: 3.7, barDir: 'bar', barGrouping: 'clustered', chartColors: [GREY, BLUE], showValue: true, dataLabelFormatCode: '0.0', dataLabelFontSize: 9,
    valAxisHidden: true, valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, catAxisLabelColor: INK2, catAxisLabelFontSize: 9.5, showLegend: true, legendPos: 'b', legendFontSize: 10, barGapWidthPct: 40, catAxisOrientation: 'maxMin' });
s.addText([{ text: 'Why', options: { bold: true, fontSize: 13, color: NAVY, breakLine: true } },
  { text: 'Events: ₹37 lakh per qualified opp; 9% win rate.', options: { bullet: true, breakLine: true } },
  { text: 'Referral deals win 24–38% and cost ₹4 lakh per opp.', options: { bullet: true, breakLine: true } },
  { text: 'SEA partner deals win 34% vs 10% direct.', options: { bullet: true, breakLine: true } },
  { text: 'ABM funds research and exec events for the 400 named accounts.', options: { bullet: true, breakLine: true } },
  { text: '₹3–4 cr of programme spend is not tied to any plan source: a candidate to fund plan initiatives if the CFO trims the envelope.', options: { bullet: true } }],
  { x: 6.9, y: 1.35, w: 2.6, h: 3.6, fontFace: BF, fontSize: 10.5, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 5, isTextBox: true });
src(s, 'Source: DR3 marketing_programmes (FY26 ₹24.0 cr). Budget sheet in the D2 workbook.');
note(s, 'CMO scepticism about attribution: this plan does not need perfect attribution. It moves money toward sources where FY26 cost per qualified opportunity and win rate are both better, and it measures ABM by strategic-tier pipeline created, not by leads.');

// 10 Threading
s = base('Fixing single-threading: ≥4 contacts on every strategic deal before it can reach proposal', 'Single-threading fix');
stat(s, 0.5, 1.4, 2.8, '50% vs 29%', 'strategic-tier win rate with 3+ contacts vs fewer (FY24–26)', BLUE);
stat(s, 0.5, 2.6, 2.8, '18.5%', 'of FY26 strategic deals had 3+ contacts', ORANGE);
stat(s, 0.5, 3.8, 2.8, '73%', 'of open pipeline is single-threaded today');
tbl(s, [['Rule', 'Strategic', 'Scaled'], ['Contacts by stage 3', '≥4, incl. economic buyer, finance or procurement, IT security', '≥3, incl. one budget holder'],
  ['Gate', 'Cannot enter 4-Proposal without a finance contact logged', 'Cannot enter 4-Proposal with 1 contact'],
  ['Target share (Q4 FY27)', '50% with 3+ (from 18.5%)', '35% with 3+ (from 15%)'],
  ['Measured', 'Weekly: % of stage 3+ deals meeting the rule, by AE', 'Weekly, same report']], 3.5, 1.4, 6.0, [1.5, 2.5, 2.0], 10);
s.addText('Only half of the observed gap is counted in the capacity plan: part of it is selection (strong deals attract more contacts).', { x: 3.5, y: 4.2, w: 6.0, h: 0.6, fontFace: BF, fontSize: 10.5, italic: true, color: INK2, margin: 0, isTextBox: true });
src(s, 'Source: DR1 clean qualified deals by tier and contacts engaged; D1 odds ratio 2.2 for 3+ contacts after controls.');
note(s, 'The brief asks for a target number of contacts per strategic opportunity and how it will be measured. Four contacts, including the economic buyer, finance or procurement, and IT security, because FY26 committees include those roles on 71% of deals.');

// 11 Account plans
s = base('Three account plans: one expansion, one Helix displacement, one never-touched whitespace account', 'Strategic account plans');
const plans = [['Lotus Motors Ltd', 'Expansion · CU-1137', '₹7.48 cr ARR, flat 2 years; 97.5% usage; 35% of assets licensed. Co-term +3,000 assets with the 13 Aug renewal.', '+₹3.2 cr ARR', BLUE],
  ['Agni Renewables Industries', 'Helix displacement · T00084', '20 plants, Helix incumbent, route-based monitoring. Land a paid pilot on critical assets at one station; integrate, don’t replace.', '₹0.7 cr pilot · stop at day 90 without EB', ORANGE],
  ['Keystone Forgings Pvt Ltd', 'New logo · T02772', 'Highest fit in the tier, no monitoring, no Helix, zero contacts ever. Reference-led entry via an expanding customer.', '₹0.8 cr pilot → ₹1.0 cr', AQUA]];
plans.forEach((p, i) => { const x = 0.5 + i * 3.05;
  s.addShape(pres.shapes.RECTANGLE, { x, y: 1.4, w: 2.85, h: 3.45, fill: { color: BG }, line: { color: 'D9D8D2' } });
  s.addShape(pres.shapes.RECTANGLE, { x, y: 1.4, w: 2.85, h: 0.08, fill: { color: p[4] }, line: { color: p[4] } });
  s.addText(p[0], { x: x + 0.15, y: 1.6, w: 2.55, h: 0.35, fontFace: HF, fontSize: 14, bold: true, color: NAVY, margin: 0, isTextBox: true });
  s.addText(p[1], { x: x + 0.15, y: 1.95, w: 2.55, h: 0.25, fontFace: BF, fontSize: 10, bold: true, color: INK2, margin: 0, isTextBox: true });
  s.addText(p[2], { x: x + 0.15, y: 2.3, w: 2.55, h: 1.6, fontFace: BF, fontSize: 10.5, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText(p[3], { x: x + 0.15, y: 4.05, w: 2.55, h: 0.6, fontFace: BF, fontSize: 11.5, bold: true, color: p[4] === AQUA ? '0E7A53' : p[4], margin: 0, valign: 'top', isTextBox: true }); });
src(s, 'Each plan (2 pages): committee map, ₹ value hypothesis, MEDDPICC status, mutual action plan, 90-day plan. See D2_Account_Plans.');
note(s, 'All three committee maps have blank names: the CRM holds almost no contacts. That is the single-threading problem made visible, and filling those names is the first 30-day task in every plan.');

// 12 Stop doing
s = base('What we stop doing so AEs have time to run these plans', 'The panel question');
tbl(s, [['Stop', 'Frees', 'Evidence'],
  ['AE prospecting in 1,600 low-touch accounts (781 on a stop-list)', '~60% of AE touches', 'Low-touch: 12% win rate, 12% of won ARR'],
  ['Cutting trade events from ₹9.6 cr to ₹4.5 cr', '₹5.1 cr of budget', '₹37 lakh per qualified opp; 9% win'],
  ['Renewing large customers flat with no expansion proposal', 'Expansion upside', 'Top-30 expansion fell ₹21.3 → ₹9.5 cr'],
  ['Head-on Helix replacement pitches and discounting against the bundle', 'AE and SE time', '0 of 11 such proposals won in FY26'],
  ['Direct AE prospecting in SEA outside the strategic tier', '2 AEs → partner co-sell', 'SEA partner deals win 34% vs 10%'],
  ['Hiring 12 AEs in H1 FY27', '~₹6 cr a year', 'Adds ₹1.1 cr FY27 capacity (ramp)']], 0.5, 1.35, 9, [4.0, 1.8, 3.2], 10.5);
s.addText('Decisions needed: CRO approves tiers and stop-list; CMO approves budget moves; CFO notes the plan is capacity-neutral in FY27. Assumptions to validate: accounts per AE, ABM cost per opp, lead conversion rates.', { x: 0.5, y: 4.35, w: 9, h: 0.6, fontFace: BF, fontSize: 11, color: NAVY, bold: true, margin: 0, isTextBox: true });
note(s, 'Answer to the panel: we stop AE prospecting in 1,600 accounts, halve trade-event spend, stop flat renewals, stop head-on Helix pitches, move SEA to partners and do not hire ahead of ramp. Each stop is backed by a number from D1 or D2.');
pres.writeFile({ fileName: 'out/D2_Account_Planning_Deck.pptx' }).then(() => console.log('ok'));
