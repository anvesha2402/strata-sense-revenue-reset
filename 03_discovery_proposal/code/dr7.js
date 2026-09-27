const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, LevelFormat, AlignmentType, BorderStyle } = require('docx');
const W = 9638, r = (t, o = {}) => new TextRun({ text: t, ...o });
const P = (x, o = {}) => new Paragraph({ spacing: { after: 90, line: 264 }, ...o, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const H = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 180, after: 80 }, children: [r(t)] });
const bul = t => new Paragraph({ numbering: { reference: 'b', level: 0 }, spacing: { after: 50 }, children: [r(t)] });
const bd = { style: BorderStyle.SINGLE, size: 4, color: 'C9C8C2' };
const cell = (t, w, h) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders: { top: bd, bottom: bd, left: bd, right: bd }, shading: h ? { type: ShadingType.CLEAR, fill: '1F3A5F', color: 'auto' } : undefined, margins: { top: 40, bottom: 40, left: 80, right: 80 }, children: [new Paragraph({ children: [r(t, { bold: h, color: h ? 'FFFFFF' : undefined, size: 18 })] })] });
const table = (rows, cols) => new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cols, rows: rows.map((rw, i) => new TableRow({ children: rw.map((t, j) => cell(t, cols[j], i === 0)) })) });
const kids = [
  new Paragraph({ children: [r('DR7 · Buyer dossier: Ranganath Precision Components Ltd', { bold: true, size: 30, color: '1F3A5F' })] }),
  P([r('Fictional company and people; synthetic data for an MBA capstone. This is what Strata knows before discovery: public information, a past CRM record and account intelligence.', { italics: true, size: 18, color: '52514E' })]),
  H('1. Company snapshot'),
  table([['Item', 'Detail'], ['Business', 'Tier-1 auto components: forged and machined crankshafts, steering knuckles, gear blanks, connecting rods'],
    ['Revenue / EBITDA (FY26)', 'About ₹2,300 cr; EBITDA margin about 13% (annual report)'],
    ['Customers', 'Three passenger-vehicle OEMs (about 70% of revenue), one two-wheeler OEM, exports to a European Tier-1'],
    ['Plants (9)', 'Chakan, Pune (3: P1, P2, P3) · Chennai (2) · Hosur (1) · Manesar (2) · Sanand (1)'],
    ['Installed rotating assets (est.)', 'About 7,400 across the group: CNC spindles, hydraulic forging presses, compressors, pumps, induction hardening, chillers'],
    ['Automation / MES', 'Helix Automation PLCs and MES at most plants; MES contract renewal expected in FY27'],
    ['Existing condition monitoring', 'Route-based (portable) vibration rounds at 4 plants; a small wireless-sensor trial at one Chennai plant'],
    ['Current initiative', 'Piloting HelixAsset (Helix’s asset-health module) at one Chakan plant since early 2026'],
    ['FY27 capex plan', 'About ₹180 cr (annual report); new EV-component line for an OEM programme']], [2800, 6838]),
  H('2. Public signals'),
  bul('Annual report FY26: "reducing unplanned downtime and improving OEE" named as an operations priority for FY27.'),
  bul('Annual report FY26: exceptional charge relating to "customer quality and delivery claims" (amount not broken out).'),
  bul('Trade press (Jan 2026): RPC wins a crankshaft contract for an OEM’s new EV-hybrid platform, with strict delivery-performance terms.'),
  bul('Job postings (Feb 2026): reliability engineer (Chakan) and OT security lead (corporate).'),
  H('3. People (from public profiles and past CRM notes)'),
  table([['Name', 'Role', 'What we know'], ['Venkat Ranganath', 'Managing Director (promoter family)', 'Final sign-off on large contracts; speaks publicly about OEM delivery performance'],
    ['Kavita Rao', 'Chief Financial Officer', 'Ex-Big 4; joined 2022'],
    ['Prakash Iyer', 'VP Manufacturing Operations (group)', 'Oversees all 9 plant heads'],
    ['Suresh Kulkarni', 'Plant Head, Chakan Plant 2', 'Long-tenured; runs the forging and machining plant where the Helix pilot sits'],
    ['Arvind Menon', 'Chief Information Officer', 'Owns MES and IT; leads the Helix MES relationship'],
    ['Neha Joshi', 'Head of Procurement', 'Rate-contract driven; known for hard negotiation'],
    ['(vacant / new)', 'OT Security Lead', 'Role advertised Feb 2026']], [2200, 2800, 4638]),
  H('4. Strata history with the account'),
  bul('FY25: Strata ran a demo for the Chennai plant maintenance team. Opportunity closed "No decision / budget" after 7 months; one contact engaged; no business case in the proposal.'),
  bul('No active opportunity today. Account sits in Strata’s strategic tier (D2).'),
  H('5. What we do not know (discovery targets)'),
  P('Terms of the Helix pilot; the real downtime picture and its cost; who decides and how the budget works; IT and security requirements; what has already been tried; what would make RPC act this year.'),
];
const doc = new Document({ styles: { default: { document: { run: { font: 'Arial', size: 20 } } }, paragraphStyles: [{ id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 24, bold: true, color: '1F3A5F' }, paragraph: { outlineLevel: 0 } }] },
  numbering: { config: [{ reference: 'b', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 460, hanging: 240 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } }, children: kids }] });
Packer.toBuffer(doc).then(b => fs.writeFileSync('dr/DR7_buyer_dossier_Ranganath.docx', b));
