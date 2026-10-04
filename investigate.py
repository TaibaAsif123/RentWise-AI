
import streamlit as st
from rentwise_backend import run_investigation

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
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #f7f8fc;
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Header */
    .hero {
        background: linear-gradient(135deg, #111827, #1f2937);
        padding: 2.5rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #d1d5db;
    }

    /* Section titles */
    .section-title {
        font-size: 1.6rem;
        font-weight: 750;
        margin-top: 1rem;
        margin-bottom: 1rem;
        color: #111827;
    }

    /* Cards */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 5px 18px rgba(0,0,0,0.05);
        height: 100%;
    }

    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #374151;
        margin-bottom: 0.8rem;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.3rem;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 5px 18px rgba(0,0,0,0.04);
    }

    .metric-icon {
        font-size: 1.7rem;
    }

    .metric-label {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }

    .metric-value {
        font-size: 1.25rem;
        font-weight: 750;
        margin-top: 0.3rem;
        color: #111827;
    }

    /* Risk box */
    .risk-box {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 18px;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    /* Question box */
    .question-box {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3rem;
        font-weight: 700;
        font-size: 1rem;
    }

    /* Divider */
    hr {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">🏠 RentWise AI</div>
    <div class="hero-subtitle">
        Rent smarter. Investigate before you commit.
    </div>
    <div style="margin-top:1rem; color:#9ca3af;">
        AI-powered rental property investigation for smarter decisions.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# PROPERTY + REQUIREMENTS INPUT
# ============================================================

st.markdown(
    '<div class="section-title">🔎 Property Investigation</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

# ------------------------------------------------------------
# PROPERTY DETAILS
# ------------------------------------------------------------

with left:

    st.markdown("""
    <div class="info-card">
        <div class="card-title">🏠 Property Details</div>
    </div>
    """, unsafe_allow_html=True)

    title = st.text_input(
        "Property Title",
        "Modern 2 Bedroom Apartment"
    )

    monthly_rent = st.number_input(
        "Monthly Rent",
        min_value=0,
        value=65000,
        step=1000
    )

    location = st.text_input(
        "Location",
        "F-11, Islamabad"
    )

    bedrooms = st.number_input(
        "Bedrooms",
        min_value=0,
        value=2
    )

    bathrooms = st.number_input(
        "Bathrooms",
        min_value=0,
        value=2
    )

    property_type = st.selectbox(
        "Property Type",
        ["Apartment", "House", "Studio", "Room"]
    )

    furnished = st.checkbox(
        "Furnished",
        value=True
    )

    parking = st.checkbox(
        "Parking Available",
        value=True
    )

    pets_allowed = st.checkbox(
        "Pets Allowed",
        value=True
    )

    description = st.text_area(
        "Property Description",
        "Furnished apartment in F-11 with parking."
    )


# ------------------------------------------------------------
# USER REQUIREMENTS
# ------------------------------------------------------------

with right:

    st.markdown("""
    <div class="info-card">
        <div class="card-title">🎯 Your Rental Requirements</div>
    </div>
    """, unsafe_allow_html=True)

    max_budget = st.number_input(
        "Maximum Monthly Budget",
        min_value=0,
        value=70000,
        step=1000
    )

    preferred_location = st.text_input(
        "Preferred Location",
        "Islamabad"
    )

    min_bedrooms = st.number_input(
        "Minimum Bedrooms",
        min_value=0,
        value=2
    )

    min_bathrooms = st.number_input(
        "Minimum Bathrooms",
        min_value=0,
        value=2
    )

    required_property_type = st.selectbox(
        "Preferred Property Type",
        ["Apartment", "House", "Studio", "Room"]
    )

    furnished_required = st.checkbox(
        "Furnished Required",
        value=True
    )

    parking_required = st.checkbox(
        "Parking Required",
        value=True
    )

    st.write("")

    investigate = st.button(
        "🚀 Investigate Property"
    )


# ============================================================
# RUN INVESTIGATION
# ============================================================

if investigate:

    property_data = {
        "title": title,
        "monthly_rent": monthly_rent,
        "location": location,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "property_type": property_type,
        "furnished": furnished,
        "parking": parking,
        "pets_allowed": pets_allowed,
        "description": description
    }

    user_requirements = {
        "max_monthly_budget": max_budget,
        "preferred_location": preferred_location,
        "min_bedrooms": min_bedrooms,
        "min_bathrooms": min_bathrooms,
        "property_type": required_property_type,
        "furnished_required": furnished_required,
        "parking_required": parking_required
    }

    with st.spinner(
        "🤖 RentWise AI is investigating this property..."
    ):

        try:

            results = run_investigation(
                property_data,
                user_requirements
            )

            st.session_state["investigation_results"] = results

            st.success(
                "✅ Investigation completed successfully!"
            )

        except Exception as e:

            st.error("❌ Investigation failed")

            st.exception(e)


# ============================================================
# RESULTS
# ============================================================

if "investigation_results" in st.session_state:

    results = st.session_state["investigation_results"]

    st.divider()

    st.markdown(
        '<div class="section-title">📊 Investigation Results</div>',
        unsafe_allow_html=True
    )

    price = results.get("price", {})
    location_result = results.get("location", {})
    requirements = results.get("requirements_analysis", {})
    risk = results.get("risk", {})


    # ========================================================
    # TOP METRICS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        price_status = (
            "Within Budget"
            if price.get("within_budget")
            else "Over Budget"
        )

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-label">Price</div>
            <div class="metric-value">{price_status}</div>
        </div>
        """, unsafe_allow_html=True)


    with c2:

        location_status = (
            "Match"
            if location_result.get("location_match")
            else "Mismatch"
        )

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📍</div>
            <div class="metric-label">Location</div>
            <div class="metric-value">{location_status}</div>
        </div>
        """, unsafe_allow_html=True)


    with c3:

        requirement_status = (
            "Match"
            if requirements.get("overall_match")
            else "Mismatch"
        )

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📋</div>
            <div class="metric-label">Requirements</div>
            <div class="metric-value">{requirement_status}</div>
        </div>
        """, unsafe_allow_html=True)


    with c4:

        risk_level = risk.get(
            "risk_level",
            "Unknown"
        )

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🛡️</div>
            <div class="metric-label">Risk Level</div>
            <div class="metric-value">{risk_level}</div>
        </div>
        """, unsafe_allow_html=True)


    # ========================================================
    # ANALYSIS SECTIONS
    # ========================================================

    st.write("")

    a1, a2 = st.columns(2)


    with a1:

        st.markdown("""
        <div class="info-card">
            <div class="card-title">💰 Price Analysis</div>
        """, unsafe_allow_html=True)

        st.write(
            price.get(
                "assessment",
                "No assessment available."
            )
        )

        st.markdown("</div>", unsafe_allow_html=True)


    with a2:

        st.markdown("""
        <div class="info-card">
            <div class="card-title">📍 Location Analysis</div>
        """, unsafe_allow_html=True)

        st.write(
            location_result.get(
                "assessment",
                "No assessment available."
            )
        )

        st.markdown("</div>", unsafe_allow_html=True)


    st.write("")


    a3, a4 = st.columns(2)


    with a3:

        st.markdown("""
        <div class="info-card">
            <div class="card-title">📋 Requirements Analysis</div>
        """, unsafe_allow_html=True)

        st.write(
            requirements.get(
                "assessment",
                "No assessment available."
            )
        )

        st.markdown("</div>", unsafe_allow_html=True)


    with a4:

        st.markdown("""
        <div class="risk-box">
            <div class="card-title">🛡️ Risk Analysis</div>
        """, unsafe_allow_html=True)

        st.write(
            risk.get(
                "assessment",
                "No assessment available."
            )
        )

        st.markdown("</div>", unsafe_allow_html=True)


    # ========================================================
    # LANDLORD QUESTIONS
    # ========================================================

    st.write("")

    st.markdown(
        '<div class="section-title">⚠️ Questions for the Landlord</div>',
        unsafe_allow_html=True
    )

    questions = risk.get(
        "questions_for_landlord",
        []
    )

    if questions:

        for question in questions:

            st.markdown(
                f"""
                <div class="question-box">
                    ❓ {question}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No additional questions were generated."
        )


    # ========================================================
    # RAW RESULT FOR DEBUGGING
    # ========================================================

    #with st.expander("🔧 View Investigation Data"):

     #   st.json(results)
