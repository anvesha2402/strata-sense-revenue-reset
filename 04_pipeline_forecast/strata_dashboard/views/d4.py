import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib.common import BLUE, NAVY, ORANGE, AQUA, bar_h, header, image, kpis, load, source, style

d = load()["d4"]
header("Deliverable 4", "Pipeline and forecasting",
       "Compared five forecasting methods in a no-look-ahead back-test, locked a forecast for an unseen quarter, and wrote stage exit rules and pipeline hygiene checks.")
h = d["holdout"]
kpis([("Back-test error, final method", "15.6%", "rep commit 26.6%"), ("Hold-out forecast", f"₹{h['forecast']} cr"), ("Hold-out actual", f"₹{h['actual']} cr"), ("Hold-out error", f"{h['error']}%", f"team commit {h['team_commit_error']}%")])

st.subheader("Forecast methods compared (8-quarter back-test)")
m = d["methods"]
st.plotly_chart(bar_h([x[0] for x in m], [x[1] for x in m], color=[ORANGE] + [BLUE] * 4 + [NAVY], text=[f"{x[1]}% error · bias +{x[2]}%" for x in m], xtitle="Mean absolute % error", height=320), width="stretch")
st.write("Every uncalibrated method over-forecasts because conversion kept falling. Calibrating on the last four quarters removed most of the bias.")

c = d["coverage"]
c1, c2 = st.columns(2)
with c1:
    st.subheader("Coverage")
    fig = go.Figure(go.Bar(x=["Reported", "Required"], y=[c["reported"], c["required"]], marker_color=[ORANGE, NAVY], marker_cornerradius=4, text=[f"{c['reported']}x", f"{c['required']}x"], textposition="outside"))
    st.plotly_chart(style(fig, 280, "Pipeline ÷ quota"), width="stretch")
with c2:
    st.subheader("In-quarter pipeline")
    fig = go.Figure(go.Pie(labels=["No hygiene flag", "Carries a flag"], values=[c["clean_cr"], c["inq_cr"] - c["clean_cr"]], hole=0.6, marker_colors=[AQUA, ORANGE], sort=False))
    fig.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), annotations=[dict(text=f"₹{c['inq_cr']} cr", showarrow=False, font_size=16)])
    st.plotly_chart(fig, width="stretch")
    st.caption(f"Only ₹{c['clean_cr']} cr of ₹{c['inq_cr']} cr had no flag.")

st.subheader("Stage exit rules")
st.dataframe(pd.DataFrame(d["stages"], columns=["Stage", "Ageing limit (days)", "Exit criteria"]), hide_index=True, width="stretch")
st.caption("These rules became the computed hygiene flags in the HubSpot CRM (see the CRM page).")
with st.expander("Back-test chart"):
    image("backtest.png")
source("D4 forecast dashboard, method note, locked hold-out forecast.")
