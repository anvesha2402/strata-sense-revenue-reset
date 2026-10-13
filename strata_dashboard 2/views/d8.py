import streamlit as st

from lib.common import header, image, kpis, load, source

d = load()["d8"]
header("Deliverable 8", "Board presentation and CEO memo",
       "The plan condensed into a 10-slide board deck, a one-page CEO memo and prepared answers to five executive challenges.")
kpis([("The ask", f"₹{d['ask_cr']} cr"), ("Committed now", f"₹{d['committed_cr']} cr"), ("Gated reserve", f"₹{d['reserve_cr']} cr"), ("New hires", f"{d['aes']} AEs + {d['channel_roles']} channel roles")])
st.info(f"Doing nothing is not flat: it ends ₹{d['do_nothing_gap_cr']} cr lower by FY29 (₹389 cr vs ₹526 cr).")
c1, c2 = st.columns(2)
with c1:
    st.subheader("What the company stops doing")
    st.markdown("\n".join(f"- {x}" for x in d["stops"]))
with c2:
    st.subheader("Executive challenges prepared")
    st.markdown("- **CFO:** no headroom and a payback breach — why not the CFO-capped plan?\n- **CMO:** how is pipeline attributed to the ₹24 cr programme reallocation?\n- **CPO:** why not launch the sensor-agnostic tier now?\n- **CRO:** can win rate rise from 17% to 22.5% while discounts fall?\n- **CEO:** why believe the plan over doing nothing?")
st.subheader("Framework: stage-gate capital allocation")
image("fw7_stagegate.png")
st.caption("Try the gate decision yourself on the Frameworks page.")
source("D8 board deck, CEO memo, Q&A sheet; D7 scenarios.")
