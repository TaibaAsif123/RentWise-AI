
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

.step {
    font-size: 1.1rem;
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>💡 How RentWise Works</h1>
    <p>Investigate a rental property before you commit.</p>
</div>
""", unsafe_allow_html=True)

steps = [
    (
        "01",
        "🏠 Enter Property Details",
        "Provide the property's rent, location, bedrooms, bathrooms, "
        "property type, furnishing, parking, pets policy, and other available information."
    ),
    (
        "02",
        "🎯 Set Your Requirements",
        "Tell RentWise your maximum budget, preferred location, "
        "minimum bedrooms and bathrooms, property type, furnishing, parking, and pet requirements."
    ),
    (
        "03",
        "🤖 AI Investigation",
        "RentWise analyzes the property against your requirements using "
        "AI-powered price, location, requirement, and risk analysis."
    ),
    (
        "04",
        "📊 Review the Results",
        "The system produces clear results showing price status, "
        "location match, requirement match, and an overall risk level."
    ),
    (
        "05",
        "🛡️ Investigate Before You Commit",
        "RentWise also identifies missing information and generates "
        "useful questions you can ask the landlord before signing anything."
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
