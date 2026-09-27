# 04 Pipeline and forecasting (D4)

Strata Sense Technologies is a fictional company; all data are synthetic, built for an MBA capstone.

- `D4_Forecast_Dashboard.xlsx`: dashboard (selector-driven performance views), coverage required vs reported, 8-quarter back-test, locked hold-out, hygiene rules and flagged deals, FY27–29 scenarios, governance
- `D4_Method_Note.docx`: method note (methods compared, calibration, range, hygiene, scenarios, governance, limits)
- `D4_Forecast_Call_Script.docx`: 10-minute forecast call
- `D4_holdout_forecast_LOCKED.json`: Q1 FY27 forecast with SHA-256, locked before the quarter's outcome was seen
- `code/`: d4_prep.py → d4_methods.py → d4_final.py → d4_views.py → d4_workbook.py → d4_charts.py

Back-test (8 quarters, no look-ahead): final method MAPE 15.6% (bias +4%) vs rep commit 26.6% (bias +25%).

AI use: code and drafting produced with an AI assistant (Claude); every figure is reproducible from the code.
