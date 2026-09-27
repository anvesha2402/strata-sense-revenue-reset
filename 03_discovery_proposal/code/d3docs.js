const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, LevelFormat, AlignmentType, BorderStyle, Footer, PageNumber, PageBreak } = require('docx');
const W = 10206, r = (t, o = {}) => new TextRun({ text: t, ...o });
const P = (x, o = {}) => new Paragraph({ spacing: { after: 90, line: 264 }, ...o, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const H1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 180, after: 70 }, keepNext: true, children: [r(t)] });
const B = t => r(t, { bold: true });
const bul = x => new Paragraph({ numbering: { reference: 'b', level: 0 }, spacing: { after: 50, line: 259 }, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const num = (x, ref = 'n') => new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 50, line: 259 }, children: (Array.isArray(x) ? x : [x]).map(y => typeof y === 'string' ? r(y) : y) });
const bd = { style: BorderStyle.SINGLE, size: 4, color: 'C9C8C2' };
let CS = 16;
const cell = (t, w, h, fill) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders: { top: bd, bottom: bd, left: bd, right: bd }, shading: h ? { type: ShadingType.CLEAR, fill: '1F3A5F', color: 'auto' } : (fill ? { type: ShadingType.CLEAR, fill, color: 'auto' } : undefined), margins: { top: 40, bottom: 40, left: 80, right: 80 }, children: [new Paragraph({ children: [r(String(t), { bold: h, color: h ? 'FFFFFF' : undefined, size: CS })] })] });
const table = (rows, cols, boldLast = false) => new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cols, rows: rows.map((rw, i) => new TableRow({ cantSplit: true, tableHeader: i === 0, children: rw.map((t, j) => cell(t, cols[j], i === 0, (boldLast && i === rows.length - 1) ? 'E8EEF5' : undefined)) })) });
const small = t => P([r(t, { size: 15, italics: true, color: '52514E' })], { spacing: { after: 100 } });
const head = (t, sub) => [new Paragraph({ spacing: { after: 40 }, children: [r(t, { bold: true, size: 30, color: '1F3A5F' })] }), P([r(sub, { italics: true, size: 16, color: '52514E' })], { border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '1F3A5F', space: 4 } } })];
const styles = { default: { document: { run: { font: 'Arial', size: 19 } } }, paragraphStyles: [{ id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 23, bold: true, color: '1F3A5F' }, paragraph: { outlineLevel: 0 } }] };
const numbering = { config: [{ reference: 'b', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 220 } } } }] },
  { reference: 'n', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 260 } } } }] },
  { reference: 'n2', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 260 } } } }] }] };
const page = { size: { width: 11906, height: 16838 }, margin: { top: 850, bottom: 850, left: 850, right: 850 } };
const foot = t => ({ default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [r(t + ' · page ', { size: 14, color: '52514E' }), new TextRun({ children: [PageNumber.CURRENT], size: 14, color: '52514E' })] })] }) });
const save = (kids, f, ft) => Packer.toBuffer(new Document({ styles, numbering, sections: [{ properties: { page }, footers: foot(ft), children: kids }] })).then(b => fs.writeFileSync('out/' + f, b));

// ================= DEBRIEF (1 page)
save([
  ...head('D3 · Discovery debrief: Ranganath Precision Components', 'Role-play, Week 3: Suresh Kulkarni (Plant Head, Chakan P2), then Kavita Rao (CFO). Fictional company; synthetic case (MBA capstone).'),
  H1('What we learned (and from whom)'),
  table([['Fact', 'Source', 'Why it matters'],
    ['HelixAsset pilot: ~300 CNC spindles only; free until 31 Dec 2026; no written success criteria; presses, hydraulics, compressors, chillers not covered', 'Suresh', 'Uncovered critical assets = our landing zone; no need to fight Helix on spindles'],
    ['"Free" requires a 3-year Helix MES renewal due Dec 2026; list price after year 1; procurement likes "free"', 'Kavita', 'Compare 3-year cost, not year 1; our deadline is the MES renewal'],
    ['Suresh was not consulted on the pilot', 'Suresh', 'Likely champion'],
    ['3 major press failures in FY26, 36–60 h each; Nov: 52 h and an OEM line stop', 'Suresh', 'Core value driver'],
    ['Press line ₹5.5 lakh/h, machining ₹2.4 lakh/h; Nov OEM penalty ₹1.2 cr (₹8 lakh/h × ~15 h)', 'Kavita', 'Buyer-owned ₹ numbers for the business case'],
    ['MES downtime unreliable: ~40% coded "Other"; reported 2.1% vs ~4% believed; paper press log exists', 'Suresh / Kavita', 'Baseline must come from the paper log, not MES'],
    ['Maintenance ₹6.5 cr/yr, ~55% reactive; monthly handheld rounds on 400 of ~1,150 assets', 'Suresh', 'Secondary value; scope sizing'],
    ['Opex up to ₹1.5 cr/yr on CFO signature; committee 15 Jul / 15 Oct; payback < 12 months, conservative; open to fees at risk', 'Kavita', 'Keep the offer under ₹1.5 cr to avoid the committee'],
    ['Oct 2025 ransomware at Manesar → edge buffering only, ISO 27001 + SOC 2 Type II, data in India, 8–10 week review', 'Kavita', 'Security gate sets the timeline'],
    ['Spares ₹5.2 cr (plant) / ₹38 cr (group); power ₹62 cr, compressors ~18%; group maintenance ₹46 cr; presses also at 2 Chennai plants', 'Kavita', 'Scale path; minor value drivers']], [5600, 1300, 3306]),
  H1('What changed my view'),
  bul([B('Confirmed: '), 'the Helix pilot leaves the costliest assets uncovered. We complement Helix rather than replace it.']),
  bul([B('New: '), 'security, not price, is the critical path. A contract under ₹1.5 cr a year can be signed by the CFO alone, so the right offer skips the committee.']),
  bul([B('New: '), 'the conservative case must exclude OEM penalties and energy (Kavita discounts them) and rest on the paper press log.']),
  H1('Continue? Yes, with conditions'),
  P('Economic buyer (Kavita) identified and engaged; likely champion (Suresh); pain quantified in the buyer’s own rupees; a compelling event (MES renewal, Dec 2026); a concrete next step agreed. Conservative payback on the press line is about 3 months, well inside her 12-month rule.'),
  P([B('Stop conditions: '), 'security review not started by 31 May; paper logs not shared; or no pilot decision by 31 July. '], {}),
  P([B('Role-play score: '), '13 of 14 hidden facts uncovered. Missed: what Suresh is personally measured on (a likely OEE target), which would have sharpened his reason to champion the pilot.']),
  P([B('Gaps: '), 'what Suresh is personally measured on; Prakash Iyer (VP Manufacturing), Arvind (CIO, owns the Helix relationship), the CISO and Neha not yet met; competitors (TrueSense) not discussed.']),
], 'D3_3_Debrief.docx', 'Strata Sense · D3 debrief');

// ================= NEGOTIATION (1-2 pages)
save([
  ...head('D3 · Negotiation plan: procurement asks for 30% off and a free pilot', 'Counterpart: Neha Joshi, Head of Procurement. Fictional; synthetic case.'),
  H1('Our position in one line'),
  P('We trade price for commitment, never for nothing. The pilot fee is credited in full on conversion, so a successful pilot costs RPC nothing. Discount stops at 15%, and every point buys a commitment.'),
  H1('Give-and-get table'),
  table([['Neha asks', 'We give', 'We get in return', 'Cost to Strata'],
    ['Free pilot', 'Pilot fee (₹25 lakh) credited 100% to year 1 if RPC converts within 60 days of a successful readout', 'Written success criteria and conversion price agreed before the pilot starts', 'Zero if converted; hardware at cost if not'],
    ['"Free pilot, no strings"', 'Pilot at no charge', 'Signed conversion order (Better scope, agreed price) that triggers automatically if the success criteria are met', 'Hardware ~₹18 lakh at risk'],
    ['30% off', 'Up to 8%', '3-year term', 'Margin'],
    ['', 'Up to 3%', 'Annual payment in advance', 'Cash benefit to us offsets'],
    ['', 'Up to 5%', 'Signed option to extend to a Chennai forging plant within 12 months', 'Margin, offset by scale'],
    ['', 'Up to 2%', 'Named reference and case study after 6 months', 'Low'],
    ['"Match Helix year-1 free"', 'Hardware as a service: one-offs spread over 36 months', 'Keeps the annual fee (~₹0.78 cr) inside Kavita’s own limit; no discount', 'Financing cost only'],
    ['Lower risk', '15% of subscription at risk against avoided-downtime hours', 'Baseline from the paper press log; measurement agreed up front', 'Upside if we perform'],
    ['Price protection', 'Same per-asset price for Chennai for 18 months', 'Chennai option signed', 'Low']], [1700, 3000, 3606, 1900]),
  H1('Walk-away point'),
  bul([B('Price: '), 'below ₹10,625 per asset per year (15% off list), or any discount without a matching commitment.']),
  bul([B('Pilot: '), 'a free pilot with neither success criteria nor a conversion price.']),
  bul([B('Timeline: '), 'security review not started by 31 May, which makes a decision before the December MES renewal impossible.']),
  bul([B('Our alternative if we walk: '), 'keep Suresh as a champion, share a 3-year cost comparison with Kavita before the MES renewal, and revisit at the January committee.']),
  H1('Opening script'),
  P('"Neha, I understand ‘free’ looks good on the Helix line. Two things. First, Kavita asked for three-year cost, and the Helix offer is free only with a three-year MES lock-in; after that it goes to list. Second, we’ll make the pilot free in effect: every rupee is credited if it works. What I can’t do is discount without something back. If you can give me a three-year term and the Chennai option, I can move 13%. That is the most I can do, and here is exactly what each point buys."'),
  small('Numbers: D3_4_Value_Model.xlsx (Discount_Rules, Scope_Price). FY26 company average discount was 19% and did not raise win rates (D1), which is why the cap is 15%.'),
], 'D3_6_Negotiation_Plan.docx', 'Strata Sense · D3 negotiation');

// ================= PROPOSAL (~8 pages)
CS = 18;
const prop = [
  ...head('Proposal to Ranganath Precision Components Ltd', 'Protecting the Chakan Plant 2 press line: a paid pilot, then scale. Prepared for Kavita Rao (CFO) and Suresh Kulkarni (Plant Head). Strata Sense and RPC are fictional; synthetic case (MBA capstone).'),
  H1('Summary'),
  P('Three press failures cost Chakan Plant 2 between 36 and 60 hours each last year. One of them stopped an OEM customer’s line and cost ₹1.2 crore in penalties. None of the assets that failed is covered by today’s monitoring: handheld rounds are monthly, and the HelixAsset pilot sees only CNC spindles wired to Helix controls.'),
  P([B('We propose '), 'a four-month paid pilot on the press line (162 assets), then conversion to the "Better" scope (422 assets: presses, compressors and critical utilities). The pilot fee is credited in full on conversion. The contract stays inside the CFO’s own approval limit.']),
  table([['', 'Conservative', 'Base', 'Upside'],
    ['Annual value, Better scope (₹ cr)', '1.30', '3.99', '7.48'],
    ['Annual fee incl. hardware as a service (₹ cr)', '0.78', '0.78', '0.78'],
    ['Payback (months)', '7.1', '2.3', '1.2']], [4200, 2000, 2000, 2006]),
  small('Conservative case: no OEM penalties, no energy savings, the shortest outages Suresh reported, and one in three press failures caught early. It meets RPC’s 12-month payback rule.'),
  H1('What we heard'),
  table([['What RPC told us', 'Who'],
    ['3 major press failures in FY26, 36–60 hours each; November: 52 hours, OEM line stopped', 'Suresh Kulkarni'],
    ['Press line loses ₹5.5 lakh of contribution per hour; machining ₹2.4 lakh', 'Kavita Rao'],
    ['OEM penalty ₹8 lakh per hour of their line stoppage; ₹1.2 crore in November', 'Kavita Rao'],
    ['MES downtime codes are unreliable (~40% "Other"); the press team keeps a paper log', 'Suresh / Kavita'],
    ['Maintenance ₹6.5 crore a year, about 55% reactive; monthly handheld rounds on 400 assets', 'Suresh Kulkarni'],
    ['HelixAsset pilot: CNC spindles only, free to Dec 2026 with a 3-year MES renewal', 'Suresh / Kavita'],
    ['Security: edge buffering only, ISO 27001 + SOC 2 Type II, data in India, 8–10 week review', 'Kavita Rao'],
    ['Payback under 12 months on conservative numbers; subscription preferred; open to fees at risk', 'Kavita Rao']], [7800, 2406]),
  Object.assign(H1('Scope options'), { __t: '3' }),
  table([['Option', 'Assets', 'Annual subscription (ARR)', 'One-off hardware & set-up', 'Annual fee with hardware as a service', 'Conservative payback'],
    ['Good: press line', '162 (22 presses + 140 hydraulic pumps/motors)', '₹0.20 cr', '₹0.34 cr', '₹0.34 cr', '3.2 months'],
    ['Better: + compressors & critical utilities (recommended)', '422', '₹0.53 cr', '₹0.64 cr', '₹0.78 cr', '7.1 months'],
    ['Best: every non-spindle asset', '670', '₹0.84 cr', '₹0.94 cr', '₹1.20 cr', '10.7 months']], [2400, 2000, 1500, 1500, 1500, 1306]),
  P('All options complement the HelixAsset pilot: the 480 CNC spindles stay with Helix and we can take its alerts into one view. We recommend Better because it covers the assets behind every failure RPC described, pays back inside the rule on conservative numbers, and keeps the annual fee (₹0.78 cr) inside the CFO’s own ₹1.5 cr limit.'),
  H1('The business case'),
  table([['Driver (Better, ₹ cr a year)', 'Conservative', 'Base', 'Upside', 'Where the numbers come from'],
    ['Press downtime avoided', '1.18', '2.97', '5.64', 'Failures, hours (Suresh); ₹5.5 lakh/h (Kavita); share caught early (pilot to prove)'],
    ['OEM penalties avoided', '0.00', '0.30', '0.54', '₹1.2 cr event (Kavita); conservative counts none'],
    ['Machining downtime from utility failures', '0.00', '0.48', '0.96', '₹2.4 lakh/h (Kavita); hours to confirm from paper logs'],
    ['Reactive maintenance saved', '0.13', '0.19', '0.26', '₹6.5 cr, 55% reactive (Suresh)'],
    ['Compressor energy', '0.00', '0.05', '0.09', '₹62 cr bill, 18% compressors (Kavita); conservative = 0'],
    ['Total', '1.30', '3.99', '7.48', ''],
    ['One-off cash from lower spares', '0.09', '0.15', '0.18', '₹5.2 cr inventory (Kavita)']], [2500, 1400, 1000, 1000, 4306], false),
  P([B('The number that came from RPC: '), 'the conservative case is 90% press downtime, and every input to that line except the detection rate came from Suresh or Kavita: three failures a year, 36 hours each, ₹5.5 lakh an hour. The detection rate (one in three) is our assumption, and it is what the pilot is designed to prove.']),
  Object.assign(H1('Pilot-to-scale commercial structure'), { __t: '5' }),
  table([['Phase', 'Scope and timing', 'Commercials'],
    ['0. Security review', 'Security pack to the CISO this week; review ~8–10 weeks (May–July); edge server, no direct OT-to-cloud link, data in India', 'No charge'],
    ['1. Paid pilot', 'Press line, 162 assets, 4 months (July–November); baseline from the paper press log', '₹25 lakh, credited 100% to year 1 on conversion; within CFO signature'],
    ['2. Convert (Better)', '422 assets from December, before the MES renewal decision', '₹12,500 per asset per year (list); hardware as a service over 36 months; ~₹0.78 cr a year; within CFO signature'],
    ['3. Scale', 'Chennai forging plants; group roll-out to the committee (Jan 2027)', 'Same per-asset price held for 18 months if the option is signed']], [1900, 5000, 3306]),
  P([B('Pilot success criteria (agreed before start). '), '(1) At least two developing faults on press hydraulics or compressors flagged at least 7 days ahead and confirmed on inspection. (2) No major press failure from a monitored failure mode goes undetected. (3) The CISO signs off the architecture and there are no security findings. (4) The maintenance team acts on at least 80% of alerts within 48 hours.']),
  P([B('Fee at risk (optional). '), '15% of the annual subscription is paid only if agreed avoided-downtime hours are achieved, measured against the paper-log baseline.']),
  H1('Three-year cost against the alternatives (press line)'),
  table([['', 'Strata Cortex', 'HelixAsset', 'TrueSense AI'],
    ['Three-year cost (₹ cr)', '0.95', '0.60', '0.61'],
    ['Why', 'Sensors on presses and hydraulics; edge buffering', 'Year 1 free only with a 3-year MES lock-in; presses need Helix sensors', 'Needs sensors RPC does not have on presses; weaker on hydraulic and low-speed assets'],
    ['Share of press failures caught early (base, to prove)', '50%', '20% (assumption)', '30% (assumption)'],
    ['Three-year net value, base (₹ cr)', '9.18', '3.65', '5.60']], [2800, 2400, 2500, 2506]),
  P('We are the more expensive option by about ₹0.35 cr over three years. That premium is worth paying only if we catch more press failures, which is why detection is the first pilot criterion. Separately, RPC can renew the MES without accepting the three-year HelixAsset lock-in.'),
  Object.assign(H1('Implementation and mutual action plan'), { __t: '7' }),
  table([['By', 'Step', 'Owner'],
    ['30 Apr', 'Security documentation to the CISO; paper press logs shared; 30-minute review with Kavita (conservative case)', 'Strata; Suresh; Kavita'],
    ['15 May', 'Architecture workshop: edge server, network segmentation, India data residency', 'CISO / Arvind; Strata SE'],
    ['10 Jul', 'Security review complete', 'CISO'],
    ['15 Jul', 'Pilot SOW and success criteria signed (₹25 lakh)', 'Kavita; Suresh'],
    ['20 Jul – 20 Nov', 'Pilot live; fortnightly reviews with Suresh', 'Joint'],
    ['30 Nov', 'Readout and conversion decision (Better, within CFO limit)', 'Kavita; Prakash Iyer'],
    ['Jan 2027', 'Chennai / group proposal to the Capex & IT Committee', 'Kavita']], [1700, 6300, 2206]),
  Object.assign(H1('Commercial terms, discount rules and risks'), { __t: '8' }),
  P('List price ₹12,500 per asset per year. Any discount is traded for a commitment, up to 15% in total: 8% for a three-year term, 3% for annual payment in advance, 5% for a signed Chennai option, 2% for a reference and case study. We do not discount hardware below cost or offer a free pilot without agreed conversion terms.'),
  P([B('Risks we are managing. '), 'The security review slips (mitigation: submit this week; edge architecture ready). The detection rate is lower than assumed (mitigation: the pilot measures it; fee at risk). The Helix bundle is signed first (mitigation: readout before the December MES decision; three-year cost comparison shared now).']),
  small('Detailed model: D3_4_Value_Model.xlsx. All ₹ in crore unless stated.'),
];
function propBody() { const PBk = () => new Paragraph({ children: [new PageBreak()] }); const o = []; prop.slice(2).forEach(p => { if (p && p.__brk) o.push(PBk()); o.push(p); }); return o; }
const PB = () => new Paragraph({ children: [new PageBreak()] });

const cover = [
  new Paragraph({ spacing: { before: 2400, after: 200 }, children: [r('Proposal', { size: 28, color: 'EB6834', bold: true })] }),
  new Paragraph({ spacing: { after: 200 }, children: [r('Protecting the Chakan Plant 2 press line', { size: 52, bold: true, color: '1F3A5F' })] }),
  new Paragraph({ spacing: { after: 600 }, children: [r('A paid pilot, then scale: a business case built on Ranganath\u2019s own numbers', { size: 28, color: '52514E' })] }),
  P([B('Prepared for: '), 'Kavita Rao, Chief Financial Officer · Suresh Kulkarni, Plant Head, Chakan Plant 2']),
  P([B('Copy: '), 'Prakash Iyer, VP Manufacturing Operations · Arvind Menon, CIO · Neha Joshi, Head of Procurement']),
  P([B('From: '), 'Strata Sense Technologies · Week 4, FY27 (April 2026)']),
  new Paragraph({ spacing: { before: 1600 }, children: [r('Strata Sense Technologies and Ranganath Precision Components are fictional; all data synthetic (MBA capstone).', { size: 16, italics: true, color: '52514E' })] }),
  PB()];
const why = [H1('Why Strata, and what we will not claim'),
  bul([B('Built for the assets that failed. '), 'Our sensors and models cover hydraulic, low-speed and reciprocating assets such as press pumps and compressors, including acoustic detection of leaks, which PLC tags and route-based rounds miss.']),
  bul([B('Proof from similar plants. '), 'A two-plant Strata customer in discrete manufacturing uses 97% of the assets it licenses; an auto-components customer expanded its subscription by 37% last year. (References available under NDA.)']),
  bul([B('Works alongside Helix. '), 'We do not ask RPC to remove the HelixAsset pilot. Spindle alerts stay with Helix; we cover what it cannot see.']),
  bul([B('What we will not claim. '), 'We will not promise a detection rate before the pilot measures it, and we will not count OEM penalties or energy in the case RPC signs against.']),
  H1('An architecture that meets your CISO\u2019s rules'),
  table([['Rule (from Kavita Rao)', 'How the design meets it'],
    ['No direct connection from the OT network to the cloud', 'Sensors report to an on-premise edge server inside the plant; only encrypted, summarised data leaves through RPC\u2019s IT DMZ on a schedule RPC controls'],
    ['ISO 27001 and SOC 2 Type II', 'Certificates and latest audit reports in the security pack sent this week'],
    ['Data stays in India', 'Hosted in an Indian cloud region; no data leaves India; RPC owns the data'],
    ['8–10 week security review before pilot', 'Review starts now so the pilot can begin in July; our security engineer joins the architecture workshop']], [3600, 6606]),
  H1('Team and governance'),
  table([['Role', 'Strata person', 'Commitment'],
    ['Executive sponsor', 'Regional VP, Strata', 'Monthly review with Kavita and Prakash'],
    ['Account executive', 'Named AE', 'Single point of contact; mutual action plan owner'],
    ['Solutions engineer', 'Named SE', 'On site weekly during installation; fortnightly reviews with Suresh'],
    ['Reliability analyst', 'Strata analytics team', 'Reviews every alert with the maintenance team for the first 90 days'],
    ['Customer success manager', 'Named CSM', 'Adoption tracking from day 1; readout pack for the conversion decision']], [2600, 2600, 5006])];
function order() {
  const body = prop.slice(2);
  const find = (txt) => body.findIndex(p => p && p.__t === txt);
  return [...cover, ...body.slice(0, find('3')), ...why.slice(0, 5), PB(), ...body.slice(find('3'), find('5')), PB(), ...body.slice(find('5'), find('7')), PB(),
    ...why.slice(5, 7), ...body.slice(find('7'), find('8')), ...why.slice(7), PB(), ...body.slice(find('8')), ...appx];
}
const appx = [H1('Appendix: assumptions and sources'),
  table([['Assumption', 'Value (C / B / U)', 'How we will test it'],
    ['Share of major press failures caught early', '33% / 50% / 67%', 'Pilot criterion 1; compared with the paper press log'],
    ['Share of outage hours avoided when caught early', '60% / 75% / 85%', 'Planned-repair duration logged for each caught fault'],
    ['Machining hours saved from utility failures (Better)', '0 / 20 / 40 per year', 'Paper logs for compressor and chiller stoppages'],
    ['Cut in reactive maintenance cost on monitored assets', '8% / 12% / 16%', 'Maintenance hours before and after, from Suresh\u2019s team'],
    ['Compressor energy saved', '0% / 4% / 7%', 'Leak survey during the pilot'],
    ['Edge server cost', '₹8 lakh', 'Confirmed in the architecture workshop']], [3800, 2400, 4006]),
  small('Buyer-supplied inputs: failures, hours, cost per hour, penalties, maintenance spend, spares, power and approval rules, all from the Week 3 discovery meetings with Suresh Kulkarni and Kavita Rao. Prices: Strata list (DR5). Model: D3_4_Value_Model.xlsx.')];
// insert page breaks before major sections
const idx = (t) => prop.findIndex(p => p === t);
const out = [...cover];
prop.slice(2).forEach(p => out.push(p));
const final = [];
out.forEach((p, i) => { final.push(p); });
Packer.toBuffer(new Document({ styles: { default: { document: { run: { font: 'Arial', size: 21 } } }, paragraphStyles: [{ id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 28, bold: true, color: '1F3A5F' }, paragraph: { outlineLevel: 0, spacing: { before: 240, after: 120 } } }] }, numbering,
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } }, footers: foot('Strata Sense · Proposal to Ranganath Precision Components'),
  children: order() }] })).then(b => fs.writeFileSync('out/D3_5_Proposal.docx', b));
