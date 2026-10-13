import pandas as pd
import streamlit as st

from lib.common import header, image, kpis, load, source

d = load()["d5"]
header("Deliverable 5", "Competitive battlecards",
       "Coded wins and losses by rival from 24 buyer interviews, then wrote battlecards for each rival and for 'no decision'.")
kpis([("Proposals won vs Helix (strong selling)", f"{d['helix_proposals_won']} of {d['helix_proposals']}"), ("Win-rate lift from battlecards", f"+{d['battlecard_lift']} pts"),
      ("Field rating", f"{d['field_rating']} / 5"), ("Helix-exposed renewals", f"₹{d['helix_exposed_renewals_cr']} cr")])
st.info("Helix is a packaging and pricing problem, not a positioning one: strong selling still won 0 of 9 proposals against it, and won and lost deals carried the same discount. What wins is scope.")
st.subheader("Battlecards at a glance")
st.dataframe(pd.DataFrame(d["cards"], columns=["Rival", "Who they are", "How to compete"]), hide_index=True, width="stretch")
st.subheader("Inject 2: Helix makes its product free until March 2027")
st.write("Do not match free. Allow a 3-month deferred start only on a 3-year term, hold the Helix-incumbent win rate at 7%, and assign executive sponsors to ₹108.6 cr of Helix-exposed renewals. Updated within 48 hours as battlecards v1.1.")
with st.expander("Framework: Kotler's five product levels"):
    image("fw5_kotler.png")
source("D5 battlecards v1.1, win/loss analysis, field validation log.")
