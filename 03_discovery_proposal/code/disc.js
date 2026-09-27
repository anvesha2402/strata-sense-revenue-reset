const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, LevelFormat, AlignmentType, BorderStyle, Footer, PageNumber } = require('docx');
const W = 10206, r = (t, o = {}) => new TextRun({ text: t, ...o });
const P = (x, o = {}) => new Paragraph({ spacing: { after: 80, line: 259 }, ...o, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const H1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 160, after: 70 }, keepNext: true, children: [r(t)] });
const H2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 110, after: 40 }, keepNext: true, children: [r(t)] });
const B = t => r(t, { bold: true });
const bul = x => new Paragraph({ numbering: { reference: 'b', level: 0 }, spacing: { after: 40, line: 252 }, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const bd = { style: BorderStyle.SINGLE, size: 4, color: 'C9C8C2' };
const cell = (t, w, h) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders: { top: bd, bottom: bd, left: bd, right: bd }, shading: h ? { type: ShadingType.CLEAR, fill: '1F3A5F', color: 'auto' } : undefined, margins: { top: 35, bottom: 35, left: 70, right: 70 }, children: [new Paragraph({ children: [r(t, { bold: h, color: h ? 'FFFFFF' : undefined, size: 15 })] })] });
const table = (rows, cols) => new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cols, rows: rows.map((rw, i) => new TableRow({ cantSplit: true, tableHeader: i === 0, children: rw.map((t, j) => cell(t, cols[j], i === 0)) })) });
const tree = [['Branch', 'Question (open first, then specific)', 'Why it matters / what I do with the answer'],
 ['Situation', 'Walk me through how maintenance works at Chakan P2 today: what is monitored, how often, by whom?', 'Baseline: route-based vs online; team size; which assets are uncovered'],
 ['Situation', 'Which assets are in the HelixAsset pilot, and which are not? What were the success criteria?', 'Pilot scope and terms; gap = Strata’s landing zone'],
 ['Situation', 'How many rotating assets does the plant have, by type (spindles, presses, compressors, pumps)?', 'Scope and price the pilot (value-model inputs)'],
 ['Pain', 'What were the three worst unplanned stoppages in the last 12 months? What failed, and for how long?', 'Specific events beat averages; points to asset class'],
 ['Pain', 'How confident are you in the downtime numbers in the MES? How are stoppages coded?', 'Tests data reliability; true downtime may be higher than reported'],
 ['Pain', 'What share of maintenance work is planned vs reactive?', 'Maintenance-savings driver'],
 ['Impact', 'What does an hour of downtime cost on a machining line? On a forging press line? Who owns that number?', 'Buyer-supplied ₹ per hour (from finance)'],
 ['Impact', 'Have any stoppages affected an OEM customer? What did that cost, in penalties or relationship?', 'Penalty exposure; board-level visibility'],
 ['Impact', 'How do these issues show up in OEE and in your own targets?', 'Personal win for the plant head'],
 ['Impact', 'What do spares inventory and compressor energy cost the plant each year?', 'Secondary value drivers'],
 ['Decision', 'Who else is involved in deciding a tool like this: operations, finance, IT, procurement, MD?', 'Committee map; find the economic buyer'],
 ['Decision', 'How is software like this budgeted: capex or opex? What can the CFO approve alone? When does the committee meet?', 'Budget cycle and paper process; sets the close date'],
 ['Decision', 'What does IT and OT security need before anything connects to plant machines? Has anything happened that shaped those rules?', 'Security gate; timeline risk'],
 ['Compelling event', 'What happens with the Helix MES renewal, and when?', 'Deadline: bundle lock-in if Strata is not in by then'],
 ['Compelling event', 'What would have to be true for you to act this financial year?', 'Tests urgency; avoids "no decision"'],
 ['Competition', 'Who else have you looked at? What did you like about each?', 'Helix, TrueSense, BMI positioning'],
 ['Competition', 'Why did the 2024 conversation with us not go anywhere?', 'Past loss reason: fix it this time']];
const kids = [
  new Paragraph({ children: [r('D3 · Discovery plan: Ranganath Precision Components', { bold: true, size: 30, color: '1F3A5F' })] }),
  P([r('Strata Sense and Ranganath are fictional; synthetic case for an MBA capstone. Inputs: DR7 buyer dossier, DR5 competitor dossier, D1–D2.', { italics: true, size: 16, color: '52514E' })]),
  H1('1. Deal hypothesis (to be proved or killed in discovery)'),
  P([B('Hypothesis. '), 'Unplanned downtime on RPC’s forging presses and critical machining is costing more than the MES shows. OEM delivery terms make it visible to the MD. The HelixAsset pilot only sees assets wired to Helix controls, so the costliest failures (hydraulic presses, compressors) sit outside it. Strata can win a paid pilot on the Chakan P2 forging line, backed by a CFO-grade business case built on RPC’s own numbers, before the Helix MES renewal locks in the bundle.']),
  P([B('What would kill it. '), '(a) The Helix pilot already covers presses and compressors well. (b) Downtime is genuinely low and costs little. (c) Security rules block any cloud connection and we cannot offer edge buffering. (d) No budget route this financial year. If two of these are true, we move RPC to a nurture track and say so.']),
  P([B('Why RPC now (D2 evidence). '), 'Strategic-tier account. The last attempt (FY25) died as "No decision" with one contact and no business case: exactly the two failure patterns D1 found across the funnel. This time the target is four or more contacts and a business case built on RPC’s numbers.']),
  H1('2. Question tree'),
  table(tree, [1300, 5000, 3906]),
  H1('3. Agendas by stakeholder'),
  H2('Plant head, Chakan P2 (45 minutes, on site)'),
  bul('5 min: purpose. "Understand where unplanned downtime hurts most; no pitch today."'),
  bul('20 min: plant walk-through of the worst stoppages last year; monitoring today; the HelixAsset pilot scope.'),
  bul('10 min: impact: OEE, OEM exposure, maintenance mix; who owns the cost-per-hour number.'),
  bul('10 min: agree next steps: access to the downtime log and maintenance records; introduction to finance.'),
  H2('CFO (30 minutes)'),
  bul('5 min: what we heard from operations (their numbers, not ours).'),
  bul('10 min: how finance values downtime and penalties; payback rule; capex or opex.'),
  bul('10 min: budget cycle, approval limits, committee dates; view on the Helix bundle.'),
  bul('5 min: agree the success criteria a business case must meet.'),
  H2('Procurement (30 minutes)'),
  bul('Vendor-onboarding steps and timeline; rate-contract rules; standard terms.'),
  bul('How they evaluate "free" bundled offers; total-cost-of-ownership format they accept.'),
  bul('Pilot commercial structure they have approved before.'),
  H2('IT / OT security (45 minutes)'),
  bul('Architecture requirements for OT data: cloud vs edge, network segmentation, data residency.'),
  bul('Certifications and questionnaire; review timeline; any recent incidents shaping policy.'),
  bul('Integration with MES and historian; who owns OT security now (role recently advertised).'),
  H1('4. Plan for the 20-minute role-play'),
  table([['Minutes', 'With', 'Must-ask questions (in order)', 'Numbers to capture'],
    ['0–12', 'Plant head', 'Worst 3 stoppages · Helix pilot scope and terms · confidence in MES downtime data · asset counts by type · maintenance mix · OEM impact · who else decides', 'Hours lost per event; asset counts; reactive %; penalty ₹'],
    ['12–20', 'CFO', 'Cost per hour by line type · payback rule and capex/opex · approval limit and committee dates · security requirements and why · view on Helix bundle', '₹ per hour; payback months; ₹ approval limit; dates']], [900, 1300, 5006, 3000]),
  P([B('Discipline. '), 'Ask about the last specific event, not averages. Repeat numbers back to confirm them. Do not pitch features. Use one fact in the next question (for example, turn a press failure into ₹ by asking finance for the press-line cost per hour).'], { spacing: { before: 80 } }),
  H1('5. Value-model inputs that must come from the buyer'),
  table([['Input', 'Pre-discovery placeholder (source)', 'Must be replaced by'],
    ['Assets by type, pilot plant', 'Group ~7,400 (DR7); per plant ~820 (7,400 ÷ 9)', 'Plant head count'],
    ['Downtime hours per year', 'None reliable (MES data quality unknown)', 'Plant head: worst events + corrected MES figure'],
    ['Cost per downtime hour', 'None', 'CFO: ₹ per hour by line type'],
    ['OEM penalties', 'Annual report mentions claims; amount unknown', 'Plant head / CFO: actual ₹'],
    ['Maintenance spend and reactive share', 'None', 'Plant head: budget and planned/reactive split'],
    ['Spares inventory; compressor energy', 'None', 'CFO: ₹ values'],
    ['Payback threshold; budget route', 'None', 'CFO']], [2700, 3700, 3806]),
];
const doc = new Document({ styles: { default: { document: { run: { font: 'Arial', size: 18 } } }, paragraphStyles: [
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 22, bold: true, color: '1F3A5F' }, paragraph: { outlineLevel: 0 } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 19, bold: true, color: '333333' }, paragraph: { outlineLevel: 1 } }] },
  numbering: { config: [{ reference: 'b', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 220 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 850, bottom: 850, left: 850, right: 850 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [r('Strata Sense · D3 discovery plan · page ', { size: 14, color: '52514E' }), new TextRun({ children: [PageNumber.CURRENT], size: 14, color: '52514E' })] })] }) }, children: kids }] });
Packer.toBuffer(doc).then(b => fs.writeFileSync('out/D3_1_Discovery_Plan.docx', b));
