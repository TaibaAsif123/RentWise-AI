import streamlit as st
from theme import apply_theme

apply_theme()

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
            Specify your preferred city so the property can
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
            you are looking for, such as a flat or house.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <h2>🛋️ Lifestyle Requirements</h2>
        <p>
            Specify whether furnished accommodation or parking is required.
            If a listing does not state these details, RentWise flags them
            as something to verify.
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