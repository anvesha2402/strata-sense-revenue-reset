const pptxgen = require('pptxgenjs');
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.title = 'Strata Sense D6: Channel Partner Expansion Strategy';
const NAVY = '1F3A5F', BLUE = '2A78D6', ORANGE = 'EB6834', AQUA = '1BAF7A', GREY = 'A3A29C', INK = '1A1A1A', INK2 = '52514E', BG = 'F7F6F2', WHITE = 'FFFFFF';
const HF = 'Cambria', BF = 'Calibri';
function base(title, kicker) {
  const s = pres.addSlide(); s.background = { color: WHITE };
  if (kicker) s.addText(kicker.toUpperCase(), { x: 0.5, y: 0.25, w: 9, h: 0.25, fontFace: BF, fontSize: 10, bold: true, color: ORANGE, charSpacing: 2, margin: 0, isTextBox: true });
  s.addText(title, { x: 0.5, y: 0.48, w: 9, h: 0.75, fontFace: HF, fontSize: 21, bold: true, color: NAVY, margin: 0, valign: 'top', isTextBox: true });
  s.addText('Strata Sense (fictional) · D6', { x: 0.5, y: 5.3, w: 5, h: 0.2, fontFace: BF, fontSize: 8, color: GREY, margin: 0, isTextBox: true });
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

// 1 Title
let s = pres.addSlide(); s.background = { color: NAVY };
s.addText('D6 · CHANNEL PARTNER EXPANSION STRATEGY', { x: 0.6, y: 0.7, w: 8.8, h: 0.3, fontFace: BF, fontSize: 11, bold: true, color: 'F4B393', charSpacing: 2, margin: 0, isTextBox: true });
s.addText('Build a small, selective channel for South-East Asia, the Gulf and machine builders, not more India resellers', { x: 0.6, y: 1.1, w: 8.6, h: 1.5, fontFace: HF, fontSize: 28, bold: true, color: WHITE, margin: 0, valign: 'top', isTextBox: true });
[['4 of 14', 'signed partners are active today; keep 4, fix 5, exit 5'], ['₹19.7 cr', 'FY29 partner-sourced ARR in plan = 25% of new logos (46% likely)'], ['₹0.24 cr', 'sourced ARR per partner per year below which the channel loses money']].forEach((a, i) => {
  s.addText(a[0], { x: 0.6 + i * 3.0, y: 3.2, w: 2.8, h: 0.5, fontFace: HF, fontSize: 22, bold: true, color: WHITE, margin: 0, isTextBox: true });
  s.addText(a[1], { x: 0.6 + i * 3.0, y: 3.7, w: 2.7, h: 0.6, fontFace: BF, fontSize: 11, color: 'CADCFC', margin: 0, valign: 'top', isTextBox: true }); });
s.addText('Revenue Strategy Lead · Office of the CRO · Week 7, FY27 · Strata Sense Technologies is fictional; data synthetic', { x: 0.6, y: 4.9, w: 8.8, h: 0.3, fontFace: BF, fontSize: 9, color: 'CADCFC', margin: 0, isTextBox: true });
note(s, 'The board objective is 25% of new-logo ARR from partners by FY29. Today it is about 6%, from 4 active partners out of 14 signed. D1 showed partners lose in India (12% win rate against 22% direct) but win in South-East Asia (34% against 10%). So the recommendation is a small, selective channel aimed where the direct team is weak: SEA, the Gulf, and machine builders who embed the sensor. The plan reaches 25% only if 17 partners are activated in FY27–28 and reach about ₹1.2 cr each. I put the odds of hitting 25% at roughly a coin flip, and I show when we stop if it is not working.');

// 2 Starting point
s = base('Partners help where we have no presence and hurt where our direct team is strong', 'Starting point (D1, DR6)');
s.addChart(pres.charts.BAR, [{ name: 'Direct', labels: ['India', 'South-East Asia'], values: [0.22, 0.10] }, { name: 'Partner-sourced', labels: ['India', 'South-East Asia'], values: [0.12, 0.34] }],
  { x: 0.5, y: 1.35, w: 5.0, h: 3.6, barDir: 'col', barGrouping: 'clustered', chartColors: [GREY, BLUE], showValue: true, dataLabelFormatCode: '0%', dataLabelFontSize: 11, dataLabelColor: INK,
    valAxisHidden: true, valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, catAxisLabelColor: INK2, catAxisLabelFontSize: 11, showLegend: true, legendPos: 'b', legendFontSize: 10,
    showTitle: true, title: 'Win rate on qualified deals, FY24–26', titleFontSize: 11, titleColor: INK2, barGapWidthPct: 60 });
stat(s, 6.0, 1.4, 3.5, '₹2.6 cr', 'partner-sourced new-logo ARR in FY26, about 6% of ₹41 cr (after re-tagging 36 mis-tagged deals)');
stat(s, 6.0, 2.55, 3.5, '10 of 14', 'signed partners inactive, occasional or never closed a deal', ORANGE);
stat(s, 6.0, 3.7, 3.5, '2 of 4', 'active partners also sell Helix (P05, P11), and they hold 53% of open partner pipeline', ORANGE);
src(s, 'Source: DR1 clean deals FY24–26 (D1 H5 test); DR6 partner file. Gulf: too few partner deals to measure.');
note(s, 'D1 rejected the idea that partners are a general fix. In India partner-sourced deals win half as often as direct deals, because the direct team already covers India and partners bring weaker, late-stage deals. In SEA it is the reverse: we have two AEs there and partners win three times as often. The partner base is mostly dormant, and two of the four active partners are tied to Helix, which matters for Inject 3.');

// 3 Role of channel
s = base('Partners take the reach, trust and services jobs that 64 AEs cannot do; strategic accounts stay direct', 'Role of the channel');
box(s, 0.5, 1.35, 4.35, 3.55, 'What partners do', '• South-East Asia and the Gulf: we have 2 AEs outside India; partners have local teams and language\n• Low-touch tier (1,600 accounts, D2): referral and resale where an AE visit does not pay back\n• Installation, integration with plant systems, and 24x7 service\n• Plant-floor trust: maintenance heads already buy from their integrator\n• Machine builders embed the sensor in new presses and compressors (PR09, PR10)', BLUE);
box(s, 5.15, 1.35, 4.35, 3.55, 'What stays direct', '• The 400 strategic accounts and the top-30 customers (₹127 cr ARR): named AEs own them; partners may deliver services only\n• India scaled tier: direct wins 22% against 12% for partners\n• Pricing, discount approval and the Helix-response offer (D5)\n• Renewals and expansion of direct-sold customers\n• Any account where a partner also sells Helix', NAVY);
src(s, 'Source: D2 tiering and coverage; D1 partner win rates; DR6.');
note(s, 'The test for each job is whether a partner does it better or cheaper than an AE. Reach outside India, services and embed are clear yes. Strategic accounts and India scaled accounts are clear no, on D1 evidence. Keeping the top-30 direct also protects the renewal base, which is where Helix pressure is highest.');

// 4 Types and mix
s = base('Five partner types, each with one job; by FY29 SEA/Gulf integrators and MSPs carry two-thirds of partner ARR', 'Partner types and target mix');
tbl(s, [['Partner type', 'Job', 'Where', 'Role / tier', 'FY29 mix'],
  ['System integrators', 'Sell, install, integrate', 'SEA, Gulf', 'Silver / Gold', '40%'],
  ['Managed-service providers', 'Sell and run monitoring as a service', 'SEA, Gulf, India-East', 'Gold (services)', '25%'],
  ['Machine builders (OEM embed)', 'Fit sensors to new machines', 'India national', 'Resell (embed)', '15%'],
  ['Regional value-added resellers', 'Resell to low-touch accounts', 'Singapore hub, SEA', 'Silver', '12%'],
  ['Automation distributors', 'Referral only; stock hardware', 'India', 'Referral', '8%']],
  0.5, 1.4, 9.0, [2.4, 2.6, 1.6, 1.4, 1.0], 10.5, [], 0.36);
s.addText('Distributors are kept to referral: in India they compete with our own scaled-tier AEs and three of the four distributor prospects or partners carry Helix or Orion lines. Machine builders are slow (about 12 months to first deal) but each has an installed base of 2,000+ machines.', { x: 0.5, y: 3.75, w: 9, h: 0.9, fontFace: BF, fontSize: 11, color: INK, margin: 0, valign: 'top', isTextBox: true });
src(s, 'Source: DR6 prospects (type, region, vendor lines, months to first deal); mix is a design choice in D6 workbook Inputs.');
note(s, 'The brief lists five partner types. Each gets one job and one tier so there is no overlap. The mix is a target, not a forecast; it drives the blended partner margin in the workbook.');

// 5 Keep fix exit
s = base('Keep 4, fix 5 against a dated condition, exit 5 that have produced almost nothing since FY24', 'Existing partners: keep, fix or exit');
tbl(s, [['Decision', 'Partners', 'Why'],
  ['Keep', 'P02 Deccan (Gold), P09 Vindhya (Gold services), P12 Siam, P13 Al Fajr (Silver)', '22% win rate and ₹4.2 cr pipeline (P02); ₹7.1 cr pipeline (P09); SEA/Gulf access (P12, P13)'],
  ['Fix: restricted', 'P05 Sahyadri, P11 Konkan', 'Real volume but Helix-tied (Inject 3). No registration in Helix-incumbent accounts; P11 referral-only until it passes the scorecard'],
  ['Fix: activate', 'P07 Mekong, P08 Hosur, P10 Penang', 'Signed, no deals. Certify 2 engineers and a joint pipeline plan by end-Q2, or exit. P08 joins the OEM-embed pilot'],
  ['Exit', 'P01, P03, P04, P06, P14 + P08 if pilot fails', 'Zero or one deal in three years; coverage moves to shortlisted prospects (PR07 for Saudi)']],
  0.5, 1.4, 9.0, [1.3, 3.2, 4.5], 10, [], 0.55);
s.addText('Exits cost nothing today, but each dormant partner can still register deals and claim margin. Removing them is also a conflict control.', { x: 0.5, y: 4.35, w: 9, h: 0.5, fontFace: BF, fontSize: 11, italic: true, color: INK2, margin: 0, isTextBox: true });
src(s, 'Source: DR6 signed partners (status, sourced/influenced ARR, win rates, pipeline, other vendor lines). Full list: workbook sheet Partners_14.');
note(s, 'Keep means the partner earns its tier today. Fix means there is a reason to keep them but a specific condition to meet by a date. Exit is for partners with no activity. P05 and P11 are the hard calls: they are our biggest partners by volume but also sell Helix. I keep them, restricted, rather than exit, because exiting would drop about half of FY26 partner-sourced ARR at once. Count: 4 keep, 5 fix (P05, P11, P07, P08, P10), 5 exit, with P08 converting to exit if the pilot fails.');

// 6 Prospects
s = base('Recruit six of the twelve prospects in FY27, led by two SEA integrators; drop the three Helix-affiliated ones', 'Prospective partners: scored shortlist');
tbl(s, [['Rank', 'Prospect', 'Type', 'Region', 'Score', 'Decision'],
  ['1', 'PR01 Java Integrasi Teknik', 'System integrator', 'Indonesia', '4.85', 'Recruit Q1'],
  ['2', 'PR02 Chao Phraya Automation', 'System integrator', 'Thailand', '4.65', 'Recruit Q1'],
  ['3', 'PR06 Merlion Industrial', 'Value-added reseller', 'Singapore hub', '4.50', 'Recruit Q1'],
  ['3', 'PR07 Arabian Asset Care', 'Managed services', 'Saudi Arabia', '4.50', 'Recruit Q2'],
  ['5', 'PR09 Tapti Press Machines', 'Machine builder', 'India', '4.40', 'Recruit: embed pilot'],
  ['6', 'PR10 Shivalik Compressors', 'Machine builder', 'India', '3.95', 'Recruit: embed pilot'],
  ['7–9', 'PR03, PR11, PR04', 'Managed services', 'VN, India-E, PH', '3.2–3.7', 'Hold for FY28'],
  ['10–12', 'PR08, PR05, PR12', 'Helix-affiliated', 'UAE, MY, India-S', '2.3–3.1', 'Deprioritise']],
  0.5, 1.35, 9.0, [0.6, 2.6, 1.7, 1.4, 0.8, 1.9], 10, [1, 2], 0.33);
s.addText('Weights: access to our target accounts 30%, conflict risk 20%, capability (engineers) 20%, vertical fit 15%, commitment 15%. A Helix affiliation scores 1 of 5 on conflict, which alone drops a prospect out of the top six.', { x: 0.5, y: 4.4, w: 9, h: 0.5, fontFace: BF, fontSize: 10, color: INK2, margin: 0, isTextBox: true });
src(s, 'Source: DR6 prospects; scores and weights in workbook sheet Prospects_12 (weights editable).');
note(s, 'Access carries the most weight because a partner that does not reach our target accounts adds nothing. Conflict risk is second because Inject 3 showed what happens when partners also sell Helix. PR05 would otherwise score well in Malaysia, but it is a Helix distributor. FY27 activations are these six plus the two reactivated partners P07 and P10, eight in total.');

// 7 Programme tiers
s = base('Three tiers, paid by role: 10% for a referral, 18% to resell, 22% plus services revenue for certified Gold partners', 'Programme design: tiers, margin and incentives');
tbl(s, [['', 'Referral', 'Silver (resell / co-sell)', 'Gold (resell + services)'],
  ['Year-1 margin on ARR', '10%', '18%', '22%'],
  ['Renewal margin (years 2–3)', '—', '8%', '10%'],
  ['Services revenue', '—', 'Installation only', 'Installation, integration, managed monitoring (keeps 100%)'],
  ['Entry requirement', 'Registered deal', '2 certified engineers, joint plan', '4 certified engineers, ₹1 cr sourced ARR in 12 months'],
  ['Market development funds', '—', 'Co-funded events', 'Up to 3% of sourced ARR'],
  ['Deal protection', '90 days', '90 days', '120 days']],
  0.5, 1.35, 9.0, [2.1, 1.5, 2.3, 3.1], 10, [], 0.36);
stat(s, 0.5, 4.0, 2.8, '16–18%', 'blended year-1 partner margin FY27–29, given the tier mix');
stat(s, 3.6, 4.0, 2.8, '₹1.64', 'direct S&M spent per ₹1 of new-logo ARR today, the cost partners replace', BLUE);
s.addText('Margin is paid on bookings once the customer pays the first invoice, never on registration.', { x: 6.7, y: 4.0, w: 2.8, h: 0.9, fontFace: BF, fontSize: 10.5, color: INK, margin: 0, valign: 'top', isTextBox: true });
src(s, 'Source: tier design and mix in workbook Inputs rows 19–23; S&M ratio from DR3 (allocation assumption: 70% of ₹96 cr S&M to new logos).');
note(s, 'Margins are set by the work the partner does, not by volume alone. A referral just brings a qualified lead. A reseller carries the sale. Gold partners also deliver services, which is where integrators make most of their money, so we let them keep services revenue rather than pay higher licence margin. Renewal margin keeps partners interested in retention but falls after year three.');

// 8 Deal registration and conflict rules
s = base('One owner per deal: registration decides who is protected, and every deal is counted once in bookings', 'Programme design: deal registration and conflict rules');
box(s, 0.5, 1.35, 2.9, 3.55, 'Deal registration', '• Partner registers named account, project and competitor lines they sell\n• Channel manager approves or rejects in 48 hours\n• Protection 90 days (Gold 120), renewable once with evidence of progress\n• First valid registration wins; direct AE opportunities created earlier take priority', BLUE);
box(s, 3.55, 1.35, 2.9, 3.55, 'Conflict rules', '• Strategic tier (400) and top-30 customers: direct only; partner can deliver services\n• Helix-incumbent accounts: no registration by Helix-tied partners\n• Channel manager rules on disputes within 5 working days; CRO decides appeals\n• A partner that switches a registered deal to a competitor loses tier immediately', ORANGE);
box(s, 6.6, 1.35, 2.9, 3.55, 'Direct team incentive', '• AE gets 50% quota credit on partner-sourced deals in their territory (comp only)\n• Bookings count once, as partner-sourced\n• No AE credit for deals in accounts they never touched\n• Partner-sourced ARR is a line in the forecast, owned by the VP Channel', AQUA);
src(s, 'Source: design choices. Counting rule matches D7 workbook (partner ARR is inside, not added to, total new-logo ARR).');
note(s, 'Channel conflict usually comes from AEs who lose credit and partners who lose protection. Fifty percent quota credit makes AEs neutral on partner deals without double counting bookings: the comp cost is in the direct-effort line of the channel P&L. The Helix rule is new after Inject 3.');

// 9 Enablement and ramp
s = base('A new partner takes 6–12 months to its first deal, so FY27 is mostly spent certifying and building pipeline', 'Certification, enablement and ramp');
const steps = [['Month 0–1', 'Sign, conflict check, joint account list from D2 low-touch and SEA territory'], ['Month 1–3', 'Certify 2 engineers (installation, TrueSense analytics); demo kit; first 10 joint account plans'],
  ['Month 3–6', 'Co-sell with SE on first 3 deals; register pipeline'], ['Month 6–12', 'First close (SIs, MSPs); machine builders at ~12 months'], ['Year 2', 'About 60% of mature productivity'], ['Year 3', 'Mature: about ₹1.2 cr sourced ARR a year']];
steps.forEach((t, i) => { const x = 0.5 + i * 1.52;
  s.addShape(pres.shapes.RECTANGLE, { x, y: 1.5, w: 1.42, h: 0.42, fill: { color: i < 4 ? BLUE : NAVY }, line: { color: WHITE } });
  s.addText(t[0], { x, y: 1.5, w: 1.42, h: 0.42, fontFace: BF, fontSize: 10.5, bold: true, color: WHITE, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
  s.addText(t[1], { x, y: 2.0, w: 1.42, h: 1.4, fontFace: BF, fontSize: 9.5, color: INK2, margin: 0.02, valign: 'top', isTextBox: true }); });
stat(s, 0.5, 3.6, 2.9, '15/60/100%', 'share of mature productivity in activation year / year 2 / year 3');
stat(s, 3.6, 3.6, 2.8, '₹1.2 cr', 'mature partner: ~10 qualified deals × 34% SEA win rate × ₹37 lakh', BLUE);
stat(s, 6.7, 3.6, 2.8, '₹0.4 cr', 'enablement and certification budget in FY27');
src(s, 'Source: DR6 months to first deal (6–12); D1 SEA partner win rate; FY26 average partner deal size. Ramp inputs are yellow assumptions in the workbook.');
note(s, 'The ramp is the most important assumption. DR6 says 6 to 12 months to first deal. I model a partner activated mid-year as producing 15% of mature output that year, 60% the next, and full output from year three. Mature productivity is built bottom-up from the SEA partner win rate. If the win rate is closer to India levels, productivity halves; slide 13 shows that case.');

// 10 Partners needed
s = base('25% of FY29 new logos needs 28 active partners, equal to 16 mature ones, so recruiting must happen in FY27–28', 'Ramp and active partners needed');
s.addChart(pres.charts.BAR, [
  { name: 'Existing partners', labels: ['FY27', 'FY28', 'FY29'], values: [2.26, 2.48, 2.73] },
  { name: 'FY27 recruits (8)', labels: ['FY27', 'FY28', 'FY29'], values: [1.44, 5.76, 9.60] },
  { name: 'FY28 recruits (9)', labels: ['FY27', 'FY28', 'FY29'], values: [0, 1.62, 6.48] },
  { name: 'FY29 recruits (5)', labels: ['FY27', 'FY28', 'FY29'], values: [0, 0, 0.90] }],
  { x: 0.5, y: 1.35, w: 5.4, h: 3.6, barDir: 'col', barGrouping: 'stacked', chartColors: [GREY, BLUE, AQUA, ORANGE], showValue: false,
    valAxisLabelFormatCode: '0', valAxisLabelFontSize: 9, valAxisLabelColor: INK2, valGridLine: { color: 'E6E5E0', size: 0.5 }, catGridLine: { style: 'none' }, catAxisLabelColor: INK2,
    showLegend: true, legendPos: 'b', legendFontSize: 9, showTitle: true, title: 'Partner-sourced new-logo ARR (₹ cr)', titleFontSize: 11, titleColor: INK2, barGapWidthPct: 50 });
tbl(s, [['', 'FY27', 'FY28', 'FY29'], ['Partner ARR (₹ cr)', '3.7', '9.9', '19.7'], ['Share of new logos', '7.9%', '15.9%', '25.3%'], ['Active partners', '14', '23', '28']], 6.2, 1.4, 3.3, [1.5, 0.6, 0.6, 0.6], 10.5, [2]);
s.addText('FY29 recruits add only ₹0.9 cr that year. If mature productivity is ₹1.0 cr rather than ₹1.2 cr, FY29 share is 21.6%; at ₹0.8 cr it is 18%.', { x: 6.2, y: 2.65, w: 3.3, h: 1.4, fontFace: BF, fontSize: 11, color: INK, margin: 0, valign: 'top', isTextBox: true });
src(s, 'Source: workbook sheet Partner_ramp. New-logo ARR plan: D2 (FY27 ₹46.5 cr), D4 base scenario (FY28 ₹62.1 cr, FY29 ₹78 cr).');
note(s, 'The board asks for 25% by FY29. Because of the ramp, what matters is how many partners we activate in FY27 and FY28, not FY29. The plan activates 8 in FY27 (six prospects and two reactivated partners) and 9 in FY28. That reaches 25.3%, only just. The sensitivity shows it is fragile: a 17% miss on productivity takes us to 21.6%.');

// 11 Channel P&L
s = base('Judged against the cost of selling direct, the channel costs ₹0.9 cr in FY27 and saves ₹11.7 cr by FY29', 'Channel profit and loss (₹ cr)');
tbl(s, [['', 'FY27', 'FY28', 'FY29'], ['Partner-sourced new-logo ARR', '3.70', '9.86', '19.71'], ['Partner margin (year-1 + renewals)', '0.61', '1.92', '4.42'], ['Channel team, enablement, PRM, MDF', '3.94', '5.46', '6.50'],
  ['Direct effort still used (AE co-sell, SE, 50% credit)', '2.43', '5.66', '9.70'], ['Total channel cost', '6.97', '13.04', '20.62'], ['Direct S&M cost avoided (₹1.64 per ₹1)', '6.06', '16.17', '32.32'],
  ['Saving / (extra cost) against direct', '(0.91)', '3.14', '11.71'], ['Incremental lens, first year only', '(4.45)', '(6.30)', '(7.15)']],
  0.5, 1.35, 6.0, [3.3, 0.9, 0.9, 0.9], 10, [5, 7], 0.31);
s.addText([{ text: 'Two honest lenses. ', options: { bold: true, breakLine: false } }, { text: 'If partner deals replace direct selling, the channel pays from FY28. If you count only first-year gross profit on deals the direct team would never win, it never pays in year one, because no subscription business does. On three-year value the FY29 cohort alone is worth ₹34 cr.', options: {} }],
  { x: 6.8, y: 1.4, w: 2.7, h: 3.3, fontFace: BF, fontSize: 11, color: INK, margin: 0, valign: 'top', isTextBox: true });
src(s, 'Source: workbook sheet Channel_PL. Direct S&M per ₹1 new-logo ARR is an allocation assumption (DR3).');
note(s, 'The panel asked for partner margin against the acquisition cost it saves. That is the substitution lens: partner deals would otherwise need AE and SE time costing ₹1.64 per rupee of new ARR. I also show the harsher incremental lens so nobody thinks I am hiding a loss. FY27 is a loss either way.');

// 12 GM floor
s = base('Partner margin costs about 0.7 points of gross margin by FY29, leaving 1.6 points above the 66% floor', 'Effect on blended gross margin');
s.addChart(pres.charts.BAR, [{ name: 'Gross margin after partner margin', labels: ['FY27', 'FY28', 'FY29'], values: [0.682, 0.679, 0.676] }],
  { x: 0.5, y: 1.35, w: 5.0, h: 3.6, barDir: 'col', chartColors: [BLUE], showValue: true, dataLabelFormatCode: '0.0%', dataLabelFontSize: 11, valAxisMinVal: 0.6, valAxisMaxVal: 0.7,
    valAxisLabelFormatCode: '0%', valAxisLabelFontSize: 9, valGridLine: { color: 'E6E5E0', size: 0.5 }, catGridLine: { style: 'none' }, catAxisLabelColor: INK2, showLegend: false, barGapWidthPct: 70,
    showTitle: true, title: 'Blended gross margin incl. partner margin (axis from 60%)', titleFontSize: 11, titleColor: INK2 });
stat(s, 6.0, 1.4, 3.5, '₹4.4 cr', 'partner margin in FY29, if booked against gross margin');
stat(s, 6.0, 2.55, 3.5, '₹14.0 cr', 'partner margin that would breach 66% in FY29, about 3x plan', AQUA);
s.addText('Today partner margin sits in S&M, outside gross margin. I book it against gross margin for the floor test so the guardrail is not met by an accounting choice.', { x: 6.0, y: 3.7, w: 3.5, h: 1.2, fontFace: BF, fontSize: 10.5, color: INK, margin: 0, valign: 'top', isTextBox: true });
src(s, 'Source: workbook sheet GM_floor. Revenue approximations replaced by D7 integrated model.');
note(s, 'The floor holds with room to spare. The bigger gross-margin risk is the Helix-response pricing in D5, not partner margin. D7 will combine both.');

// 13 Panel question
s = base('The channel loses money if active partners average under ₹0.24 cr a year; likely in FY27, unlikely by FY29 if we select well', 'Panel question: at what productivity does the channel lose money, and how likely is that?');
tbl(s, [['Probability the channel loses money (substitution lens)', 'FY27', 'FY28', 'FY29'], ['Plan case: 70% activation, median ₹1.0 cr per partner', '96%', '9%', '<1%'], ['Downside: partners like FY26 India partners', '100%', '91%', '44%'],
  ['P(25% share in FY29): plan case / downside', '', '', '46% / 0%']], 0.5, 1.45, 5.9, [3.5, 0.8, 0.8, 0.8], 10, [], 0.36);
stat(s, 6.7, 1.4, 2.8, '₹0.24 cr', 'break-even sourced ARR per active partner, FY29 (28 partners, ₹6.5 cr fixed cost)');
stat(s, 6.7, 2.55, 2.8, '₹0.19 cr', 'FY26 actual per signed partner: below break-even, because 10 of 14 are dormant', ORANGE);
s.addText('Kill gate at end-Q2 FY28: if fewer than 10 partners are active or trailing partner-sourced ARR is under ₹6 cr a year, stop recruiting, cut MDF, and return partner-manager budget to direct SEA hiring.', { x: 0.5, y: 3.45, w: 5.9, h: 1.0, fontFace: BF, fontSize: 11, bold: true, color: NAVY, margin: 0, valign: 'top', isTextBox: true });
src(s, 'Source: workbook sheets Breakeven and Risk_sim (Monte Carlo, 20,000 runs: activation rate, per-partner productivity, common market shock). Downside uses 45% activation and ₹0.45 cr median.');
note(s, 'Direct answer: break-even is about ₹0.24 cr of sourced ARR per active partner per year on the substitution basis, or about ₹6.7 cr of total partner ARR in FY29. The active partners in FY26 averaged ₹0.49 cr, so a selected partner clears the bar. The danger is carrying dormant partners, which is why the average across all 14 signed partners was only ₹0.19 cr. How likely: FY27 almost certainly loses a little. After that it depends on selection. If recruits behave like FY26 India partners, we lose money in FY28 and have a 44% chance in FY29. That is why the kill gate exists.');

// 14 Inject 3
s = base('Inject 3: P05 and P11 join Helix programmes; restrict them, require disclosure, and bring SEA recruits forward', 'Partner-conflict inject (week 7)');
stat(s, 0.5, 1.4, 2.9, '₹7.85 cr', 'of ₹14.83 cr open partner-sourced pipeline sits with P05 and P11 (53%)', ORANGE);
stat(s, 0.5, 2.55, 2.9, '₹0.30 cr', 'FY27 partner ARR shortfall against D2’s ₹4.0 cr, handed to D7 (direct headroom ₹2.9 cr covers it)');
stat(s, 0.5, 3.7, 2.9, '1.26 of 2.61', 'FY26 partner-sourced ARR (₹ cr) came from P05 and P11');
box(s, 3.7, 1.35, 5.8, 3.55, 'Response', '1. Restrict, do not exit: no deal registration for P05/P11 in Helix-incumbent accounts; keep them in non-Helix accounts and for services.\n2. Disclosure: every registration lists competing lines; conflict check within 48 hours.\n3. No exclusivity demand: we cannot enforce it and it would push both to Helix. Protection is earned by clean registrations.\n4. Accelerate PR01, PR02 and PR06 to Q1 onboarding; drop Helix-affiliated PR05, PR08, PR12.\n5. Review at end-Q2 FY27: exit if registered-deal conversion is under 15% or any registered deal switches to Helix.\n6. Move the top P05/P11 deals in Helix accounts to direct AEs with the D5 Helix battlecard.', ORANGE);
src(s, 'Source: DR1 open deals (partner-sourced, re-tagged); DR6; workbook sheet Inject3 (50% haircut on P05/P11 Helix-account pipeline is an assumption).');
note(s, 'This is the risk the brief flagged: partners tied to Helix will favour Helix. Exiting both would cost half our partner ARR overnight and hand their customers to Helix. Restriction limits the damage to the accounts where the conflict is real. The FY27 hit is small, ₹0.3 cr, because most FY27 partner ARR comes from new partners anyway. The lesson is structural: conflict risk is now 20% of the prospect score.');

// 15 Structure, scorecard, ask
s = base('Ask: a VP Channel and two SEA partner managers now, inside the Inject 1 envelope, with a scorecard that removes weak partners', 'Structure, scorecard and the ask');
tbl(s, [['Channel team', 'FY27', 'FY28', 'FY29'], ['VP Channel', '1', '1', '1'], ['Partner managers', '2 (SEA)', '4', '5'], ['Fixed cost excl. MDF (₹ cr)', '2.44', '3.46', '4.00']], 0.5, 1.4, 4.2, [2.1, 0.7, 0.7, 0.7], 10);
tbl(s, [['Scorecard (quarterly)', 'Promote', 'Coach', 'Remove'], ['Sourced ARR, trailing 12m', '≥ ₹1.0 cr', '₹0.3–1.0 cr', '< ₹0.3 cr after 4 qtrs'], ['Registered-deal win rate', '≥ 25%', '15–25%', '< 15%'],
  ['Certified engineers', '≥ 4', '2–3', '< 2 by month 6'], ['Customer satisfaction (1–10)', '≥ 8', '6–8', '< 6'], ['Conflict breach', 'none', '—', 'any']], 4.9, 1.4, 4.6, [1.7, 0.95, 0.95, 1.0], 9.5, [], 0.28);
s.addText([{ text: 'The ask. ', options: { bold: true, color: NAVY } }, { text: 'Approve 3 channel roles in FY27 (limit 6), ₹2.44 cr fixed cost within the Inject 1 allocation of ₹2.84 cr, ₹1.5 cr MDF from the ₹24 cr programme budget, the exits and restrictions above, and the kill gate at end-Q2 FY28.', options: { color: INK } }],
  { x: 0.5, y: 3.3, w: 4.2, h: 1.6, fontFace: BF, fontSize: 11, margin: 0, valign: 'top', isTextBox: true });
src(s, 'Source: workbook Inputs (costs), Checks (roles ≤ 6, GM ≥ 66%, envelope). 90-day launch plan attached.');
note(s, 'The team is small on purpose: two partner managers in SEA, where the evidence is strongest, and a VP who owns partner ARR in the forecast. It grows only if partners activate. The scorecard thresholds are the same numbers as the break-even and the Inject 3 rules, so promote, coach and remove decisions follow the economics.');

pres.writeFile({ fileName: 'out/D6_Channel_Strategy_Deck.pptx' }).then(() => console.log('ok'));
