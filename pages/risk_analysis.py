import streamlit as st
from theme import apply_theme

apply_theme()

st.markdown("""
<div class="hero">
    <h1>🛡️ Rental Risk Analysis</h1>
    <p>Understand what RentWise looks for before you commit.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h2>🔍 What Does RentWise Check?</h2>
    <p>
        RentWise examines the information provided about a rental property
        and identifies factors that may require further investigation.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h2>💰 Financial Risk</h2>
        <p>
            Checks whether the asking rent fits within the tenant's stated
            rental budget and highlights significant price mismatches.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h2>📋 Information Gaps</h2>
        <p>
            Identifies important details that may be missing from the
            property information, such as deposits, maintenance costs,
            utilities, or verification details.
        </p>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="card">
        <h2>🏠 Suitability Risk</h2>
        <p>
            Compares the property characteristics with the tenant's
            requirements, including property type, furnishing,
            bedrooms, bathrooms, and parking.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <h2>⚠️ Verification Concerns</h2>
        <p>
            RentWise can highlight areas where additional verification
            or questions may be appropriate before making a commitment.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

st.info(
    "RentWise provides an investigation aid based on the information "
    "available about a listing. It does not replace legal, financial, or "
    "professional verification, and it does not claim that any property "
    "or landlord is fraudulent."
)

if st.button("🔎 Investigate a Property", use_container_width=True):
    st.switch_page("pages/investigate.py")