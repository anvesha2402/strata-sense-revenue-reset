const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, LevelFormat, AlignmentType, BorderStyle, Footer, PageNumber, PageBreak } = require('docx');
const W = 10206, r = (t, o = {}) => new TextRun({ text: t, ...o });
const P = (x, o = {}) => new Paragraph({ spacing: { after: 70, line: 252 }, ...o, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const H1 = (t, col = '1F3A5F') => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 0, after: 60 }, children: [r(t, { color: col })] });
const H2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 100, after: 40 }, keepNext: true, children: [r(t)] });
const B = t => r(t, { bold: true });
const bul = x => new Paragraph({ numbering: { reference: 'b', level: 0 }, spacing: { after: 30, line: 245 }, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const bd = { style: BorderStyle.SINGLE, size: 4, color: 'C9C8C2' };
const cell = (t, w, h, fill, sz = 15) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders: { top: bd, bottom: bd, left: bd, right: bd }, shading: h ? { type: ShadingType.CLEAR, fill: '1F3A5F', color: 'auto' } : (fill ? { type: ShadingType.CLEAR, fill, color: 'auto' } : undefined), margins: { top: 30, bottom: 30, left: 60, right: 60 }, children: String(t).split('\n').map(line => new Paragraph({ children: [r(line, { bold: h, color: h ? 'FFFFFF' : undefined, size: sz })] })) });
const table = (rows, cols, sz = 15) => new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cols, rows: rows.map((rw, i) => new TableRow({ cantSplit: true, children: rw.map((t, j) => cell(t, cols[j], i === 0, undefined, sz)) })) });
const box = (title, lines, fill = 'FFF1E8') => new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [W], rows: [new TableRow({ children: [new TableCell({ width: { size: W, type: WidthType.DXA }, borders: { top: bd, bottom: bd, left: { style: BorderStyle.SINGLE, size: 18, color: 'EB6834' }, right: bd }, shading: { type: ShadingType.CLEAR, fill, color: 'auto' }, margins: { top: 60, bottom: 60, left: 120, right: 120 }, children: [new Paragraph({ children: [r(title, { bold: true, size: 17 })] }), ...lines.map(l => new Paragraph({ spacing: { before: 30 }, children: [r(l, { size: 16 })] }))] })] })] });
const PB = () => new Paragraph({ children: [new PageBreak()] });
const small = t => P([r(t, { size: 14, italics: true, color: '52514E' })], { spacing: { after: 60 } });
function card(c) {
  return [H1(c.title, c.col), P([r(c.sub, { size: 15, color: '52514E' })]),
    table([['When we WIN', 'When we LOSE']].concat([[c.win, c.lose]]), [5103, 5103]),
    H2('Their real strengths (say them before the buyer does)'), ...c.strengths.map(s => bul(s)),
    H2('Their weaknesses, with evidence'), table([['Weakness', 'Evidence']].concat(c.weak), [4200, 6006]),
    H2('Five objections and what to say'), table([['Buyer says', 'We say']].concat(c.obj), [3400, 6806]),
    H2('Questions that expose the gap'), ...c.qs.map(s => bul(s)),
    H2('Three-year total cost (500-asset plant, list prices, DR5)'), table([['', 'Strata', c.rname]].concat(c.tco), [4400, 2903, 2903]),
    H2('Talk tracks by persona'), table([['Plant head', 'CFO', 'IT security']].concat([c.persona]), [3402, 3402, 3402]),
    H2('Proof points'), ...c.proof.map(s => bul(s)),
    H2('Pricing limits'), table([['Rep may trade', 'Manager may approve', 'Never']].concat([c.price]), [3402, 3402, 3402]), PB()];
}
const helix = { title: 'Battlecard 1 · Helix Automation (HelixAsset)', col: 'EB6834', rname: 'HelixAsset', sub: 'Bundled incumbent. On 24% of FY26 qualified deals. Version 1.1: updated for the Week 5 announcement (HelixAsset free to existing plant customers until 31 Mar 2027).',
  win: 'Plant runs mixed automation (Orion, Vektor, Kaizen), so HelixAsset only sees part of the fleet.\nWe scope only the assets Helix cannot see (hydraulics, compressors, chillers) and integrate with Helix, not replace it.\nThe plant head sponsors us because failures happen on uncovered assets. (DR4: 2 of 2 wins)',
  lose: 'Helix is the plant’s automation vendor and IT wants one vendor on the OT network. (DR4: 5 of 6 losses)\nWe pitch a head-on replacement, or discount to match "free". Strong selling won 0 of 9 proposals against Helix.\nWe are single-threaded below the economic buyer, or not in the integrator’s design.',
  strengths: ['Already inside the control system; one vendor for IT and procurement.', 'Near-zero price: now free to existing customers until 31 March 2027.', 'Strong integrator ecosystem that designs new lines.'],
  weak: [['Sees only what Helix PLCs see: no coverage of hydraulic packs, most compressors, chillers or non-Helix machines', 'DR5 capability notes; DR4 VOB-03, VOB-19, VOB-20; D3 discovery (RPC pilot on spindles only)'],
    ['Threshold rules and generic models on PLC tags; no acoustic or low-speed diagnostics', 'DR5; DR4 VOB-01 ("your analytics were better")'],
    ['Free is temporary; list price ₹9,500/asset/yr afterwards; earlier offer tied to a 3-year MES lock-in', 'DR5; D3 discovery (CFO)'],
    ['Non-Helix assets need Helix sensors at ~₹13,000 each', 'DR5']],
  obj: [['"HelixAsset is free now. Why pay you?"', '"Free until March, on machines wired to Helix PLCs. Which of your last three breakdowns were on those machines?" Then show the uncovered-asset list.'],
    ['"IT wants one vendor on the OT network."', '"Understood. We don’t connect to your PLCs at all. Our sensors report to an edge server inside your plant; IT gets a security pack on day one."'],
    ['"We’ll try Helix first and see."', '"Fine for the spindles. Run us on the presses and compressors at the same time; compare what each finds in 90 days."'],
    ['"Helix will add those assets later."', '"With their sensors at ~₹13,000 each, after the free period. Let’s price both on the same asset list for three years."'],
    ['"Can you match free?"', '"No. We’ll price only the assets Helix doesn’t cover, and we can defer the start by three months on a three-year term."']],
  qs: ['"Which assets does the HelixAsset pilot cover, and which does it not?"', '"What were your last three unplanned stoppages, and would a PLC tag have seen them coming?"', '"What happens to the price on 1 April 2027? Is that in writing?"', '"How many of your machines are wired to Helix controls today?"'],
  tco: [['Subscription (3 years)', '₹1.88 cr', '₹0.95 cr (2 paid years after free period)'], ['Sensors / hardware', '₹0.55 cr', '₹0.33 cr (Helix sensors on ~250 non-Helix assets)'], ['Set-up, gateways, edge', '₹0.19 cr', 'Included'], ['Three-year total', '₹2.61 cr', '₹1.28 cr'], ['Coverage', 'All 500 assets', 'Helix-wired assets + those given Helix sensors; no acoustic']],
  persona: ['"Keep Helix on the spindles. We watch the presses and compressors it can’t see: the assets behind your worst stoppages."', '"Free for 12 months, then list price. Compare three-year cost per failure prevented, not year-one price."', '"No PLC connection, edge buffering, data in India, ISO 27001 and SOC 2 Type II. Security pack before the first meeting."'],
  proof: ['Mixed-automation plant chose Strata because "Helix was only free on Helix machines" (DR4 VOB-20).', 'Press-line plant with Helix incumbent bought Strata for hydraulic systems only (DR4 VOB-19).'],
  price: ['Scope limited to non-PLC assets; 3-month deferred start on a 3-year term', 'Up to 10% for a 3-year complement term', 'Match "free"; bid for PLC-connected assets; discount to "win back" Helix']
};
const ts = { title: 'Battlecard 2 · TrueSense AI', col: '2A78D6', rname: 'TrueSense AI', sub: 'Sensor-agnostic, venture-backed. On 22% of FY26 qualified deals. Prices 35–40% below Strata.',
  win: 'Plant has no online sensors, or poor data on the assets that fail (slow drives, hydraulics). (DR4 VOB-17, VOB-18)\nWe run a paid pilot with written success criteria and a business case on the buyer’s numbers.\n3+ contacts incl. finance and IT; we answer security first. Strong selling won 36% vs 12% otherwise.',
  lose: 'Plant already has good online sensors on simple assets; TrueSense connects to the historian with no hardware. (DR4: 3 of 4 losses)\nOur offer starts with hardware and a paid pilot, against their free 60-day proof of concept.\nWe meet only procurement at the end; price is the only comparison.',
  strengths: ['No new hardware where sensors exist; fast start (weeks).', 'Free 60-day proof of concept; lower per-asset price (₹7,800).', 'Well funded; expanding to South-East Asia.'],
  weak: [['Weaker on low-speed and hydraulic assets and where existing sensor data is poor', 'DR5; DR4 VOB-17 ("where our sensors weren’t good, you found the fault"); RN-04'],
    ['Needs sensors the plant may not have; third-party sensors ~₹8,000 each at the customer’s cost', 'DR5; DR4 VOB-18'],
    ['Cloud-only design raises OT-security concerns', 'DR4 VOB-24'],
    ['Free POC has no pass/fail criteria tied to money', 'DR4 VOB-07, VOB-23']],
  obj: [['"TrueSense uses our existing sensors. You want to replace them."', '"Only where the data can’t see the failure. Let’s audit your sensor coverage on the assets that failed last year, together."'],
    ['"They’re 35% cheaper."', '"Per asset, yes. Per failure caught, compare the pilot results. We’ll put that in writing as success criteria."'],
    ['"Their proof of concept is free."', '"Ours is credited in full if it works, and it has pass/fail criteria your finance team writes."'],
    ['"They connected in two weeks."', '"On assets with good historian data. Which of your critical assets have none?"'],
    ['"We’ll decide on price."', '"Then let’s price the same assets, including sensors you’d need to buy for TrueSense, over three years."']],
  qs: ['"Which of your critical assets have online sensors today, and how good is that data?"', '"How does their model handle slow-speed drives and hydraulic presses?"', '"What are the pass/fail criteria of the free proof of concept?"', '"Does their design send OT data straight to the cloud?"'],
  tco: [['Subscription (3 years)', '₹1.88 cr', '₹1.17 cr'], ['Sensors / hardware', '₹0.55 cr', '₹0.20 cr (customer buys ~250 third-party sensors)'], ['Set-up, gateways, edge', '₹0.19 cr', '~₹0.10 cr'], ['Three-year total', '₹2.61 cr', '₹1.47 cr'], ['Where it matters', 'Hydraulics, slow drives, no-sensor assets', 'Assets with good existing data']],
  persona: ['"Where your sensors are good, anyone can read them. Where they aren’t, is where your breakdowns are."', '"Pay for failures caught, not for a demo. Our pilot has pass/fail criteria; theirs doesn’t."', '"Edge buffering inside your plant; nothing from OT goes straight to the cloud."'],
  proof: ['Cement plant: TrueSense POC struggled on kiln drives; Strata pilot caught a gearbox fault three weeks early (DR4 VOB-17).', 'Plant with portable monitoring only: Strata won with a business case on the plant’s own breakdown log (DR4 VOB-18).'],
  price: ['Up to 5%, only against a give (term, prepay, reference)', 'Up to 12% with a 3-year term and a paid pilot', 'Price-match their per-asset rate; free pilot without conversion terms']
};
const bmi = { title: 'Battlecard 3 · Bharat Machine Intelligence', col: '1BAF7A', rname: 'BMI', sub: 'Regional low-cost. On 9% of FY26 qualified deals, mostly small or low-fit sites (D2 stop-list).',
  win: 'Critical assets where a missed failure is expensive; the CFO is in the room. (DR4 VOB-21)\nPlant needs diagnosis, not just trend lines.',
  lose: 'Small sites with simple fans and pumps where trends are "good enough". (DR4 VOB-11)\nPrice-only comparison with procurement; local partner support. (DR4 VOB-12)',
  strengths: ['Lowest price (₹6,500/asset/yr, sensors ~₹6,000).', 'Local support through a regional integrator.', 'Simple dashboards that maintenance teams like.'],
  weak: [['Trend alerts only; limited diagnosis', 'DR5; DR4 VOB-21 ("cheap monitoring that misses the big failure is expensive")'], ['Regional support only; no SEA or Gulf coverage', 'DR5'], ['Phase-one wins often leave critical assets uncovered', 'DR4 VOB-12']],
  obj: [['"BMI is half your price."', '"For fans and pumps, they may be right. For your kiln drives, what does one missed failure cost?"'], ['"Their team is local."', '"So is our partner network; and our analysts review every alert with your team for 90 days."'],
    ['"We only need trends."', '"Then we may not be the right fit for those assets. Let’s focus on the ones where you need a diagnosis."'], ['"Can you come closer on price?"', '"Only with a longer term or a second site. We don’t discount to compete on basic monitoring."'],
    ['"We’ll start cheap and upgrade later."', '"Sensible for non-critical assets. Start us on the critical ones and compare."']],
  qs: ['"What did your last missed failure cost, and would a trend line have caught it?"', '"Who diagnoses the alert once it fires?"', '"What coverage do they offer outside your region?"'],
  tco: [['Subscription (3 years)', '₹1.88 cr', '₹0.98 cr'], ['Sensors / hardware', '₹0.55 cr', '₹0.30 cr'], ['Set-up, gateways, edge', '₹0.19 cr', '~₹0.05 cr'], ['Three-year total', '₹2.61 cr', '₹1.33 cr'], ['Fit', 'Critical, complex assets', 'Simple assets, trends only']],
  persona: ['"Use trends where trends are enough. Use us where a failure stops the line."', '"Cheap monitoring that misses the big failure is expensive (a CFO’s words, not ours)."', '"Same security standards on every asset; regional tools often skip them."'],
  proof: ['Cement group CFO chose Strata over a cheaper BMI offer after seeing kiln-drive failures BMI could not diagnose (DR4 VOB-21).'],
  price: ['0%; qualify out price-only small sites', 'Up to 5% with a CFO risk case on critical assets', 'Discount to compete on basic monitoring']
};
const nd = { title: 'Battlecard 4 · "No decision" (status quo)', col: '52514E', rname: 'Status quo', sub: 'Buyer does nothing. 52 of 359 FY26 qualified losses (14%); more hide in blank loss reasons.',
  win: 'A compelling event with a date (renewal, OEM audit, budget cycle); the economic buyer engaged by stage 2.\nBusiness case built on the buyer’s numbers; paid pilot with written criteria. (DR4 VOB-23)',
  lose: 'One contact who moves or loses budget. (DR4: 2 of 4 no-decision losses)\nBusiness case built on vendor averages that finance ignores. (DR4 VOB-16)\nDecision rights move (group IT, MES renewal) and we don’t notice. (DR4 VOB-13, VOB-15)',
  strengths: ['Costs nothing today; no project risk.', 'Existing handheld rounds "work well enough".', 'Other priorities compete for the same budget.'],
  weak: [['Status quo has a cost the buyer rarely measures (e.g. press failures, OEM penalties)', 'D3 discovery: ₹1.2 cr OEM penalty; 3 major press failures'], ['Delay pushes the decision past budget windows', 'D3: committee dates 15 Jul / 15 Oct']],
  obj: [['"Let’s revisit next year."', '"Happy to. What will the next press failure cost between now and then? Let’s put a number on waiting."'], ['"Budget is frozen."', '"Is opex under your CFO’s own limit also frozen? Our pilot sits inside it."'],
    ['"Our current rounds work."', '"Monthly rounds on a press that runs three shifts: how many failures did they catch last year?"'], ['"We need to see results first."', '"Agreed: a paid pilot with pass/fail criteria you write, credited if it works."'],
    ['"Head office is reviewing digital."', '"Who at head office should see this, and when do they decide?"']],
  qs: ['"What happens if you do nothing for 12 months?"', '"Who else must say yes, and when does money get released?"', '"Which number in our business case do you disagree with?"'],
  tco: [['Cost of doing nothing (example: Chakan P2, conservative)', '—', '≈ ₹1.3 cr a year of avoidable downtime and maintenance (D3 value model)'], ['Pilot cost', '₹0.25 cr, credited on conversion', '₹0'], ['Payback (conservative)', '3–7 months', 'n/a']],
  persona: ['"What does the next breakdown cost you personally: OEE, overtime, the OEM call?"', '"Waiting has a price: here it is in your own numbers."', '"Starting the security review now costs nothing and keeps the option open."'],
  proof: ['Plant finance approved quickly because pilot pass/fail criteria were written with finance (DR4 VOB-23).'],
  price: ['Pilot credit only', 'Pilot credit only', 'End-of-quarter discount to force a decision']
};
const kids = [
  new Paragraph({ spacing: { after: 40 }, children: [r('D5 · Competitive battlecards', { bold: true, size: 32, color: '1F3A5F' })] }),
  P([r('Version 1.1 · Week 5 · Strata Sense and all competitors are fictional; synthetic data (MBA capstone).', { size: 16, italics: true, color: '52514E' })]),
  box('URGENT UPDATE v1.1 (Inject 2): Helix makes HelixAsset free to all existing plant customers until 31 March 2027', [
    '1. Talk track changes from "free with a 3-year lock-in" to "free until March, then what, and on which machines?"',
    '2. No matching "free". New allowed trade: 3-month deferred start on complement scope, only with a 3-year term.',
    '3. FY27 win-rate assumption for Helix-incumbent accounts held at 7% (the complement uplift is cancelled until April 2027).',
    '4. Every Helix-incumbent customer renewing before March 2027 gets an executive sponsor and usage review 90 days ahead (₹108.6 cr of ARR).',
    '5. Tag deals "HELIX-FREE" in the CRM for 90 days so the effect can be measured. Published within 48 hours; 30-minute rep briefing.']),
  H2('Is the Helix bundle a positioning, pricing or product problem?'),
  P([B('Answer: in Helix-incumbent accounts it is a packaging and pricing problem, not a positioning problem, and our product is the way out. '), 'Positioning does not move it: strong selling (business case plus several contacts) won 0 of 9 proposals against Helix, and the win rate in Helix-incumbent accounts fell from 20% to 7% whatever reps did. Discounting does not move it either: won and lost deals carried the same discount (20% vs 19%). What does win is scope. In both DR4 wins against Helix, Strata priced only the assets Helix cannot see and integrated with it. So the response is a complement package priced on uncovered assets, a retention offer for Helix-incumbent customers, and a CPO decision on a sensor-agnostic tier. It is not better scripts and not bigger discounts.']),
  H2('How to use these cards'),
  bul('Two pages per rival: win/lose patterns first, then objections, trap questions, three-year cost, persona tracks, proof and pricing limits.'),
  bul('Evidence tags: DR1 = CRM (cleaned in D1); DR4 = voice of buyer (VOB-xx interviews, RN-xx rep notes); DR5 = competitor dossier; D1–D4 = earlier deliverables.'),
  bul('Caution: the CRM competitor field is mostly filled after a loss, so win rates "against" a rival are biased low. Cards compare strong vs weak selling within each rival.'),
  PB(),
  ...card(helix), ...card(ts), ...card(bmi), ...card(nd),
  H1('Rep quick reference (one page)'),
  table([['', 'Helix', 'TrueSense', 'BMI', 'No decision'],
    ['Engage when', 'Mixed automation; failures on non-PLC assets', 'Poor or no sensor data on failing assets', 'Critical assets; CFO in the room', 'Compelling event with a date'],
    ['Qualify out when', 'IT mandates one vendor and all critical assets are Helix-wired', 'Good online sensors on simple assets', 'Small site, simple assets, price only', 'No economic buyer by stage 2'],
    ['One-line counter', '"Free until March, on Helix machines. Which breakdowns were on those?"', '"Anyone reads good sensors. Your failures are where the data is poor."', '"Trends where trends are enough; us where failure stops the line."', '"Here is the cost of waiting, in your numbers."'],
    ['Killer question', 'Which assets does the pilot not cover?', 'How good is the data on the assets that failed?', 'Who diagnoses the alert?', 'What happens if you do nothing for a year?'],
    ['Max discount (rep / manager)', '0% to match free / 10% for 3-yr complement', '5% / 12%', '0% / 5%', 'Pilot credit only'],
    ['Proof point', 'VOB-20: "Helix was only free on Helix machines"', 'VOB-17: gearbox fault caught 3 weeks early', 'VOB-21: CFO chose lower risk', 'VOB-23: pilot criteria written with finance']], [1500, 2176, 2176, 2176, 2178], 14),
  H2('Always'), bul('Business case on the buyer’s numbers. ≥3 contacts incl. finance and IT by stage 3. Security pack before IT asks. Every discount point traded for a commitment.'),
  PB(),
  H1('Win/loss analysis and expected uplift'),
  P('Coding: DR1 loss reasons for FY25–26 qualified losses, plus the 24 DR4 interviews coded into 15 themes (D5_WinLoss_Analysis.xlsx, VOB_coding). Loss themes: single-threaded or no economic buyer (7 of 16 losses), Helix bundle lock-in (5), vendor numbers instead of the buyer’s (4), sensor reuse (3), price only (3), budget or deferral (3). Win themes: multi-threading (4 of 8 wins), buyer numbers (3), pilot criteria (2), complementing Helix (2), diagnostic depth (2).'),
  table([['Rival', 'Lever', 'FY27 uplift in those deals', 'Effect on overall win rate', 'New beyond D2', 'Assumption'],
    ['Helix (named 40)', 'Complement uncovered assets; no matching', '+3 pts, cancelled by Inject 2 → 0', '0.0', '0.0', 'Recover in FY28 when "free" ends'],
    ['TrueSense', 'Business case + ≥3 contacts; sensor-data audit; qualify out', '+5 pts', '+1.1', '+0.4', 'Strong selling 12% → 36% (14 strong proposals)'],
    ['BMI', 'Stop-list; CFO risk case', '+2 pts', '+0.2', '+0.1', 'Lower BMI volume after D2 stop-list'],
    ['No decision', 'Compelling event; EB by stage 2; paid pilot criteria', '+1.5 pts', '+0.2', '+0.1', 'Converts a few no-decisions to wins'],
    ['Total', '', '', '+1.5 pts', '+0.6 pts', 'Most overlaps with the D2 multi-threading lift; D7 counts it once']], [1400, 2600, 1700, 1400, 1100, 2006], 14),
  P([B('Contradiction to explain: '), 'reps say "we always lose to TrueSense on price" (RN-01). The data disagrees: won and lost TrueSense proposals carried the same discount (19% vs 21%), and interviews name sensor reuse and missing business cases more often than price. Price is the reason given at the end of a deal that was lost earlier.'], { spacing: { before: 80 } }),
  H1('Enablement and maintenance'),
  table([['Item', 'Plan'], ['Owner', 'Competitive-intelligence lead in product marketing (interim: Revenue Strategy Lead). Each card has an SE co-owner for technical claims.'],
    ['Cadence', 'Monthly refresh from win/loss tags and new DR4 interviews; quarterly deep review with sales leaders.'],
    ['Urgent-update rule', 'Any rival pricing or packaging announcement: updated card within 48 hours, 30-minute briefing within one week, CRM tag for 90 days. Tested live by Inject 2 (v1.1).'],
    ['Training', 'Week 1: 60-minute briefing per card. Week 2: role-play certification on the five objections (manager scores). Ongoing: one call review per AE per month using the card.'],
    ['Measures', 'Adoption: share of competitive deals with the card’s trap questions logged in discovery notes (target 70%). Outcome: win rate on strong-selling proposals by rival; average discount by rival (target ≤ 14%); loss-reason and competitor fields complete on ≥ 90% of closed deals.']], [2000, 8206]),
  H1('Field validation (to be completed with real practitioners)'),
  P('The brief requires testing at least two cards with three or more practitioners (sales leaders or buyers of industrial software) and documenting what changed. Plan: test the Helix and TrueSense cards with three people from your interview list (Strata_Interview_Log.xlsx, "OK to test battlecard = Y"). Ask each: (1) Which objection is missing or wrongly worded? (2) Which response would not work with your buyers, and why? (3) Which trap question would you actually ask? (4) Is the pricing limit realistic? Record answers in D5_Field_Validation_Log.xlsx and publish version 1.2 with a change log.'),
  table([['Practitioner (role)', 'Card tested', 'Main feedback', 'Change made in v1.2'], ['[to fill]', 'Helix', '', ''], ['[to fill]', 'TrueSense', '', ''], ['[to fill]', 'Helix + TrueSense', '', '']], [2600, 1800, 3000, 2806]),
  small('No practitioner feedback is included above: it must come from real conversations.'),
];
const doc = new Document({ styles: { default: { document: { run: { font: 'Arial', size: 17 } } }, paragraphStyles: [
  { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 25, bold: true }, paragraph: { outlineLevel: 0 } },
  { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 18, bold: true, color: '1F3A5F' }, paragraph: { outlineLevel: 1 } }] },
  numbering: { config: [{ reference: 'b', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 200 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 750, bottom: 750, left: 850, right: 850 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [r('Strata Sense · D5 battlecards v1.1 · page ', { size: 14, color: '52514E' }), new TextRun({ children: [PageNumber.CURRENT], size: 14, color: '52514E' })] })] }) }, children: kids }] });
Packer.toBuffer(doc).then(b => fs.writeFileSync('out/D5_Battlecards_v1.1.docx', b));
