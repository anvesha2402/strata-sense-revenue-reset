# Strata Sense Revenue Reset — dashboard

A Streamlit dashboard for the eight-deliverable MBA capstone: an overview, one page per deliverable (D1–D8), an interactive frameworks page, and the CRM layer built in HubSpot.

Strata Sense Technologies is a fictional company. All data are synthetic, built for an MBA practice capstone.

## Pages

| Page | What it shows |
|---|---|
| Overview | Starting position, the plan's result, ARR path vs board path and do-nothing |
| D1 Diagnostic | Root causes in ₹, win-rate mix/rate split, hypothesis verdicts, AE ramp |
| D2 Account planning | Tiers, effort vs revenue, FY27 capacity bridge |
| D3 Discovery to proposal | Role-play findings, proposal, negotiation limits, Buygrid, JTBD |
| D4 Pipeline and forecast | Back-test of 5 methods, hold-out result, coverage, stage exit rules |
| D5 Battlecards | Helix finding, battlecards at a glance, Kotler's five levels |
| D6 Channel partners | Partner decisions, programme tiers, loss probability |
| D7 Three-year plan | Scenario switch, ARR paths, sensitivity, guardrails, Q2 triggers |
| D8 Board ask | The ask, the gate, what stops, executive challenges |
| Frameworks | Interactive sales velocity, ramp/hiring and stage-gate tools, plus 6 framework diagrams |
| CRM layer (HubSpot) | Pipeline by stage and hygiene, flags, discount vs guardrail, build steps |

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

1. Upload this folder to a GitHub repository (as the repo root, or as a subfolder).
2. Go to share.streamlit.io, sign in with GitHub, and click **Create app**.
3. Pick the repository and branch. For **Main file path** enter `dashboard/streamlit_app.py` (or `streamlit_app.py` if this folder is the repo root).
4. Click **Deploy**.

## Data

- `data/strata.json` — figures from the deliverables; model figures come from the D7 integrated model (`runs.json`, ARR_bridge sheet).
- `data/hubspot_live.json` — stage and hygiene totals pulled from the HubSpot portal via the HubSpot API (11 Oct 2026).
- `assets/` — framework diagrams and deliverable charts.

AI use: built with an AI assistant (Claude); every figure traces to a deliverable output.

—
Anvesha · MBA Year 2 (PGDM), WeSchool
