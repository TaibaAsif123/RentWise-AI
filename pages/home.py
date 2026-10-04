
import streamlit as st

st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #111827, #1f2937);
    padding: 4rem 3rem;
    border-radius: 24px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.hero h1 {
    font-size: 3.5rem;
    margin-bottom: 0.5rem;
}

.hero p {
    font-size: 1.2rem;
    color: #d1d5db;
}

.card {
    background: white;
    padding: 1.8rem;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🏠 RentWise AI</h1>
    <p>Rent smarter. Investigate before you commit.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h2>🔎 AI-Powered Rental Investigation</h2>
    <p>
        RentWise helps tenants investigate rental properties by analyzing
        price, location, requirements, and potential risks before making
        a rental decision.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>💰 Price Analysis</h3>
        <p>Check whether the property fits your rental budget.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>📋 Requirement Matching</h3>
        <p>Compare the property with your specific requirements.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>🛡️ Risk Investigation</h3>
        <p>Identify missing information and potential rental risks.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

if st.button("🔎 Start Investigation", use_container_width=True):
    st.switch_page("pages/investigate.py")
