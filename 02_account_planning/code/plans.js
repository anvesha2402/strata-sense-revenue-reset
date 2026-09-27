const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, LevelFormat, AlignmentType, BorderStyle, Footer, PageNumber, PageBreak } = require('docx');
const W = 10206;
const r = (t, o = {}) => new TextRun({ text: t, ...o });
const P = (runs, o = {}) => new Paragraph({ spacing: { after: 70, line: 252 }, ...o, children: (Array.isArray(runs) ? runs : [runs]).map(x => typeof x === 'string' ? r(x) : x) });
const H1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 0, after: 60 }, children: [r(t)] });
const H2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 110, after: 40 }, keepNext: true, children: [r(t)] });
const B = t => r(t, { bold: true });
const bd = { style: BorderStyle.SINGLE, size: 4, color: 'C9C8C2' };
const cell = (t, w, head, sz = 14, fill) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders: { top: bd, bottom: bd, left: bd, right: bd },
  shading: head ? { type: ShadingType.CLEAR, fill: '1F3A5F', color: 'auto' } : (fill ? { type: ShadingType.CLEAR, fill, color: 'auto' } : undefined),
  margins: { top: 30, bottom: 30, left: 60, right: 60 }, children: [new Paragraph({ children: [r(String(t), { bold: head, color: head ? 'FFFFFF' : undefined, size: sz })] })] });
const RAG = { G: 'D9F2E6', A: 'FFF1CC', R: 'FBDADA' };
const table = (rows, cols, ragCol = -1) => new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cols,
  rows: rows.map((rw, i) => new TableRow({ cantSplit: true, children: rw.map((t, j) => cell(t, cols[j], i === 0, 14, (j === ragCol && i > 0) ? RAG[String(t)[0]] : undefined)) })) });
const note = t => P([r(t, { size: 14, italics: true, color: '52514E' })], { spacing: { after: 60 } });

function plan(p) {
  return [
    H1(p.title),
    P([r(p.kind, { bold: true, color: '1F3A5F' }), r('   ·   ' + p.ids, { size: 16, color: '52514E' })]),
    table([['Fact (data room)', 'Value', 'Fact (data room)', 'Value']].concat(p.facts), [2600, 2503, 2600, 2503]),
    H2('Why this account, and the play'), P(p.why),
    H2('Buying committee map'),
    table([['Role', 'Name', 'What they care about', 'Stance today', 'Our next move']].concat(p.committee), [1650, 1050, 3000, 1400, 3106]),
    note('Names: the CRM holds ' + p.known + '. Every blank name is a discovery task, not an assumption.'),
    H2('Value hypothesis (₹, to be validated in discovery)'),
    table([['Driver', 'Hypothesis and arithmetic', '₹ cr / yr']].concat(p.value), [2200, 6606, 1400]),
    note(p.valueNote),
    H2('Qualification (MEDDPICC)'),
    table([['Element', 'What we know / need', 'Status']].concat(p.meddpicc), [1900, 7306, 1000], 2),
    H2('Mutual action plan (buyer and Strata)'),
    table([['By', 'Step', 'Owner']].concat(p.map), [1300, 6906, 2000]),
    H2('90-day plan'),
    table([['Window', 'Actions', 'Exit test']].concat(p.plan90), [1300, 6006, 2900]),
    P([B('Stop doing on this account: '), p.stop], { spacing: { before: 60 } }),
  ];
}
const A = {
  title: 'Account plan 1: Lotus Motors Ltd — expansion in a top-30 customer', kind: 'Expansion', ids: 'DR2 customer CU-1137 · top-30 by ARR (rank 4)',
  facts: [['ARR 31 Mar 2026', '₹7.48 cr (flat since Mar 2024)', 'Assets licensed / installed (est.)', '6,417 / 18,133 (35%)'],
          ['Usage (assets reporting, 90 days)', '97.5%: highest in the top 30', 'Implied price per asset', '₹11,657 / yr'],
          ['Plants', '2 (India)', 'Renewal date', '13 Aug 2026 (Q2 FY27)'],
          ['Automation incumbent', 'Vektor Systems (not Helix)', 'CSM assigned', 'Yes']],
  why: 'Lotus Motors uses almost every asset it pays for, yet its ARR has not moved in two years: nobody asked for the next plant area. It is the cleanest expansion case in the base: proven value, no Helix exposure, and a renewal in August that gives a natural decision date. Top-30 expansion fell from ₹21.3 cr in FY25 to ₹9.5 cr in FY26 (D1); this account alone could return a quarter of that gap. Play: co-term an expansion into the balance-of-plant assets (compressors, pumps, HVAC and utilities) with the August renewal, on a 2-year term.',
  known: 'no named contacts (DR2 has no contact table)',
  committee: [['Economic buyer: VP Manufacturing', 'TBC', 'Line uptime across both plants; capex vs opex', 'Unknown', 'CSM + AE request exec review in April'],
              ['Champion: Reliability / maintenance head', 'TBC', 'Fewer breakdowns; proof for his team', 'Likely positive (98% usage)', 'Co-build the value case with his failure log'],
              ['Plant heads (x2)', 'TBC', 'Output targets; overtime; spares', 'Unknown', 'Site walk to map uncovered assets'],
              ['CFO / finance controller', 'TBC', 'Payback; budget cycle; multi-year terms', 'Unknown', 'Share 2-year savings summary in June'],
              ['Procurement', 'TBC', 'Price per asset; renewal terms', 'Will push discount', 'Give-get: term length for price, not free discount'],
              ['IT / OT security', 'TBC', 'Data leaving the plant; access', 'Neutral (already approved)', 'Reconfirm security review covers new assets']],
  value: [['Avoided downtime', '3,000 more assets; 8% line-critical (240); 0.35 failures/asset/yr (84); 50% caught early (42); 6 hrs saved each at ₹4 lakh/hr', '10.1'],
          ['Maintenance cost', '3,000 assets × ₹12,000 maintenance/yr × 12% shift from reactive to planned', '0.4'],
          ['Spare-parts inventory', '5% lower safety stock on ₹6 cr of balance-of-plant spares', '0.3'],
          ['Total value vs price', 'Value ₹10.8 cr vs expansion price ~₹3.2 cr/yr (3,000 × ₹11,657 less 8% for 2-year term)', '3.4x']],
  valueNote: 'Every input is a hypothesis for the discovery conversation. The asset count and price come from DR2; downtime cost, failure rates and spares value must come from the customer’s own maintenance records (D3 builds the full model).',
  meddpicc: [['Metrics', 'Need their breakdown log for 2025 and cost per line-hour', 'A'], ['Economic buyer', 'VP Manufacturing not yet met', 'R'],
             ['Decision criteria', 'Likely payback and integration with Vektor systems', 'A'], ['Decision process', 'Renewal already runs through procurement; confirm who signs expansion', 'A'],
             ['Paper process', 'Co-term amendment to existing contract (low friction)', 'G'], ['Identify pain', 'Uncovered balance-of-plant failures: to quantify on site walk', 'A'],
             ['Champion', 'Reliability head: probable, not yet tested', 'A'], ['Competition', 'No rival in the account; risk is "do nothing" at renewal', 'G']],
  map: [['30 Apr', 'Exec review: usage results and uncovered asset map', 'Strata AE + CSM; VP Mfg'], ['20 May', 'Site walk at both plants; failure log shared', 'Plant heads; reliability head'],
        ['15 Jun', 'Joint value case agreed (their numbers)', 'Reliability head; Strata SE'], ['10 Jul', 'Proposal: renewal + expansion, 2-year term options', 'Strata AE'],
        ['31 Jul', 'Procurement and finance sign-off', 'CFO; procurement'], ['13 Aug', 'Co-termed renewal and expansion signed', 'VP Mfg']],
  plan90: [['Days 1–30', 'Exec review; name all six committee members; get failure log', '≥4 contacts named; EB meeting held'],
           ['Days 31–60', 'Site walks; joint value case; security reconfirmation', 'Value case signed off by champion'],
           ['Days 61–90', 'Proposal with give-get pricing; finance review', 'Verbal yes before 31 Jul']],
  stop: 'treating renewal as an admin event run by procurement alone; renewing flat without an expansion proposal.'
};
const Bp = {
  title: 'Account plan 2: Agni Renewables Industries Ltd — Helix displacement', kind: 'Competitive displacement (Helix incumbent)', ids: 'DR2 target T00084 · Strategic tier, EV rank 11 · named-40 Helix list',
  facts: [['Segment / sub-sector', 'Energy & utilities / thermal power', 'Revenue band', '> ₹20,000 cr'],
          ['Plants', '20', 'Installed rotating assets (est.)', '28,866'],
          ['Automation incumbent', 'Helix Automation', 'Existing condition monitoring', 'Portable / route-based'],
          ['P(win | qualified) / expected 1st-yr ARR', '0.42 / ₹1.28 cr', 'FY26 engagement', '1 touch, 1 contact; last activity 9 Apr 2025']],
  why: 'In FY26 Strata won only 7% of qualified deals in Helix-incumbent accounts, and none of 11 proposals where Helix was the named rival, even with a business case and several contacts (D1). A head-on replacement pitch will fail. Agni is on the named list because its size, route-based monitoring (a genuine gap Helix’s module does not close) and asset count make the upside worth one disciplined attempt. Play: do not attack Helix; land as the specialist layer on the assets where a forced outage is costliest (boiler feed pumps, ID/FD fans, coal mills) at one station, integrated with the Helix control system, through a paid pilot.',
  known: 'one contact, not named in the export, last touched in April 2025',
  committee: [['Economic buyer: Director, Generation', 'TBC', 'Plant load factor; forced-outage rate', 'Unknown', 'Exec briefing via ABM (outage-cost benchmark)'],
              ['Champion target: Station maintenance head', 'TBC', 'Route-based rounds miss failures between visits', 'Unknown', 'Offer failure-mode review on 3 critical systems'],
              ['Station head (pilot site)', 'TBC', 'Availability; safety', 'Unknown', 'Pilot site selection with maintenance head'],
              ['CFO', 'TBC', 'Regulated returns; penalty exposure', 'Unknown', 'Outage-cost case in ₹ per MWh lost'],
              ['Procurement', 'TBC', 'Rate contracts; Helix bundle price', 'Will cite free Helix module', 'Price the pilot, not the enterprise'],
              ['IT / OT security', 'TBC', 'Grid-critical OT; data residency', 'Likely sceptical', 'Early security pack; on-premise option question for CPO'],
              ['Helix account team (influencer)', '—', 'Protecting the bundle', 'Opposed', 'Position as integration partner, not replacement']],
  value: [['Avoided forced outage', 'Pilot station: 2 forced outages/yr on monitored systems avoided × 10 hrs × 500 MW × ₹4/kWh lost generation', '4.0'],
          ['Maintenance rounds', 'Replace part of route-based rounds on 600 assets: 2 technicians redeployed', '0.2'],
          ['Total value vs price', 'Value ₹4.2 cr at one station vs pilot ~₹0.7 cr/yr (600 assets) → scale path to ₹1.3 cr+ across stations', '6.0x']],
  valueNote: 'Unit size, tariff and outage frequency are illustrative placeholders to be replaced with Agni’s own data in discovery. If Helix makes its module free (a likely market move), the value case must stand on the uncovered critical assets, not on price.',
  meddpicc: [['Metrics', 'Forced-outage hours and cost per hour at the pilot station: unknown', 'R'], ['Economic buyer', 'Not identified', 'R'],
             ['Decision criteria', 'Likely integration with Helix DCS, OT security, price vs bundle', 'A'], ['Decision process', 'Unknown; utilities often need a technical committee', 'R'],
             ['Paper process', 'Rate contract vs one-off pilot PO: to confirm', 'A'], ['Identify pain', 'Route-based monitoring gap: strong hypothesis, not confirmed', 'A'],
             ['Champion', 'None yet', 'R'], ['Competition', 'Helix incumbent with bundle; TrueSense possible (existing sensors: none online)', 'R']],
  map: [['15 May', 'Exec briefing: outage-cost benchmark for thermal fleets', 'Strata RVP; Director Generation'], ['15 Jun', 'Failure-mode review on 3 critical systems at one station', 'Maintenance head; Strata SE'],
        ['15 Jul', 'Security pack reviewed by IT/OT', 'IT/OT security'], ['31 Aug', 'Paid pilot scope and success criteria agreed', 'Station head; procurement'],
        ['30 Sep', 'Pilot PO', 'CFO / procurement'], ['Q3 FY27', 'Pilot live; results review at 90 days', 'Joint']],
  plan90: [['Days 1–30', 'Account research; find champion via ABM and SI partner; re-open the dormant contact', 'Champion candidate identified'],
           ['Days 31–60', 'Exec briefing; failure-mode review', 'EB met; pain confirmed in ₹'],
           ['Days 61–90', 'Security pack; pilot scope with success criteria', 'Go / no-go: stop if no EB or champion by day 90']],
  stop: 'pitching a full replacement of Helix; discounting against a free bundle; spending AE time past day 90 without an economic buyer.'
};
const Cp = {
  title: 'Account plan 3: Keystone Forgings Pvt Ltd — new-logo whitespace', kind: 'New logo (never engaged)', ids: 'DR2 target T02772 · Strategic tier, EV rank 9 · highest P(win) in the tier',
  facts: [['Segment / sub-sector', 'Discrete manufacturing / forgings & castings', 'Revenue band', '> ₹20,000 cr'],
          ['Plants', '18', 'Installed rotating assets (est.)', '16,995'],
          ['Automation incumbent', 'Vektor Systems (not Helix)', 'Existing condition monitoring', 'None'],
          ['P(win | qualified) / expected 1st-yr ARR', '0.55 / ₹1.00 cr', 'FY26 engagement', '0 touches, 0 contacts; assigned to AE032']],
  why: 'Keystone scores highest on fit in the strategic tier, has no condition monitoring at all (so no TrueSense sensor-reuse angle), and no Helix exposure, yet nobody at Strata has spoken to it. Meanwhile AE time went to low-fit accounts, which took 61% of FY26 touches (D1). Play: executive-sponsored entry with a reference from a similar customer that is expanding (Trident Auto Components, CU-1150, ARR up 37% in FY26), then a paid pilot on forging presses and hydraulic systems at one plant.',
  known: 'no contacts at all',
  committee: [['Economic buyer: COO / Head of Operations', 'TBC', 'Press uptime; delivery to OEM customers', 'Unknown', 'Reference-led exec intro (ABM)'],
              ['Champion target: Corporate maintenance head', 'TBC', 'Unplanned press and hydraulic failures', 'Unknown', 'Discovery call with failure-cost questions'],
              ['Plant head (pilot plant)', 'TBC', 'OEM delivery penalties; overtime', 'Unknown', 'Site visit with SE'],
              ['CFO', 'TBC', 'Payback within the year', 'Unknown', 'Business case built on their numbers'],
              ['Procurement', 'TBC', 'Price per asset; pilot terms', 'Unknown', 'Pilot-to-scale structure'],
              ['IT / OT security', 'TBC', 'Cloud and plant network access', 'Unknown', 'Security pack in first month']],
  value: [['Avoided downtime', 'Pilot plant: 700 assets; 10% critical (70); 0.4 failures/yr (28); 50% caught early (14); 8 hrs saved each at ₹2 lakh/hr', '2.2'],
          ['OEM delivery penalties', 'Avoid 2 late-delivery penalties a year at ₹15 lakh each', '0.3'],
          ['Maintenance cost', '700 assets × ₹12,000/yr × 12% shift to planned', '0.1'],
          ['Total value vs price', 'Value ₹2.6 cr at one plant vs pilot ~₹0.8 cr/yr (700 assets) → 18-plant path ≈ ₹1.0 cr first-year, more at scale', '3.2x']],
  valueNote: 'Asset counts come from DR2; downtime cost, failure rates and penalties are hypotheses for the first discovery call.',
  meddpicc: [['Metrics', 'Unknown: first discovery objective', 'R'], ['Economic buyer', 'Not identified', 'R'], ['Decision criteria', 'Unknown', 'R'],
             ['Decision process', 'Unknown', 'R'], ['Paper process', 'Unknown', 'R'], ['Identify pain', 'Hypothesis: no monitoring on presses and hydraulics', 'A'],
             ['Champion', 'None', 'R'], ['Competition', 'None visible; TrueSense less likely (no existing sensors)', 'G']],
  map: [['30 Apr', 'Reference call arranged with Trident Auto Components', 'Strata AE + customer marketing'], ['31 May', 'Exec intro meeting; discovery with maintenance head', 'COO; maintenance head'],
        ['30 Jun', 'Site visit at pilot plant; failure-cost data', 'Plant head; Strata SE'], ['31 Jul', 'Business case on their numbers', 'Champion; CFO'],
        ['31 Aug', 'Paid pilot agreed', 'Procurement'], ['Q4 FY27', 'Pilot results; scale decision', 'COO']],
  plan90: [['Days 1–30', 'ABM research; reference secured; 3 contacts identified', 'First meeting booked'],
           ['Days 31–60', 'Exec intro and discovery; site visit', 'EB and champion named; pain in ₹'],
           ['Days 61–90', 'Business case; security pack; pilot proposal', 'Pilot proposal accepted in principle']],
  stop: 'leaving the highest-fit accounts untouched while the AE works low-fit inbound.'
};
const kids = [
  new Paragraph({ spacing: { after: 30 }, children: [r('D2 · Three strategic account plans', { bold: true, size: 28, color: '1F3A5F' })] }),
  P([r('Strata Sense Technologies is fictional; all data synthetic (MBA capstone). Facts from DR1–DR3; ₹ value figures are hypotheses to validate in discovery.', { italics: true, size: 15, color: '52514E' })]),
  ...plan(A), new Paragraph({ children: [new PageBreak()] }), ...plan(Bp), new Paragraph({ children: [new PageBreak()] }), ...plan(Cp)
];
const doc = new Document({
  styles: { default: { document: { run: { font: 'Arial', size: 16 } } },
    paragraphStyles: [{ id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 24, bold: true, color: '1F3A5F' }, paragraph: { outlineLevel: 0 } },
                      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 18, bold: true, color: '333333' }, paragraph: { outlineLevel: 1 } }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 800, bottom: 800, left: 850, right: 850 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [r('Strata Sense · D2 account plans · page ', { size: 14, color: '52514E' }), new TextRun({ children: [PageNumber.CURRENT], size: 14, color: '52514E' })] })] }) },
    children: kids }] });
Packer.toBuffer(doc).then(b => fs.writeFileSync('out/D2_Account_Plans.docx', b));
