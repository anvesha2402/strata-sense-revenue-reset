const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, LevelFormat, AlignmentType, BorderStyle } = require('docx');
const W = 10206, r = (t, o = {}) => new TextRun({ text: t, ...o });
const P = (x, o = {}) => new Paragraph({ spacing: { after: 80, line: 259 }, ...o, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const H1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 150, after: 60 }, keepNext: true, children: [r(t)] });
const B = t => r(t, { bold: true });
const bul = x => new Paragraph({ numbering: { reference: 'b', level: 0 }, spacing: { after: 40, line: 252 }, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const bd = { style: BorderStyle.SINGLE, size: 4, color: 'C9C8C2' };
const cell = (t, w, h, hl) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders: { top: bd, bottom: bd, left: bd, right: bd }, shading: h ? { type: ShadingType.CLEAR, fill: '1F3A5F', color: 'auto' } : (hl ? { type: ShadingType.CLEAR, fill: 'E8EEF5', color: 'auto' } : undefined), margins: { top: 35, bottom: 35, left: 70, right: 70 }, children: String(t).split('\n').map(line => new Paragraph({ spacing: { after: 20 }, children: [r(line, { bold: h || hl, color: h ? 'FFFFFF' : undefined, size: 16 })] })) });
const table = (rows, cols, hlRow = -1) => new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cols, rows: rows.map((rw, i) => new TableRow({ cantSplit: true, children: rw.map((t, j) => cell(t, cols[j], i === 0, i === hlRow)) })) });
const small = t => P([r(t, { size: 15, italics: true, color: '52514E' })]);
const kids = [
  new Paragraph({ spacing: { after: 30 }, children: [r('Memo to the CEO: the revenue reset, and what I need from the board', { bold: true, size: 28, color: '1F3A5F' })] }),
  P([r('From the Revenue Strategy Lead · Week 9 FY27 · Strata Sense is fictional; data synthetic. Every number is from D7_Integrated_Model.xlsx.', { italics: true, size: 16, color: '52514E' })], { border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '1F3A5F', space: 4 } } }),
  H1('The recommendation'),
  P([B('Approve ₹14.95 crore of FY27 investment (inside the ₹15 crore cap), six net new AEs starting Q3, three channel roles, and a ₹1.9 crore reserve released only if Q2 targets are met. '), 'The plan takes ARR from ₹310 crore to ₹351 crore (FY27), ₹423 crore (FY28) and ₹526 crore (FY29), ahead of the board’s ₹522 crore. It breaks even on EBITDA in FY28 (₹2.6 crore) and earns ₹52.6 crore in FY29. Doing nothing leaves us at ₹389 crore.']),
  P([B('The trade-off I am asking you to accept: '), 'FY27 grows 13.2%, not 15% (₹5.6 crore short). Q1 was set by the pipeline on 1 April, and new AEs take a year to become productive. Buying the gap with the extra ₹3 crore does not pay back inside the CFO’s 15 months.']),
  H1('Why growth stalled, in one paragraph'),
  P('Win rate fell from 27% to 17% and NRR from 118% to 99% in three years. The biggest cause (₹34 crore a year) is Helix bundling our category into its automation contracts; that is a packaging problem, not a sales problem. The rest is ours to fix: AEs spent 62% of their time on accounts that produce 12% of wins, deals were single-threaded, and discounts rose without buying wins. The plan fixes these three and about a third of the Helix loss.'),
  H1('What changes'),
  bul([B('First 30 days: '), 'tiers applied to territories; discounts above 15% need the CFO; Commit means stage 5; Helix-tied partners restricted; CEO meeting with Vajra.']),
  bul([B('By day 60: '), 'retention squad and value-selling training live; three SEA partners signed; offers out to six AEs.']),
  bul([B('By day 90: '), 'the Q2 review decides whether the reserve is released.']),
  bul([B('We stop: '), 'sending AEs to 1,600 low-touch accounts; matching Helix’s free offer; Commit calls before stage 5; planning on a six-month ramp; carrying dormant partners; hiring AEs to quota instead of to pipeline.']),
  H1('The three largest risks'),
  table([['Risk', 'Probability', 'Impact (model)', 'Fallback'], ['Helix pressure deeper (churn +2 pts)', '35%', '−₹23 cr FY29 ARR', 'Second retention squad; win-back when HelixAsset’s free period ends (Mar 2027)'],
    ['Win-rate programme stalls (−3 pts)', '30%', '−₹26 cr; payback breach at −0.7 pts', 'Hold reserve; move to CFO-capped path'], ['Hardware share does not fall', '35%', 'Gross margin 64.5% by FY29 (floor 66%)', 'Hardware price floor; software-led expansion; sensor-agnostic tier']], [2800, 1200, 2600, 3606]),
  H1('How the board will know: continue, adjust or stop at Q2'),
  P('Continue if win rate ≥ 18.0%, new qualified deals ≥ 95 a quarter, H1 churn and contraction ≤ ₹13.5 crore, H1 expansion ≥ ₹12.5 crore and payback ≤ 30 months. Adjust (hold the reserve) if win rate or pipeline misses. Stop the Q3 hires and come back to the board if win rate is below 17% and payback above 32 months.'),
  H1('Guardrails, and the one I am asking you to waive'),
  P('Investment, gross margin, S&M ratio, headcount and the Q4 FY28 payback test are all met. One is not: Q1 FY27 CAC payback is 31.0 months against 30, because its bookings were locked before the plan. I ask for an exception for that quarter only. Q3 FY27 is tight at 29.4 months, which is why the reserve is gated.'),
  H1('What I am least sure of'),
  P('That hardware will fall from ₹1.48 to ₹1.05 per rupee of new and expansion ARR. If it does not, ARR still grows but gross margin breaks the floor by FY28, and the sensor-agnostic tier becomes a margin necessity. I would rather the board knew this today than discover it in FY28.'),
];
Packer.toBuffer(new Document({ styles: { default: { document: { run: { font: 'Arial', size: 22 } } }, paragraphStyles: [{ id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 21, bold: true, color: '1F3A5F' }, paragraph: { spacing: { before: 120, after: 40 } } }] },
  numbering: { config: [{ reference: 'b', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 800, bottom: 800, left: 850, right: 850 } } }, children: kids }] })).then(b => fs.writeFileSync('out/D8_CEO_Memo.docx', b));
