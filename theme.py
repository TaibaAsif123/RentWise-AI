import streamlit as st

_CSS = """
<style>
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1400px; }

/* Hero banner: dark with light text, readable in both themes */
.hero {
    background: linear-gradient(135deg, #111827, #1f2937);
    border: 1px solid rgba(255,255,255,.12);
    padding: 3rem;
    border-radius: 24px;
    margin-bottom: 2rem;
    text-align: center;
}
.hero h1 { font-size: 2.8rem; margin-bottom: .5rem; }
.hero-title { font-size: 2.8rem; font-weight: 800; margin-bottom: .4rem; }
.hero h1, .hero-title { color: #ffffff !important; }
.hero p, .hero-subtitle { color: #d1d5db !important; font-size: 1.1rem; }

/* Cards: translucent background + inherited text colour = works in light and dark */
.card, .metric-card, .question-box {
    background: rgba(128, 128, 128, .10);
    border: 1px solid rgba(128, 128, 128, .30);
    color: inherit;
}
.card { padding: 1.8rem; border-radius: 18px; margin-bottom: 1rem; }
.card h2, .card h3, .card p { color: inherit !important; }
.card p { opacity: .85; line-height: 1.7; }
.step { font-size: 1.1rem; line-height: 1.7; }

.metric-card { padding: 1.3rem; border-radius: 18px; text-align: center; }
.metric-icon { font-size: 1.7rem; }
.metric-label { opacity: .7; font-size: .9rem; margin-top: .3rem; }
.metric-value { font-size: 1.25rem; font-weight: 750; margin-top: .3rem; }

.question-box { padding: 1rem 1.2rem; border-radius: 14px; margin-bottom: .7rem; }

.section-title { font-size: 1.6rem; font-weight: 750; margin: 1rem 0; }

.stButton > button { width: 100%; border-radius: 12px; height: 3rem; font-weight: 700; }
</style>
"""


def apply_theme():
    st.markdown(_CSS, unsafe_allow_html=True)