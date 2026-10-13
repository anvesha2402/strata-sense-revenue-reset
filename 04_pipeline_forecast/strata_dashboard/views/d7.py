import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib.common import BLUE, ORANGE, SCEN_COLORS, header, image, kpis, load, source, style

D = load()
a, sc = D["arr"], D["scenarios"]
header("Deliverable 7", "Integrated revenue model and three-year plan",
       "One workbook (~1,400 formulas, no plugs) links AE capacity, win rate, deal size, channel, retention, P&L and investment, under four scenarios.")

choice = st.segmented_control("Scenario", ["Base", "Downside", "Aggressive", "CFO-capped"], default="Base")
r = sc[choice or "Base"]
kpis([("FY29 ARR", f"₹{r['ARR FY29']:.1f} cr"), ("Growth FY29", f"{r['Growth FY29']*100:.1f}%", f"FY27: {r['Growth FY27']*100:.1f}%"), ("NRR FY29", f"{r['NRR FY29']*100:.1f}%"),
      ("EBITDA FY29", f"₹{r['EBITDA FY29']:.1f} cr"), ("FY27 investment", f"₹{D['investment'][choice or 'Base']} cr")])

fig = go.Figure()
for name in ["Board path", "Aggressive", "Base", "CFO-capped", "Downside", "Do nothing"]:
    sel = name == (choice or "Base")
    fig.add_trace(go.Scatter(x=a["years"], y=a[name], name=name, mode="lines+markers", line=dict(color=SCEN_COLORS[name], width=3 if sel else 1.5, dash="dot" if name in ("Board path", "Do nothing") else "solid"),
                             opacity=1 if sel or name in ("Board path", "Do nothing") else 0.45, marker=dict(size=8), hovertemplate=name + " %{x}: ₹%{y:.1f} cr<extra></extra>"))
st.plotly_chart(style(fig, 380, "Closing ARR (₹ cr)"), width="stretch")

c1, c2 = st.columns(2)
with c1:
    st.subheader("What moves FY29 ARR most")
    base = sc["Base"]["ARR FY29"]
    sens = D["sensitivity_arr_fy29"]
    rows = sorted(sens.items(), key=lambda kv: abs(kv[1]["high"] - kv[1]["low"]))
    fig = go.Figure()
    fig.add_trace(go.Bar(y=[k for k, _ in rows], x=[v["low"] - base for _, v in rows], orientation="h", name="Driver 1 step worse/lower", marker_color=ORANGE, hovertemplate="%{y}: %{x:+.1f} cr<extra></extra>"))
    fig.add_trace(go.Bar(y=[k for k, _ in rows], x=[v["high"] - base for _, v in rows], orientation="h", name="Driver 1 step better/higher", marker_color=BLUE, hovertemplate="%{y}: %{x:+.1f} cr<extra></extra>"))
    fig.update_layout(barmode="overlay")
    st.plotly_chart(style(fig, 320, xtitle="Change in FY29 ARR vs Base (₹ cr)"), width="stretch")
    st.caption("One-step moves per driver as defined in the D7 sensitivity sheet (e.g. win rate ±1 pt). For churn, 'higher' means more churn.")
with c2:
    st.subheader("Guardrail checks (Base)")
    st.dataframe(pd.DataFrame(D["d7"]["guardrails"], columns=["Guardrail", "Result", "Status"]), hide_index=True, width="stretch")
    st.write("The plan is more likely to break a guardrail than to destroy value: the every-quarter payback rule breaks at a 0.7-point win-rate miss, while the investment still pays back within 30 months unless win rate falls 7.9 points.")

st.subheader("Early-warning triggers for the Q2 FY27 review")
st.dataframe(pd.DataFrame(D["d7"]["triggers"], columns=["Measure", "Q2 threshold", "If missed"]), hide_index=True, width="stretch")
with st.expander("Framework: sales velocity (interactive version on the Frameworks page)"):
    image("fw4_velocity.png")
with st.expander("Original D7 charts"):
    image("bridge.png", "FY26 → FY29 ARR bridge, Base"); image("cac.png", "Quarterly CAC payback against the guardrails")
source("D7 integrated model (runs.json, Scenarios, Sensitivity, ARR_bridge sheets), plan memo.")
