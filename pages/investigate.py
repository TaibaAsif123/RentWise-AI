import streamlit as st
import pandas as pd
from rentwise_backend import run_investigation, compare_properties
from property_search import search_properties

st.set_page_config(page_title="RentWise AI", page_icon="🏠",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp { background:#f7f8fc; }
.block-container { padding-top:2rem; padding-bottom:3rem; max-width:1400px; }
.hero { background:linear-gradient(135deg,#111827,#1f2937); padding:2.5rem;
        border-radius:24px; margin-bottom:2rem; color:white; }
.hero-title { font-size:3rem; font-weight:800; margin-bottom:.4rem; }
.hero-subtitle { font-size:1.1rem; color:#d1d5db; }
.section-title { font-size:1.6rem; font-weight:750; margin:1rem 0; color:#111827; }
.metric-card { background:white; padding:1.3rem; border-radius:18px;
               border:1px solid #e5e7eb; text-align:center; }
.metric-icon { font-size:1.7rem; }
.metric-label { color:#6b7280; font-size:.9rem; margin-top:.3rem; }
.metric-value { font-size:1.25rem; font-weight:750; margin-top:.3rem; color:#111827; }
.question-box { background:white; border:1px solid #e5e7eb; border-radius:14px;
                padding:1rem 1.2rem; margin-bottom:.7rem; }
.stButton > button { width:100%; border-radius:12px; height:3rem; font-weight:700; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="hero-title">🏠 RentWise AI</div>
  <div class="hero-subtitle">Rent smarter. Investigate before you commit.</div>
  <div style="margin-top:1rem;color:#9ca3af;">
    AI-assisted rental screening: it flags missing information and tells you what to ask.
  </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# HELPERS
# ============================================================

def val(row, *names):
    for n in names:
        if n in row.index and pd.notna(row[n]) and str(row[n]).strip():
            return row[n]
    return None


def row_to_property(row):
    beds, baths = int(row["bedroom_numeric"]), int(row["bath_numeric"])
    ptype = str(val(row, "type") or "Property")
    city_name = str(val(row, "location_city") or "")
    area = str(val(row, "location", "location_name", "address") or "")
    return {
        "title": str(val(row, "title", "name") or f"{beds} Bedroom {ptype}"),
        "monthly_rent": float(row["price_numeric"]),
        "location": f"{area}, {city_name}".strip(", "),
        "bedrooms": beds,
        "bathrooms": baths,
        "property_type": ptype,
        "furnished": "Not stated in listing",
        "parking": "Not stated in listing",
        "pets_allowed": "Not stated in listing",
        "description": str(val(row, "description", "details") or "No description in the dataset."),
    }


def bullets(items):
    for item in items or []:
        st.markdown(f"- {item}")


def metric(icon, label, value):
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-icon">{icon}</div>
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
    </div>""", unsafe_allow_html=True)


# ============================================================
# SEARCH FORM
# ============================================================

st.markdown('<div class="section-title">🔎 Find a Rental Property</div>', unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)
with f1:
    city = st.selectbox("City", ["Islamabad", "Rawalpindi"])
    max_budget = st.number_input("Maximum Monthly Budget (PKR)", min_value=0, value=100000, step=5000)
with f2:
    min_bedrooms = st.number_input("Minimum Bedrooms", min_value=0, max_value=10, value=2)
    min_bathrooms = st.number_input("Minimum Bathrooms", min_value=0, max_value=10, value=2)
with f3:
    property_type = st.selectbox("Property Type", ["Flat", "House", "Upper Portion", "Lower Portion", "Room"])
    furnished_required = st.checkbox("Furnished Required")
    parking_required = st.checkbox("Parking Required")

if st.button("🔎 Search Properties"):
    st.session_state["search_results"] = search_properties(
        city=city, max_budget=max_budget, min_bedrooms=min_bedrooms,
        min_bathrooms=min_bathrooms, property_type=property_type)
    st.session_state["user_requirements"] = {
        "max_monthly_budget": max_budget,
        "preferred_location": city,
        "min_bedrooms": min_bedrooms,
        "min_bathrooms": min_bathrooms,
        "property_type": property_type,
        "furnished_required": furnished_required,
        "parking_required": parking_required,
    }
    st.session_state["visible_count"] = 10
    st.session_state.pop("investigation_results", None)
    st.session_state["history"] = []        # new search = new comparison
    st.session_state.pop("ai_comparison", None)


# ============================================================
# RUN INVESTIGATION (triggered by a card button)
# ============================================================

if "to_investigate" in st.session_state:
    selected = st.session_state.pop("to_investigate")
    with st.spinner("🤖 RentWise AI is investigating this property..."):
        try:
            results = run_investigation(selected, st.session_state["user_requirements"])
            st.session_state["investigation_results"] = results

            history = st.session_state.setdefault("history", [])
            history[:] = [h for h in history if h["property"] != results["property"]]
            history.append(results)
            del history[:-5]                       # keep the last 5 only
            st.session_state.pop("ai_comparison", None)
        except Exception as e:
            st.error("❌ Investigation failed")
            st.exception(e)


# ============================================================
# RESULTS
# ============================================================

if "investigation_results" in st.session_state:
    results = st.session_state["investigation_results"]
    prop = results.get("property", {})
    price = results.get("price", {})
    loc = results.get("location", {})
    reqs = results.get("requirements_analysis", {})
    risk = results.get("risk", {})
    scores = results.get("scores", {})
    overall = results.get("overall", {})

    st.divider()
    st.markdown('<div class="section-title">📊 Investigation Results</div>', unsafe_allow_html=True)

    if not results.get("ai_used", True):
        st.warning("⚠️ AI analysis was unavailable, so this result uses RentWise's rule-based screening.")

    st.markdown(f"**{prop.get('title', '')}** · {prop.get('location', '')} · "
                f"PKR {prop.get('monthly_rent', 0):,.0f}/month")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: metric("⭐", "RentWise Score", f"{scores.get('final', 0)}/100")
    with c2: metric("💰", "Price", "Within Budget" if price.get("within_budget") else "Over Budget")
    with c3: metric("📍", "Location", "Match" if loc.get("location_match") else "Mismatch")
    with c4: metric("📋", "Requirements", "Match" if reqs.get("overall_match") else "Mismatch")
    with c5: metric("🛡️", "Risk Level", risk.get("risk_level", "Unknown"))

    st.write("")
    st.info(f"**Verdict: {overall.get('verdict', 'Proceed with caution')}.** "
            f"{overall.get('assessment', '')}")

    a1, a2 = st.columns(2)
    with a1:
        with st.container(border=True):
            st.markdown("**💰 Price Analysis**")
            st.write(price.get("assessment", "No assessment available."))
            bullets(price.get("missing_information"))
    with a2:
        with st.container(border=True):
            st.markdown("**📍 Location Analysis**")
            st.write(loc.get("assessment", "No assessment available."))
            bullets(loc.get("missing_information"))

    a3, a4 = st.columns(2)
    with a3:
        with st.container(border=True):
            st.markdown("**📋 Requirements Analysis**")
            st.write(reqs.get("assessment", "No assessment available."))
            if reqs.get("matched_requirements"):
                st.markdown("✅ Matched")
                bullets(reqs["matched_requirements"])
            if reqs.get("unmatched_requirements"):
                st.markdown("❌ Not matched")
                bullets(reqs["unmatched_requirements"])
            if reqs.get("missing_information"):
                st.markdown("❔ Could not verify")
                bullets(reqs["missing_information"])
    with a4:
        with st.container(border=True):
            st.markdown(f"**🛡️ Risk Analysis** (risk score {risk.get('risk_score', '-')}/100)")
            st.write(risk.get("assessment", "No assessment available."))
            if risk.get("concerns"):
                st.markdown("Concerns")
                bullets(risk["concerns"])
            if risk.get("warning_signs"):
                st.markdown("Warning signs")
                bullets(risk["warning_signs"])

    st.markdown('<div class="section-title">⚠️ Questions for the Landlord</div>', unsafe_allow_html=True)
    questions = risk.get("questions_for_landlord", [])
    if questions:
        for q in questions:
            st.markdown(f'<div class="question-box">❓ {q}</div>', unsafe_allow_html=True)
    else:
        st.info("No additional questions were generated.")


# ============================================================
# COMPARE INVESTIGATED PROPERTIES
# ============================================================

history = st.session_state.get("history", [])

if len(history) >= 2:
    st.divider()
    st.markdown('<div class="section-title">⚖️ Compare Investigated Properties</div>',
                unsafe_allow_html=True)

    rows = []
    for r in history:
        p = r["property"]
        rows.append({
            "Property": p.get("title"),
            "Location": p.get("location"),
            "Rent (PKR)": f"{p.get('monthly_rent', 0):,.0f}",
            "Score": r["scores"]["final"],
            "Price": "Within budget" if r["price"].get("within_budget") else "Over budget",
            "Location match": "Yes" if r["location"].get("location_match") else "No",
            "Requirements": "Match" if r["requirements_analysis"].get("overall_match") else "Mismatch",
            "Risk": r["risk"].get("risk_level"),
            "Verdict": r["overall"].get("verdict"),
        })

    table = pd.DataFrame(rows).sort_values("Score", ascending=False)
    st.dataframe(table, hide_index=True, use_container_width=True)

    best = table.iloc[0]
    st.success(f"Highest RentWise score: {best['Property']} ({best['Score']}/100)")

    b1, b2 = st.columns(2)
    with b1:
        if st.button("🤖 Get AI Recommendation"):
            with st.spinner("RentWise AI is comparing the properties..."):
                st.session_state["ai_comparison"] = compare_properties(history)
    with b2:
        if st.button("🗑️ Clear comparison"):
            st.session_state["history"] = []
            st.session_state.pop("ai_comparison", None)
            st.rerun()

    comparison = st.session_state.get("ai_comparison")
    if comparison:
        with st.container(border=True):
            st.markdown(f"**🏆 Recommended: {comparison.get('best_property', '')}**")
            st.write(comparison.get("recommendation", ""))
            if comparison.get("trade_offs"):
                st.markdown("Trade-offs")
                bullets(comparison["trade_offs"])
            if not comparison.get("ai_used", True):
                st.caption("AI was unavailable, so this recommendation uses the RentWise score only.")


# ============================================================
# PROPERTY CARDS
# ============================================================

found = st.session_state.get("search_results")

if found is not None:
    st.divider()
    st.markdown(f'<div class="section-title">🏘️ {len(found)} properties found</div>',
                unsafe_allow_html=True)

    if found.empty:
        st.info("No properties matched. Try a higher budget or fewer bedrooms/bathrooms.")
    else:
        found = found.sort_values("price_numeric")
        shown = st.session_state.get("visible_count", 10)

        for idx, row in found.head(shown).iterrows():
            p = row_to_property(row)
            with st.container(border=True):
                left, right = st.columns([4, 1])
                with left:
                    st.markdown(f"**🏠 {p['title']}**")
                    st.write(f"📍 {p['location']}")
                    st.write(f"💰 PKR {p['monthly_rent']:,.0f}/month  |  "
                             f"🛏 {p['bedrooms']} beds  |  🛁 {p['bathrooms']} baths  |  {p['property_type']}")
                with right:
                    if st.button("Investigate", key=f"inv_{idx}"):
                        st.session_state["to_investigate"] = p
                        st.rerun()

        if shown < len(found):
            if st.button("Show 10 more"):
                st.session_state["visible_count"] = shown + 10
                st.rerun()