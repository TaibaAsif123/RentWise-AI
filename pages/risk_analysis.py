
import streamlit as st

st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #111827, #1f2937);
    padding: 3rem;
    border-radius: 24px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.hero h1 {
    font-size: 2.8rem;
}

.card {
    background: white;
    padding: 1.8rem;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    margin-bottom: 1rem;
}

.card h2 {
    color: #111827;
}

.card p {
    color: #4b5563;
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)

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
            bedrooms, bathrooms, parking, and pet preferences.
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
    "entered by the user. It does not replace legal, financial, or "
    "professional verification."
)

if st.button("🔎 Investigate a Property", use_container_width=True):
    st.switch_page("pages/investigate.py")
