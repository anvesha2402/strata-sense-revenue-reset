import streamlit as st

st.set_page_config(page_title="Strata Sense Revenue Reset", page_icon="📈", layout="wide")

pages = {
    "Project": [
        st.Page("views/home.py", title="Overview", icon=":material/home:", default=True),
    ],
    "Deliverables": [
        st.Page("views/d1.py", title="D1 Diagnostic", icon=":material/troubleshoot:"),
        st.Page("views/d2.py", title="D2 Account planning", icon=":material/account_tree:"),
        st.Page("views/d3.py", title="D3 Discovery to proposal", icon=":material/handshake:"),
        st.Page("views/d4.py", title="D4 Pipeline and forecast", icon=":material/query_stats:"),
        st.Page("views/d5.py", title="D5 Battlecards", icon=":material/swords:"),
        st.Page("views/d6.py", title="D6 Channel partners", icon=":material/hub:"),
        st.Page("views/d7.py", title="D7 Three-year plan", icon=":material/trending_up:"),
        st.Page("views/d8.py", title="D8 Board ask", icon=":material/gavel:"),
    ],
    "Tools": [
        st.Page("views/frameworks.py", title="Frameworks", icon=":material/schema:"),
        st.Page("views/crm.py", title="CRM layer (HubSpot)", icon=":material/database:"),
    ],
}
st.navigation(pages).run()

st.sidebar.caption("Strata Sense Technologies is a fictional company. All data are synthetic, built for an MBA practice capstone.")
st.sidebar.caption("Built by Anvesha · MBA Year 2 (PGDM), WeSchool")
