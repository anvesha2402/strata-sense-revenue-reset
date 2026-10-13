import numpy as np
import plotly.graph_objects as go
import streamlit as st

from lib.common import AQUA, BLUE, GREY, NAVY, ORANGE, header, image, load, style

D = load()
header("Frameworks", "The sales and marketing frameworks behind the project",
       "Each framework is applied to a finding from a deliverable. Three of them are interactive: change the inputs and see the result.")

tabs = st.tabs(["Sales velocity", "Ramp and hiring", "Stage-gate", "Ishikawa (D1)", "Account pyramid (D2)", "Buygrid (D3)", "JTBD (D3)", "Kotler (D5)", "CRM flow"])

# --- Sales velocity -----------------------------------------------------------
with tabs[0]:
    v = D["d7"]["velocity"]
    st.subheader("Sales velocity = qualified opps × win rate × net deal size ÷ cycle length")
    st.write("Start from FY26 actuals (defaults) and move the levers. The FY29 Base plan values are shown under each slider.")
    c1, c2, c3, c4, c5 = st.columns(5)
    opps = c1.slider("Qualified opps / year", 300, 600, v["fy26"]["opps"], 10, help=f"FY29 plan: {v['fy29']['opps']}")
    win = c2.slider("Win rate %", 10.0, 30.0, v["fy26"]["win"], 0.1, help=f"FY29 plan: {v['fy29']['win']}%")
    lst = c3.slider("List deal size (₹ lakh)", 50.0, 100.0, v["fy26"]["list"], 0.5, help=f"FY29 plan: {v['fy29']['list']}")
    disc = c4.slider("Discount %", 5.0, 30.0, v["fy26"]["disc"], 0.1, help=f"FY29 plan: {v['fy29']['disc']}%")
    cyc = c5.slider("Cycle (months)", 5.0, 10.0, v["fy26"]["cycle"], 0.1, help=f"FY29 plan: {v['fy29']['cycle']}")
    vel = lambda o, w, l, dsc, c: o * (w / 100) * l * (1 - dsc / 100) / c / 100
    base = vel(*[v["fy26"][k] for k in ("opps", "win", "list", "disc", "cycle")])
    plan = vel(*[v["fy29"][k] for k in ("opps", "win", "list", "disc", "cycle")])
    now = vel(opps, win, lst, disc, cyc)
    m1, m2, m3 = st.columns(3)
    m1.metric("FY26 velocity", f"₹{base:.2f} cr / month")
    m2.metric("Your velocity", f"₹{now:.2f} cr / month", f"{(now / base - 1) * 100:+.0f}% vs FY26", delta_color="normal" if abs(now - base) > 1e-9 else "off")
    m3.metric("FY29 Base plan", f"₹{plan:.2f} cr / month")
    fig = go.Figure(go.Bar(x=["FY26", "Your inputs", "FY29 plan"], y=[base, now, plan], marker_color=[GREY, BLUE, NAVY], marker_cornerradius=4,
                           text=[f"₹{x:.2f} cr" for x in (base, now, plan)], textposition="outside"))
    st.plotly_chart(style(fig, 300, "₹ cr bookings per month"), width="stretch")
    st.caption("Inputs from the D7 assumptions sheet (direct new-logo business). A 1-point win-rate gain is worth more than a 1-point discount cut or a shorter cycle.")

# --- Ramp ---------------------------------------------------------------------
with tabs[1]:
    st.subheader("How much do new AEs add in FY27?")
    st.write("Measured productivity by tenure: ₹0 (0–6 months), ₹0.29 cr (6–12), ₹0.59 cr (12–24), ₹0.89 cr (24+) a year. Choose when and how many AEs to hire.")
    band = lambda t: 0.0 if t < 6 else 0.29 if t < 12 else 0.59 if t < 24 else 0.89
    c1, c2 = st.columns(2)
    plan_q = {}
    with c1:
        for q in ["Q1", "Q2", "Q3", "Q4"]:
            plan_q[q] = st.number_input(f"AEs hired at start of {q} FY27", 0, 12, 6 if q == "Q3" else 0, key=f"h{q}")
    fy27 = 0.0
    for i, (q, n) in enumerate(plan_q.items()):
        months = 12 - 3 * i
        fy27 += n * sum(band(t) / 12 for t in range(months))
    assumed = 0.0
    for i, (q, n) in enumerate(plan_q.items()):
        months = 12 - 3 * i
        assumed += n * sum((0.89 * min(t / 6, 1)) / 12 for t in range(months))
    with c2:
        st.metric("FY27 bookings from these hires (measured ramp)", f"₹{fy27:.2f} cr")
        st.metric("Same hires under the 6-month assumption", f"₹{assumed:.2f} cr", f"₹{assumed - fy27:.2f} cr never arrives", delta_color="off")
        st.caption("Simplified: no attrition, straight-line within each tenure band. D2's full model (with attrition) gives ₹1.1 cr for 12 AEs in H1.")
    mx = np.arange(0, 37)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mx, y=[band(t) for t in mx], name="Measured ramp", line=dict(color=BLUE, width=2.5, shape="hv")))
    fig.add_trace(go.Scatter(x=mx, y=[0.89 * min(t / 6, 1) for t in mx], name="6-month assumption", line=dict(color=ORANGE, width=2, dash="dash")))
    st.plotly_chart(style(fig, 300, "₹ cr per AE per year", "Months in role"), width="stretch")

# --- Stage gate ---------------------------------------------------------------
with tabs[2]:
    st.subheader("Q2 FY27 gate: continue, adjust or stop?")
    st.write("Enter Q2 results. Each measure is checked against the threshold in D7 §12.")
    c1, c2, c3 = st.columns(3)
    vals = {
        "Qualified win rate ≥ 18.0%": c1.number_input("Qualified win rate (%)", 0.0, 40.0, 18.5, 0.1) >= 18.0,
        "New qualified direct deals ≥ 95 / quarter": c2.number_input("New qualified direct deals", 0, 200, 98) >= 95,
        "Churn + contraction H1 ≤ ₹13.5 cr": c3.number_input("Churn + contraction H1 (₹ cr)", 0.0, 40.0, 12.8, 0.1) <= 13.5,
        "Expansion ARR H1 ≥ ₹12.5 cr": c1.number_input("Expansion ARR H1 (₹ cr)", 0.0, 40.0, 12.9, 0.1) >= 12.5,
        "Quarterly CAC payback ≤ 30 months": c2.number_input("Quarterly CAC payback (months)", 0.0, 60.0, 29.4, 0.1) <= 30,
        "Forecast error ≤ 15%": c3.number_input("Forecast error (%)", 0.0, 60.0, 14.0, 0.1) <= 15,
        "Vajra not shortlisted on price": c1.checkbox("Vajra still in play (not lost on price)", True),
    }
    passed = sum(vals.values())
    for k, ok in vals.items():
        st.write(("✅ " if ok else "❌ ") + k)
    if passed == 7:
        st.success("CONTINUE — release the ₹1.92 cr reserve and hire 6 AEs from Q3 (Base plan, ₹526 cr FY29).")
    elif passed >= 5 and vals["Quarterly CAC payback ≤ 30 months"]:
        st.warning(f"ADJUST — {7 - passed} measure(s) missed. Hold the reserve, apply the 'if missed' action for each, and review again at Q3.")
    else:
        st.error("STOP — move to the CFO-capped path: ₹13.03 cr only, FY28–29 hiring frozen (₹492 cr FY29).")
    st.caption("Decision rule here is a simple illustration of D8's continue / adjust / stop gate: all seven met = continue; a payback miss or three or more misses = stop.")
    image("fw7_stagegate.png")

with tabs[3]:
    image("fw1_ishikawa.png")
    st.write("Six branches; the four orange causes are sized in ₹ ARR at stake (₹55 cr a year in total). The largest sits on the product branch, so it goes to pricing and product, not sales training.")
with tabs[4]:
    image("fw2_pyramid.png")
    st.write("400 strategic accounts produced 51% of won ARR on 8.5% of AE touches; 1,600 low-touch accounts took 62.5% of touches for 12%.")
with tabs[5]:
    image("fw3a_buygrid.png")
with tabs[6]:
    image("fw3b_jtbd.png")
with tabs[7]:
    image("fw5_kotler.png")
with tabs[8]:
    image("fw8_crmflow.png")
