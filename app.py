
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RentWise AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# PAGE NAVIGATION
# ============================================================

home = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠",
    default=True
)

how_it_works = st.Page(
    "pages/how_it_works.py",
    title="How It Works",
    icon="💡"
)

investigate = st.Page(
    "pages/investigate.py",
    title="Investigate",
    icon="🔎"
)

risk_analysis = st.Page(
    "pages/risk_analysis.py",
    title="Risk Analysis",
    icon="🛡️"
)

requirements = st.Page(
    "pages/requirements.py",
    title="Requirements",
    icon="📋"
)

# ============================================================
# TOP NAVBAR
# ============================================================

pg = st.navigation(
    [
        home,
        how_it_works,
        investigate,
        risk_analysis,
        requirements
    ],
    position="top"
)

# ============================================================
# RUN SELECTED PAGE
# ============================================================

pg.run()
