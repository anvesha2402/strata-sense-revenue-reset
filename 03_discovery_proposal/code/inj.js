const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, LevelFormat, AlignmentType, BorderStyle } = require('docx');
const W = 10206, r = (t, o = {}) => new TextRun({ text: t, ...o });
const P = (x, o = {}) => new Paragraph({ spacing: { after: 90, line: 259 }, ...o, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const B = t => r(t, { bold: true });
const bul = x => new Paragraph({ numbering: { reference: 'b', level: 0 }, spacing: { after: 50, line: 252 }, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const bd = { style: BorderStyle.SINGLE, size: 4, color: 'C9C8C2' };
const cell = (t, w, h) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders: { top: bd, bottom: bd, left: bd, right: bd }, shading: h ? { type: ShadingType.CLEAR, fill: '1F3A5F', color: 'auto' } : undefined, margins: { top: 35, bottom: 35, left: 70, right: 70 }, children: [new Paragraph({ children: [r(t, { bold: h, color: h ? 'FFFFFF' : undefined, size: 16 })] })] });
const table = (rows, cols) => new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cols, rows: rows.map((rw, i) => new TableRow({ children: rw.map((t, j) => cell(t, cols[j], i === 0)) })) });
const kids = [
  new Paragraph({ children: [r('MEMO · Inject 1: FY27 envelope cut from ₹18 cr to ₹15 cr', { bold: true, size: 28, color: '1F3A5F' })] }),
  P([B('To: '), 'Rohan Bhatt (CFO)   ', B('cc: '), 'Meera Krishnan (CEO), Arjun Mehta (CRO)   ', B('From: '), 'Revenue Strategy Lead   ', B('Week: '), '3, FY27']),
  P([r('Fictional company; synthetic data (MBA capstone). Detail: Inject1_Envelope.xlsx.', { italics: true, size: 16, color: '52514E' })]),
  P([B('Recommendation. '), 'Accept the ₹15 cr cap. We do not request the extra ₹3 cr now. The plan still covers the FY27 new-logo need (D2: ₹49.4 cr capacity vs ₹46.5 cr) and the blended payback of the committed spend is 13.1 months on run-rate, inside your 15-month test.']),
  P([B('What changed from the ₹18 cr draft')]),
  table([['Change', 'Saves', 'Costs', 'Why it is the right trade'],
    ['12 AEs from H1 → 6 AEs from Q3', '₹4.5 cr in FY27', '≈ ₹1.0 cr FY27 ARR; ≈ ₹2.5 cr FY28 capacity unless the Q2 trigger releases more hires', 'New AEs book nothing for 6 months (D1); 12 H1 hires added only ₹1.1 cr FY27 ARR for ₹6 cr (D2)'],
    ['3 → 2 solutions engineers', '₹0.32 cr', 'Slower paid pilots in strategic accounts', 'Lowest-return item after hiring (16-month payback)'],
    ['Gated reserve ₹1.54 → ₹3.36 cr', '—', 'Money held, not spent', 'Released at the Q2 review only if triggers are met']], [2600, 1400, 2900, 3306]),
  P([B('What we protected, and why')], { spacing: { before: 100 } }),
  bul([B('Customer retention, expansion and AE retention (₹3.3 cr, 6–12-month payback). '), 'The installed base carries about two-thirds of the ARR at stake (D1). Retention squad 8.9 months; top-30 expansion 5.8 months; AE retention 11.8 months.']),
  bul([B('SEA channel foundation (₹2.8 cr incl. partner incentives, ~16-month payback on run-rate). '), 'It misses the 15-month test on its own, and we say so. We keep it because the FY29 goal of 25% partner-sourced ARR cannot be reached without it and SEA partner deals win 34% vs 10% direct.']),
  bul([B('Forecasting and value selling (₹1.9 cr). '), 'RevOps and tooling claim no ARR; value selling pays back in 13.5 months.']),
  P([B('The extra ₹3 cr: an option, not a request. '), 'One package would pass your test: a second retention squad for Helix-incumbent renewals (₹1.6 cr, ₹2.0 cr ARR protected, 14.1-month payback). Six more AEs in Q4 would not (21 months). We will bring the retention package to the Q2 review with evidence from the first squad and from the top-five re-tender risk.'], { spacing: { before: 100 } }),
  P([B('Reserve release triggers (Q2 FY27 review). '), 'Release up to ₹3.36 cr only if: strategic-tier qualified pipeline ≥ 50 opportunities created in H1; the first retention squad has protected ≥ ₹1 cr of ARR; Commit-to-booked conversion ≥ 40%. Otherwise the reserve returns to cash.']),
  P([B('What remains uncertain. '), 'The ARR gains per initiative are planning estimates drawn from D1–D2 evidence, and some overlap with the D2 capacity bridge (multi-threading, partners). D7 will reconcile them in one model so nothing is counted twice.']),
];
const doc = new Document({ styles: { default: { document: { run: { font: 'Arial', size: 18 } } } },
  numbering: { config: [{ reference: 'b', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 220 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 850, bottom: 850, left: 850, right: 850 } } }, children: kids }] });
Packer.toBuffer(doc).then(b => fs.writeFileSync('out/Inject1_CFO_Memo.docx', b));
