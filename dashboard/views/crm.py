import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib.common import AQUA, BLUE, ORANGE, bar_h, header, image, kpis, load, source, style

D = load()
c, h = D["crm"], D["hubspot"]
header("Implementation", "CRM layer — built in HubSpot",
       "The plan's sales rules were built into a live HubSpot CRM: D4's stage exit rules became computed deal fields, and every flag was checked against D4 before it was written.")
kpis([("Companies", f"{c['companies']:,}"), ("Open deals", f"{c['deals']}", f"₹{c['pipeline_cr']} cr"), ("Flagged deals", f"{c['flagged']}", f"₹{c['flagged_cr']} cr"),
      ("Clean deals", f"{c['clean']}", f"₹{c['clean_cr']} cr"), ("Discount above 14%", f"{c['discount']['above_guardrail']} of {c['discount']['filled']}")])

st.subheader("Pipeline by stage and hygiene status")
fig = go.Figure()
fig.add_trace(go.Bar(x=h["stages"], y=h["clean_v"], name="Clean", marker_color=AQUA, customdata=h["clean_n"], hovertemplate="%{x}<br>Clean: %{customdata} deals, ₹%{y:.1f} cr<extra></extra>"))
fig.add_trace(go.Bar(x=h["stages"], y=h["flag_v"], name="Flagged", marker_color=ORANGE, customdata=h["flag_n"], hovertemplate="%{x}<br>Flagged: %{customdata} deals, ₹%{y:.1f} cr<extra></extra>"))
fig.update_layout(barmode="stack", bargap=0.35)
st.plotly_chart(style(fig, 360, "Open pipeline (₹ cr)"), width="stretch")
st.write("Flags sit where the money is: 97 of the 119 deals at stage 3 or later are flagged.")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Five computed hygiene flags")
    f = c["flags"]
    st.plotly_chart(bar_h([x[0] for x in f], [x[2] for x in f], color=ORANGE, text=[f"{x[1]} deals · ₹{x[2]} cr" for x in f], xtitle="₹ cr carrying the flag"), width="stretch")
    st.caption("All five matched D4's published counts exactly. D4's sixth flag (ageing limit) was left out: the source never captured stage-entry dates.")
with c2:
    st.subheader("Discount % against the 14% guardrail")
    fig = go.Figure(go.Bar(x=h["stages"], y=h["disc_avg"], marker_color=BLUE, marker_cornerradius=4, text=[f"{a:.1f}% (n={n})" for a, n in zip(h["disc_avg"], h["disc_n"])], textposition="outside"))
    fig.add_hline(y=c["discount"]["guardrail"], line_dash="dash", annotation_text="Guardrail 14%")
    st.plotly_chart(style(fig, 300, "Average discount (%)"), width="stretch")
    st.caption("128 quoted deals filled from the source CRM export. CAC, CAC payback and Gross margin % fields exist but stay blank until deals close; the data room holds them only at company level.")

st.subheader("Screens from HubSpot")
tabs = st.tabs(["Deal board", "Flagged deals (105)", "Discount above 14% (121)", "Deal record", "Pipeline stages", "Companies (1,995)"])
for t, (f, cap) in zip(tabs, [("1_pipeline_board.png", "Board view of the 'Strata new logo' pipeline"), ("2_flagged_deals.png", "Deals filtered on Pipeline hygiene status = Flagged"),
                              ("3_discount.png", "Deals filtered on Discount % above the 14% guardrail"), ("4_deal_record.png", "A flagged deal: close date passed, no contacts, 24.1% discount"),
                              ("5_pipeline_stages.png", "Pipeline settings: five stages with D4's exit rules as stage descriptions"), ("8_companies.png", "Companies list, 1,995 records")]):
    with t:
        image(f, cap)
st.caption("Screenshots captured in the HubSpot portal on 13 Oct 2026.")

st.subheader("How it was built")
image("hs5_build.png")
steps = [["1 Source", "D1 clean accounts and D4 open-pipeline snapshot", "Row counts match"], ["2 Companies", "Imported; 270 duplicates removed; 21 missing added", "1,995; no orphan deals"],
         ["3 Pipeline", "Five stages named exactly as D4", "Names match"], ["4 Deals", "279 deals, each associated to its company", "279 of 279"], ["5 Properties", "8 hygiene + 4 guardrail fields on Deal", "Types checked"],
         ["6 Compute", "Flags against the 1 Apr 2026 snapshot date", "No real-calendar dates"], ["7 Validate", "Each flag vs D4's published count", "5 of 5 exact"],
         ["8 Write", "41 batched updates of 10 records", "0 failures"], ["9 Use", "Q2 clean-up list; discount watch", "Feeds the D7 Q2 review"]]
st.dataframe(pd.DataFrame(steps, columns=["Step", "What was done", "Check"]), hide_index=True, width="stretch")
with st.expander("Framework: automated CRM pipeline flow"):
    image("fw8_crmflow.png")
with st.expander("Example deal record"):
    image("hs4_record.png")
source("HubSpot portal (free CRM), data pulled via the HubSpot API on 11 Oct 2026.")
