
import streamlit as st
from rentwise_backend import run_investigation

st.set_page_config(
    page_title="RentWise",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 RentWise")
st.subheader("Rent smarter. Investigate first.")

st.write(
    "Enter the property details and your rental requirements. "
    "RentWise will investigate the property using AI."
)

st.divider()

st.header("🔎 Investigate Property")

col1, col2 = st.columns(2)

with col1:
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

with col2:
    furnished = st.checkbox("Furnished", value=True)

    parking = st.checkbox("Parking Available", value=True)

    pets_allowed = st.checkbox("Pets Allowed", value=True)

    description = st.text_area(
        "Property Description",
        "Furnished apartment in F-11 with parking."
    )

    st.subheader("Your Requirements")

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

    furnished_required = st.checkbox(
        "Furnished Required",
        value=True
    )

    parking_required = st.checkbox(
        "Parking Required",
        value=True
    )


st.divider()

if st.button("🚀 Investigate Property", use_container_width=True):

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
        "property_type": property_type,
        "furnished_required": furnished_required,
        "parking_required": parking_required
    }

    with st.spinner("🤖 RentWise is investigating the property..."):

        try:
            results = run_investigation(
                property_data,
                user_requirements
            )

            st.session_state["investigation_results"] = results

            st.success("✅ Investigation completed!")

        except Exception as e:
            st.error("❌ Investigation failed")
            st.exception(e)


if "investigation_results" in st.session_state:

    results = st.session_state["investigation_results"]

    st.divider()

    st.header("📊 Investigation Results")

    col1, col2, col3, col4 = st.columns(4)

    price = results.get("price", {})
    location_result = results.get("location", {})
    requirements = results.get("requirements_analysis", {})
    risk = results.get("risk", {})

    with col1:
        st.metric(
            "💰 Price",
            "Within Budget" if price.get("within_budget") else "Over Budget"
        )

    with col2:
        st.metric(
            "📍 Location",
            "Match" if location_result.get("location_match") else "Mismatch"
        )

    with col3:
        st.metric(
            "📋 Requirements",
            "Match" if requirements.get("overall_match") else "Mismatch"
        )

    with col4:
        st.metric(
            "🛡️ Risk",
            risk.get("risk_level", "Unknown")
        )

    st.subheader("💰 Price Analysis")
    st.write(price.get("assessment", "No assessment available."))

    st.subheader("📍 Location Analysis")
    st.write(location_result.get("assessment", "No assessment available."))

    st.subheader("📋 Requirements Analysis")
    st.write(requirements.get("assessment", "No assessment available."))

    st.subheader("🛡️ Risk Analysis")
    st.write(risk.get("assessment", "No assessment available."))

    st.subheader("⚠️ Questions for the Landlord")

    questions = risk.get("questions_for_landlord", [])

    if questions:
        for question in questions:
            st.write("• " + question)
    else:
        st.write("No additional questions generated.")
