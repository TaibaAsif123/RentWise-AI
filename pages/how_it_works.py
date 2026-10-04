import streamlit as st
from theme import apply_theme

apply_theme()

st.markdown("""
<div class="hero">
    <h1>💡 How RentWise Works</h1>
    <p>Investigate a rental property before you commit.</p>
</div>
""", unsafe_allow_html=True)

steps = [
    (
        "01",
        "🎯 Set Your Requirements",
        "Choose your city, maximum monthly budget, minimum bedrooms and "
        "bathrooms, and the property type you want."
    ),
    (
        "02",
        "🏘️ Browse Matching Properties",
        "RentWise searches its rental dataset of Islamabad and Rawalpindi "
        "listings and shows the properties that fit your requirements."
    ),
    (
        "03",
        "🤖 Investigate a Property",
        "Pick a property and RentWise analyzes it against your requirements "
        "using AI-powered price, location, requirement, and risk analysis."
    ),
    (
        "04",
        "📊 Review the Results",
        "You get a RentWise score, price status, location match, requirement "
        "match, a risk level, and a verdict."
    ),
    (
        "05",
        "🛡️ Ask Before You Commit",
        "RentWise highlights missing information and generates questions "
        "to ask the landlord before signing anything. You can also compare "
        "several investigated properties side by side."
    ),
]

for number, title, description in steps:

    st.markdown(
        f"""
        <div class="card">
            <h2>{number} — {title}</h2>
            <p class="step">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

if st.button("🔎 Try RentWise", use_container_width=True):
    st.switch_page("pages/investigate.py")