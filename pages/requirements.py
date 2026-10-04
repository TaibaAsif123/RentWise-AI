
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
    <h1>📋 Rental Requirements</h1>
    <p>Define what you need before investigating a property.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h2>🎯 Why Requirements Matter</h2>
    <p>
        A rental property may look attractive but still fail to meet
        important requirements. RentWise compares the property against
        the tenant's preferences before producing its investigation results.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h2>💰 Budget</h2>
        <p>
            Set the maximum monthly rent you are willing to pay.
            RentWise compares this amount with the property's asking rent.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h2>📍 Location</h2>
        <p>
            Specify your preferred city or area so the property can
            be checked against your location requirement.
        </p>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="card">
        <h2>🛏️ Space & Property Type</h2>
        <p>
            Define minimum bedrooms, bathrooms, and the type of property
            you are looking for, such as an apartment or house.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <h2>🛋️ Lifestyle Requirements</h2>
        <p>
            Specify preferences such as furnished accommodation,
            parking availability, and whether pets are required or allowed.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

st.markdown("""
<div class="card">
    <h2>🔎 How RentWise Uses Them</h2>
    <p>
        During an investigation, the requirements are compared with
        the property's details. The result indicates which requirements
        match and which ones do not.
    </p>
</div>
""", unsafe_allow_html=True)

if st.button("🔎 Set Requirements & Investigate", use_container_width=True):
    st.switch_page("pages/investigate.py")
