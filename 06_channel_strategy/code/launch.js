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
  new Paragraph({ spacing: { after: 30 }, children: [r('D6 · Channel launch: the first 90 days', { bold: true, size: 30, color: '1F3A5F' })] }),
  P([r('Strata Sense is fictional; all data synthetic (MBA capstone). Economics: D6_Partner_Economics.xlsx. Strategy: D6_Channel_Strategy_Deck.pptx. Day 1 = approval of the channel plan (week 8, FY27).', { italics: true, size: 16, color: '52514E' })], { border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '1F3A5F', space: 4 } } }),
  H1('Goal for day 90'),
  P([B('Six of FY27’s eight partner activations signed (PR01, PR02, PR06, PR07, plus P07 and P10 reactivated), PR09/PR10 pilot scope agreed, 12 engineers in certification, ₹6 cr of registered partner pipeline, and zero unresolved conflicts. '), 'No partner revenue is expected in 90 days: DR6 puts first deals at 6–12 months. The 90 days build the rules, the team and the pipeline that make FY27’s ₹3.7 cr of partner-sourced ARR possible and FY28’s ₹9.9 cr likely.']),
  H1('Plan by month'),
  table([['Days', 'Actions', 'Owner', 'Done when'],
    ['1–30: rules and people', '• Publish tier terms (10% / 18% + 8% / 22% + 10% + services), deal-registration rules and conflict rules\n• Restrict P05 and P11 (Inject 3): letters sent, Helix-account registrations frozen, top deals moved to direct AEs with the D5 battlecard\n• Send exit notices to P01, P03, P04, P06, P14\n• Start VP Channel search; appoint interim owner (CRO’s chief of staff)\n• Load 14 partners and 12 prospects into CRM; add partner-source and registration fields (fixes D1 mis-tagging)', 'CRO; RevOps; Legal', 'Terms signed off by CFO; P05/P11 acknowledge restriction; CRM fields live'],
    ['31–60: sign and certify', '• Sign PR01 (Indonesia), PR02 (Thailand), PR06 (Singapore); term sheets to PR07 (Saudi), PR09 and PR10 (embed pilot)\n• Activation plans with P07 and P10: two engineers each into certification, joint list of 10 accounts\n• Run first certification cohort (installation and TrueSense analytics), demo kits shipped\n• Hire partner manager 1 (SEA)\n• AE comp plan updated: 50% quota credit on partner-sourced deals, counted once in bookings', 'Interim channel owner; Enablement; HR', '3 new partners signed; 8+ engineers enrolled; comp change communicated'],
    ['61–90: pipeline and review', '• Joint account plans: each active partner owns 10 named low-touch or SEA accounts (from D2 tiers)\n• First co-sell calls with SE support on at least 6 opportunities\n• Sign PR07; PR09/PR10 pilot scope agreed (sensor fitted to one machine model each)\n• Hire partner manager 2; VP Channel offer made\n• First quarterly scorecard for all active partners; partner-sourced ARR added as a forecast line (D4 process)', 'Partner managers; SE lead; VP Channel (if hired)', '₹6 cr registered pipeline; scorecard issued; forecast line live']], [1500, 5306, 1500, 1900]),
  H1('Measures we report every two weeks'),
  table([['Measure', 'Day 30', 'Day 60', 'Day 90', 'Why it matters'],
    ['Partners signed or reactivated (of 8 for FY27)', '0', '3', '6', 'Ramp: partners activated late in FY27 add almost nothing until FY28'],
    ['Engineers in certification / certified', '0 / 0', '8 / 0', '12 / 6', 'Silver needs 2 certified engineers, Gold 4'],
    ['Registered partner pipeline (₹ cr)', '—', '2', '6', 'About 10 qualified deals per mature partner a year'],
    ['Registration decisions within 48 hours', '—', '≥ 90%', '≥ 90%', 'Slow approvals are the main source of conflict'],
    ['Open conflicts older than 5 working days', '0', '0', '0', 'Measures whether the rules are working'],
    ['P05 / P11 registrations in Helix-incumbent accounts', '0', '0', '0', 'Inject 3 restriction holds']], [3200, 900, 900, 900, 4306]),
  H1('Budget in the first 90 days'),
  P('About ₹0.9 cr of the ₹3.94 cr FY27 channel budget: part-year partner manager (₹0.1 cr), recruiting fees for the VP Channel (₹0.15 cr), first certification cohort and demo kits (₹0.15 cr), PRM and CRM configuration (₹0.2 cr), and the first ₹0.3 cr of partner marketing funds, released only against signed joint plans. Channel roles stay at three in FY27, inside the limit of six, and fixed cost stays within the Inject 1 allocation of ₹2.84 cr.'),
  H1('Risks and what we do'),
  table([['Risk', 'Early sign', 'Response'],
    ['Helix-tied partners steer deals to Helix (Inject 3)', 'Registered deal switches to Helix; P05/P11 registrations in Helix accounts', 'Loss of tier immediately; move account to direct; review both at end-Q2'],
    ['SEA recruits slow to certify', 'Fewer than 8 engineers enrolled by day 60', 'Partner manager on site; certification fees waived for first cohort'],
    ['AEs resist partner deals', 'Registration disputes; AE-created duplicates on registered accounts', '50% quota credit; CRO rules on appeals; duplicate check in CRM'],
    ['VP Channel hire delayed', 'No offer by day 75', 'Interim owner continues; do not delay partner signings'],
    ['Partners perform like FY26 India partners', 'Registered pipeline under ₹3 cr at day 90', 'Stop FY27 wave-2 recruiting; kill gate at end-Q2 FY28 (fewer than 10 active or under ₹6 cr trailing partner ARR)']], [2800, 3300, 4106]),
  H1('Partner by partner: status on day 90'),
  table([['Partner', 'Decision (D6)', 'Day-90 target', 'If missed'],
    ['P02 Deccan', 'Keep: Gold', 'Gold terms signed; 4 open deals registered', 'Coach'],
    ['P09 Vindhya', 'Keep: Gold (services)', 'Managed-monitoring offer priced; 3 deals registered', 'Coach'],
    ['P12 Siam, P13 Al Fajr', 'Keep: Silver', 'Joint plan of 10 accounts each', 'Move to referral'],
    ['P05 Sahyadri, P11 Konkan', 'Fix: restricted (Inject 3)', 'Restriction acknowledged; non-Helix pipeline registered; disclosure on every deal', 'Exit at end-Q2 review'],
    ['P07 Mekong, P10 Penang', 'Fix: activate', '2 engineers each in certification; 10-account plan', 'Exit at end-Q2'],
    ['P08 Hosur', 'Fix: OEM pilot', 'Pilot scoped alongside PR09/PR10', 'Exit'],
    ['P01, P03, P04, P06, P14', 'Exit', 'Notices served; registrations closed', '—'],
    ['PR01, PR02, PR06', 'Recruit (Q1)', 'Signed; certification cohort 1', 'Escalate to CRO'],
    ['PR07', 'Recruit (Q2)', 'Signed by day 90', 'Slip to Q3'],
    ['PR09, PR10', 'Embed pilot', 'One machine model each agreed', 'Revisit in FY28'],
    ['PR03, PR04, PR11', 'Hold for FY28', 'Introductory meeting only', '—'],
    ['PR05, PR08, PR12', 'Deprioritise (Helix)', 'No contact', '—']], [2600, 2200, 3606, 1800]),
  P([B('Decision needed on day 1: '), 'approve the tier terms, the P05/P11 restriction, the five exits, three channel roles and ₹1.5 cr of partner marketing funds from the ₹24 cr programme budget.'], { spacing: { before: 100 } }),
];
Packer.toBuffer(new Document({ styles: { default: { document: { run: { font: 'Arial', size: 18 } } }, paragraphStyles: [{ id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 22, bold: true, color: '1F3A5F' }, paragraph: { spacing: { before: 150, after: 60 } } }] },
  numbering: { config: [{ reference: 'b', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 800, bottom: 800, left: 850, right: 850 } } }, children: kids }] })).then(b => fs.writeFileSync('out/D6_90Day_Launch_Plan.docx', b));
