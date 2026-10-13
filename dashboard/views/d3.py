import streamlit as st

from lib.common import header, image, kpis, load, source

d = load()["d3"]
header("Deliverable 3", "Discovery to proposal: Ranganath Precision Components",
       "A live buyer role-play with a nine-plant auto-parts supplier already piloting a rival product, followed by a value model, a proposal and a negotiation plan.")
kpis([("Hidden facts uncovered", f"{d['facts_found']} of {d['facts_total']}"), ("Proposal", f"₹{d['price_cr']} cr a year", f"{d['assets']} assets"),
      ("Conservative payback", f"{d['payback_months']} months"), ("Press downtime cost", f"₹{d['press_cost_lakh_hr']} lakh / hour")])
c1, c2 = st.columns(2)
with c1:
    st.subheader("What discovery found")
    st.markdown(f"""
- The rival's pilot covered only ~300 CNC spindles; the costliest failures (presses) were not monitored.
- Security review, not price, was the critical path.
- An offer under ₹{d['cfo_limit_cr']} cr a year could be signed by the CFO alone.
- Missed: what the plant head is personally measured on (1 of 14 facts).
""")
with c2:
    st.subheader("Negotiation limits")
    st.markdown(f"""
- Discount cap: **{d['discount_cap']}%**
- Price floor: **₹{d['floor_per_asset']:,} per asset**
- Offer: complement the rival, don't replace it
- Payback shown at half the claimed savings, because finance halves vendor claims
""")
st.subheader("Inject 1: the CFO cuts the envelope to ₹15 cr")
i = d["inject1"]
st.write(f"Accepted the ₹{i['envelope']} cr cap; hire {i['aes']} AEs from Q3 instead of 12 in H1; protect retention; keep a ₹{i['reserve']} cr gated reserve; blended payback {i['payback']} months.")
t1, t2 = st.tabs(["Framework: Buygrid", "Framework: JTBD and four forces"])
with t1: image("fw3a_buygrid.png")
with t2: image("fw3b_jtbd.png")
source("D3 discovery plan, debrief, value model, proposal, negotiation plan; Inject 1 memo.")
