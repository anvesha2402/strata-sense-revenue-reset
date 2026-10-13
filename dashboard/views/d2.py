import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib.common import AQUA, BLUE, NAVY, ORANGE, header, image, kpis, load, source, style

d = load()["d2"]
header("Deliverable 2", "Enterprise account planning and lead generation",
       "Scored all 3,100 target accounts on expected value, set three tiers, and matched sales coverage and capacity to them.")
kpis([("Strategic accounts", "400", "34% past win rate"), ("Scaled accounts", "1,100", "21%"), ("Low-touch accounts", "1,600", "12%"), ("FY27 capacity", "₹49.4 cr", "need ₹46.5 cr")])

t = pd.DataFrame(d["tiers"], columns=["Tier", "Accounts", "Win rate %", "Value per qualified opp (₹ lakh)", "Share of AE touches %", "Share of won ARR %", "Coverage"])
st.subheader("Effort went where revenue wasn't")
fig = go.Figure()
fig.add_trace(go.Bar(x=t["Tier"], y=t["Share of AE touches %"], name="Share of AE touches", marker_color=ORANGE, marker_cornerradius=4))
fig.add_trace(go.Bar(x=t["Tier"], y=t["Share of won ARR %"], name="Share of won ARR", marker_color=BLUE, marker_cornerradius=4))
fig.update_layout(barmode="group", bargap=0.35)
st.plotly_chart(style(fig, 330, "% of total"), width="stretch")
st.caption("Strategic and low-touch shares are from D2; the scaled tier is the remainder.")
st.dataframe(t, hide_index=True, width="stretch")

st.subheader("FY27 capacity bridge")
cb = d["capacity_bridge"]
fig = go.Figure(go.Waterfall(x=[c[0] for c in cb] + ["Total capacity"], measure=["absolute"] + ["relative"] * (len(cb) - 1) + ["total"],
                             y=[c[1] for c in cb] + [0], text=[f"₹{c[1]} cr" for c in cb] + ["₹49.4 cr"], textposition="outside",
                             increasing=dict(marker_color=AQUA), totals=dict(marker_color=NAVY), connector=dict(line=dict(color="#ccc"))))
fig.add_hline(y=d["need"], line_dash="dash", line_color=ORANGE, annotation_text=f"Need ₹{d['need']} cr")
st.plotly_chart(style(fig, 330, "₹ cr new ARR"), width="stretch")
st.write("Capacity fits the need only if multi-threading improves and SEA partners deliver. Hiring 12 AEs in H1 would add only ₹1.1 cr of FY27 ARR because of the two-year ramp.")

st.subheader("Account plans written")
st.write(" · ".join(d["plans"]))
with st.expander("Frameworks: account pyramid and ramp S-curve"):
    image("fw2_pyramid.png"); image("fw6_scurve.png")
source("D2 tiering and coverage workbook, account planning deck.")
