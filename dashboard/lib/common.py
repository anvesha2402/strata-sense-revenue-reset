import json
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

NAVY, BLUE, ORANGE, AQUA, GREY, INK2, LINE = "#1F3A5F", "#2A78D6", "#EB6834", "#1BAF7A", "#A3A29C", "#52514E", "#D9D8D2"
SCEN_COLORS = {"Base": BLUE, "Aggressive": AQUA, "CFO-capped": NAVY, "Downside": ORANGE, "Do nothing": GREY, "Board path": INK2}


@st.cache_data
def load():
    data = json.loads((ROOT / "data" / "strata.json").read_text(encoding="utf-8"))
    data["hubspot"] = json.loads((ROOT / "data" / "hubspot_live.json").read_text(encoding="utf-8"))
    return data


def header(kicker, title, intro=None):
    st.caption(kicker.upper())
    st.title(title)
    if intro:
        st.write(intro)


def kpis(items):
    cols = st.columns(len(items))
    for c, item in zip(cols, items):
        label, value = item[0], item[1]
        delta = item[2] if len(item) > 2 else None
        c.metric(label, value)
        if delta:
            c.caption(delta)


def image(name, caption=None):
    st.image(str(ASSETS / name), caption=caption, width="stretch")


def style(fig, height=380, ytitle=None, xtitle=None):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=30, b=10), plot_bgcolor="white", paper_bgcolor="white",
                      font=dict(family="Inter, Arial, sans-serif", size=13), legend=dict(orientation="h", y=-0.18),
                      hoverlabel=dict(bgcolor="white"))
    fig.update_xaxes(showgrid=False, linecolor=LINE, title=xtitle)
    fig.update_yaxes(gridcolor="#EEEDE8", linecolor=LINE, title=ytitle, zeroline=False)
    return fig


def bar_h(labels, values, color=BLUE, text=None, xtitle=None, height=300):
    fig = go.Figure(go.Bar(x=values, y=labels, orientation="h", marker_color=color, marker_cornerradius=4,
                           text=text, textposition="outside", cliponaxis=False, hovertemplate="%{y}: %{x}<extra></extra>"))
    fig.update_yaxes(autorange="reversed")
    return style(fig, height=height, xtitle=xtitle)


def source(text):
    st.caption(f"Source: {text}")
