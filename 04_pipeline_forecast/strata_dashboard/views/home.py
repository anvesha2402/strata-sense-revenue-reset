import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib.common import SCEN_COLORS, header, kpis, load, source, style

d = load()
s = d["start"]

header("MBA capstone · B2B SaaS revenue turnaround", "The Strata Sense Revenue Reset",
       "An industrial predictive-maintenance company (sensors plus analytics software, ₹310 cr ARR) was growing more slowly every year. "
       "This project diagnoses why, plans the three-year fix, defends it to a board, and builds its sales rules into a live HubSpot CRM.")

st.subheader("The starting position (FY26)")
kpis([("ARR", f"₹{s['arr_fy26']} cr"), ("Win rate", f"{s['win_to']}%", f"from {s['win_from']}%"), ("Net revenue retention", f"{s['nrr_to']}%", f"from {s['nrr_from']}%"),
      ("Sales cycle", f"{s['cycle_to']} months", f"from {s['cycle_from']}"), ("Average discount", f"{s['disc_to']}%", f"from {s['disc_from']}%")])

st.subheader("The plan's result")
kpis([("FY29 ARR (Base)", "₹526 cr", "board path ₹522 cr"), ("FY27 investment", "₹14.95 cr", "cap ₹15 cr"), ("EBITDA positive", "FY28"),
      ("Payback vs do-nothing", "≈ 8 months"), ("Do-nothing FY29 ARR", "₹389 cr")])

a = d["arr"]
fig = go.Figure()
for name in ["Board path", "Base", "CFO-capped", "Do nothing"]:
    fig.add_trace(go.Scatter(x=a["years"], y=a[name], name=name, mode="lines+markers",
                             line=dict(color=SCEN_COLORS[name], width=2, dash="dot" if name in ("Board path", "Do nothing") else "solid"),
                             marker=dict(size=8), hovertemplate=name + " %{x}: ₹%{y:.1f} cr<extra></extra>"))
st.plotly_chart(style(fig, 360, "Closing ARR (₹ cr)"), width="stretch")
source("D7 integrated model (runs.json, ARR_bridge sheet).")

st.subheader("The eight deliverables")
rows = [["D1", "Diagnostic and hypothesis test", "₹55 cr/yr of root causes ranked; 1 of 6 hypotheses rejected"],
        ["D2", "Account planning", "400 / 1,100 / 1,600 account tiers; capacity fits the need, thinly"],
        ["D3", "Discovery to proposal", "Live buyer role-play; 13 of 14 hidden facts found; 7.1-month payback"],
        ["D4", "Pipeline and forecast", "Hold-out forecast error 23.3%, locked before the outcome"],
        ["D5", "Competitive battlecards", "Helix is a packaging problem, not a positioning one"],
        ["D6", "Channel partners", "Break-even ₹0.24 cr sourced ARR per partner"],
        ["D7", "Integrated three-year plan", "₹526 cr FY29 ARR; ~1,400 formulas; 1 disclosed guardrail breach"],
        ["D8", "Board ask", "₹14.95 cr, 6 AEs, gated on Q2 FY27 triggers"],
        ["CRM", "HubSpot build", "1,995 companies, 279 deals, 5 validated hygiene flags"]]
st.dataframe(pd.DataFrame(rows, columns=["#", "Deliverable", "Headline"]), hide_index=True, width="stretch")
st.caption("Use the sidebar to open each deliverable, the frameworks page, or the CRM layer.")
