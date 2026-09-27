# The Strata Sense Revenue Reset

An 8-deliverable B2B SaaS revenue turnaround, run end to end for an MBA practice capstone: diagnose why growth stalled, build a three-year plan back to it, defend it to a board, and then implement the plan's CRM rules in a live system.

**Strata Sense Technologies is a fictional company.** There was no real instructor or data room for this assignment, so the entire data room (CRM export, account master, finance pack, interviews, competitor and partner files) was built synthetic, calibrated to the brief, with flaws planted blind so the cleaning and diagnosis were genuine tests. No real company, person or result is represented.

## The problem

Strata Sense, a ₹310 crore ARR industrial predictive-maintenance company (sensors plus analytics software), was growing more slowly every year: win rate fell from 27% to 17% in three years, net revenue retention from 118% to 99%, and forecasts missed by a quarter. The board asked for a plan to grow ARR 15% / 20% / 22% over FY27–29 inside tight financial guardrails.

## What's here

| Folder | Deliverable | Headline |
|---|---|---|
| [`01_diagnostic`](01_diagnostic) | D1 — Diagnostic and hypothesis test | ₹55 cr/yr of root causes ranked; 1 of 6 hypotheses rejected |
| [`02_account_planning`](02_account_planning) | D2 — Account planning and lead generation | 400 / 1,100 / 1,600 account tiers; capacity fits the need, thinly |
| [`03_discovery_proposal`](03_discovery_proposal) | D3 — Discovery to proposal | Live buyer role-play; 13 of 14 hidden facts found; 7.1-month payback |
| [`04_pipeline_forecast`](04_pipeline_forecast) | D4 — Pipeline and forecasting | Hold-out forecast error 23.3%, locked before the outcome was known |
| [`05_battlecards`](05_battlecards) | D5 — Competitive battlecards | Helix is a packaging problem, not a positioning one |
| [`06_channel_strategy`](06_channel_strategy) | D6 — Channel partner expansion | Break-even ₹0.24 cr sourced ARR per partner; 25% share is a coin flip |
| [`07_integrated_model`](07_integrated_model) | D7 — Integrated model and three-year plan | ₹526 cr FY29 ARR plan, ~1,400 formulas, no plugs; 1 disclosed guardrail breach |
| [`08_board`](08_board) | D8 — Board presentation and CEO memo | ₹14.95 cr ask, 6 hires, gated on Q2 FY27 triggers |
| [`data`](data) | Shared data-room files each deliverable's code reads from | DR1b hold-out snapshot, buyer dossier, competitor dossier, partner file |

Each deliverable folder has its own `README.md`, its own `code/` (the scripts that produce every number and chart), and its finished output files. Run order and dependencies are noted per folder — most read from `../../data/` or from an earlier deliverable's `out/`.

## The plan

Invest ₹14.95 crore in FY27 (inside a ₹15 crore cap): re-tier the sales effort onto the 1,500 of 3,100 accounts that actually convert, sell on proven value with a 15% discount cap, protect Helix-exposed renewals, build a small partner channel in South-East Asia and the Gulf, hire six salespeople from Q3, and gate a reserve on Q2 results. The model takes ARR to ₹351 / ₹423 / ₹526 crore (FY27–29), turns EBITDA positive in FY28, and pays back in about 8 months against doing nothing (₹389 crore by FY29). One guardrail is breached and disclosed rather than hidden: Q1 FY27 CAC payback, which was locked before the plan existed.

Every number traces to one workbook with no plugs, four scenarios, a sensitivity and break-even analysis, and a cascade test. The Q1 FY27 forecast was locked before any outcome was seen and scored 23.3% error against actuals after the fact.

## What came next: a live CRM

The plan's "load the CRM" step wasn't left as a slide. The cleaned D1 accounts and the D4 open-pipeline snapshot were loaded into a free HubSpot CRM — 1,995 Company records and 279 Deal records on a 5-stage pipeline matching D4's stage names exactly. D4's stage exit criteria were written in as 8 computed Deal properties (HubSpot's stage objects have no field for exit-criteria text), and every reproducible hygiene flag was checked against D4's own published counts before being trusted: all five matched exactly, flagging 105 of 279 open deals (₹49.5 cr) for clean-up ahead of the Q2 FY27 review. That build — including an honest, row-by-row check of which of the plan's eleven Q2 trigger measures a CRM can and can't show — is written up in the final report below.

## Full report and project summary

- `Strata_Sense_Final_Project_Report.docx` / `.pdf` — the complete write-up: assignment, method, all 8 deliverables, the 4 mid-project injects, primary evidence and benchmarks, limitations, and the HubSpot build. Not included in this repo; ask for it alongside this one.
- A 5-slide project summary deck is available on request.

## Tools

Python (pandas, numpy, statsmodels) for data cleaning and modelling; Excel workbooks with live formulas (blue inputs, yellow key assumptions, black formulas), recalculated and error-checked; Word memos and PowerPoint decks generated from code so every figure traces to the analysis; a free HubSpot CRM for the implementation step.


Anvesha · MBA Year 2 (PGDM), Prin. L.N. Welingkar Institute of Management Development and Research (WeSchool)
