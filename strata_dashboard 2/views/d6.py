import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib.common import BLUE, ORANGE, header, kpis, load, source, style

d = load()["d6"]
header("Deliverable 6", "Channel partner expansion",
       "Decided keep, fix or exit for 14 signed partners, designed a partner programme, and modelled when the channel makes or loses money.")
kpis([("Break-even per active partner", f"₹{d['breakeven_cr']} cr", "sourced ARR / year"), ("FY26 active partners averaged", f"₹{d['fy26_active_avg']} cr"),
      ("Spread across all 14 signed", f"₹{d['fy26_all_avg']} cr"), ("Chance of hitting 25% share", f"{d['share_goal_prob']}%")])
c1, c2 = st.columns(2)
with c1:
    st.subheader("Partner decisions")
    st.dataframe(pd.DataFrame(d["decisions"], columns=["Decision", "Partners", "Why"]), hide_index=True, width="stretch")
    st.subheader("Programme tiers")
    st.dataframe(pd.DataFrame(d["tiers"], columns=["Tier", "Margin", "Renewals / services"]), hide_index=True, width="stretch")
with c2:
    st.subheader("Probability the channel loses money")
    lp = d["loss_prob"]
    fig = go.Figure(go.Bar(x=[x[0] for x in lp], y=[x[1] for x in lp], marker_color=[ORANGE, BLUE, BLUE], marker_cornerradius=4, text=[f"{x[1]}%" for x in lp], textposition="outside"))
    st.plotly_chart(style(fig, 300, "% of 20,000 simulation runs"), width="stretch")
    st.caption("FY27 loss is by design (set-up year). Monte Carlo with the selected partners.")
st.write("The risk is dormant partners, not the channel itself. Inject 3 (two partners join Helix programmes): restrict them from Helix accounts, require disclosure, and bring South-East Asia recruits forward.")
source("D6 channel strategy deck, partner economics workbook, 90-day launch plan.")
