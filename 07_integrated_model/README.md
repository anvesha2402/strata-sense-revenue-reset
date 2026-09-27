# 07 Integrated revenue model and three-year plan (D7) + Inject 4

Strata Sense Technologies is fictional; all data synthetic (MBA capstone).

- `D7_Integrated_Model.xlsx`: one workbook owns every number. Assumptions with scenario switch (Base, Downside, Aggressive, CFO-capped) and sensitivity shifts; Capacity (AE cohorts, ramp, attrition); Bookings (capacity × win rate × deal; pipeline required); Channel (partner ARR, channel P&L); quarterly ARR bridge FY27–FY29; P&L with gross margin incl. partner margin, CAC payback; Investment (₹15 cr envelope, payback vs do-nothing); Inject4 (Vajra re-tender); Checks; Cascade (+3 pts win rate); Traceability. ~1,400 formulas, no plugs.
- `D7_Plan_Memo.docx/.pdf`: 11-page plan memo: recommendation, programmes, ARR delivery and defended shortfalls, capacity and pipeline arithmetic, P&L and payback, scenarios, sensitivity and break-even, cascade test, Inject 4 retention plan, sequencing, risks, Q1–Q2 FY27 triggers, traceability map.
- `code/`: model.py builds the workbook; run_scenarios.py recalculates it under each scenario and shift (LibreOffice) and finalize.py writes the saved-run sheets.

AI use: model and drafting produced with an AI assistant (Claude).
