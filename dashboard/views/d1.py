import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib.common import BLUE, NAVY, ORANGE, bar_h, header, image, kpis, load, source, style

d = load()["d1"]
header("Deliverable 1", "Diagnostic and hypothesis test",
       "Cleaned the CRM, rebuilt ARR and retention, and tested six hypotheses about why growth stalled. Each root cause is sized in rupees of ARR at stake.")
kpis([("CRM rows after cleaning", "1,794", "from 1,840"), ("Root causes sized", "₹55 cr/yr"), ("NRR, all customers", f"{d['nrr']['all_to']}%", f"from {d['nrr']['all_from']}%"),
      ("NRR, Helix-incumbent", f"{d['nrr']['helix_to']}%", f"from {d['nrr']['helix_from']}%")])

c1, c2 = st.columns(2)
with c1:
    st.subheader("Root causes by ARR at stake")
    rc = d["root_causes"]
    st.plotly_chart(bar_h([r[0] for r in rc], [r[1] for r in rc], color=[ORANGE, BLUE, BLUE, BLUE], text=[f"₹{r[1]} cr" for r in rc], xtitle="₹ cr a year"), width="stretch")
    st.write("The largest cause is a pricing and packaging problem (a rival bundling monitoring free), which sales effort alone cannot fix.")
with c2:
    st.subheader("Why win rate fell 7 points")
    w = d["winrate_decomp"]
    fig = go.Figure(go.Waterfall(x=["Win rate FY24", "Mix (who we sold to)", "Rate (how well we sold)", "Win rate FY26"], measure=["absolute", "relative", "relative", "total"],
                                 y=[23.9, w["mix"], w["rate"], 0], decreasing=dict(marker_color=ORANGE), totals=dict(marker_color=NAVY), increasing=dict(marker_color=BLUE),
                                 text=["", f"{w['mix']} pts", f"{w['rate']} pts", ""], textposition="outside"))
    st.plotly_chart(style(fig, 300, "Win rate (%)"), width="stretch")
    st.write("Half the fall came from selling to worse-fit accounts, half from selling less well within comparable deals.")
    st.caption("Clean-data win rates; the split is from D1's mix/rate decomposition.")

st.subheader("Hypothesis verdicts")
st.dataframe(pd.DataFrame(d["hypotheses"], columns=["Hypothesis", "Verdict", "Evidence"]), hide_index=True, width="stretch")

st.subheader("AE productivity by tenure")
st.write("New salespeople take about two years, not six months, to reach full productivity.")
r = d["ramp"]
st.plotly_chart(bar_h([x[0] for x in r], [x[1] for x in r], text=[f"₹{x[1]} cr" for x in r], xtitle="₹ cr bookings per AE per year", height=240), width="stretch")

with st.expander("CRM audit: what was fixed"):
    st.dataframe(pd.DataFrame(d["audit"], columns=["Issue", "Rows", "Rule"]), hide_index=True, width="stretch")
with st.expander("Framework: root-cause (Ishikawa) diagram"):
    image("fw1_ishikawa.png")
with st.expander("Original D1 exhibits"):
    image("ex1_arr_bridge.png", "FY26 ARR bridge and retention trend")
    image("ex8_root_causes.png", "Root causes ranked by ARR at stake")
source("D1 diagnostic memo and data appendix.")
