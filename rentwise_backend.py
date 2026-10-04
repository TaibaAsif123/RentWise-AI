import os
import json
import re
import time
from google import genai


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# The app still starts without a key; it just runs in rule-based mode.
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
FALLBACK_MODELS = ["gemini-3.5-flash"]   # tried if the main model fails


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _clean_json_response(text):
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError("Gemini returned a response that could not be parsed as JSON.")


def _generate_json(prompt, max_retries=2, fallback_models=None):
    """Send a prompt to Gemini and return parsed JSON.
    Retries temporary errors and tries fallback models."""

    if client is None:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    if fallback_models is None:
        fallback_models = []

    models_to_try = [MODEL_NAME] + [m for m in fallback_models if m != MODEL_NAME]
    last_error = None

    for model_name in models_to_try:
        print(f"Trying Gemini model: {model_name}")

        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name, contents=prompt
                )
                if not response.text:
                    raise ValueError("Gemini returned an empty response.")

                result = _clean_json_response(response.text)
                print(f"✅ Successful response from {model_name}")
                return result

            except Exception as e:
                last_error = e
                error_text = str(e)

                temporary_error = (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                )

                if temporary_error:
                    if attempt < max_retries - 1:
                        wait_time = 5 * (attempt + 1)
                        print(f"Gemini temporarily unavailable ({model_name}). "
                              f"Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    print(f"⚠️ {model_name} failed after {max_retries} attempts.")
                    break

                raise

    raise last_error


# ============================================================
# PRICE ANALYSIS
# ============================================================

def analyze_price(property_data, user_requirements):
    prompt = f"""
You are RentWise, an AI rental property investigation system.

Analyze the rental price objectively.

PROPERTY:
{json.dumps(property_data, indent=2)}

USER REQUIREMENTS:
{json.dumps(user_requirements, indent=2)}

Return ONLY valid JSON using exactly this structure:

{{
    "rent": number,
    "budget": number,
    "difference": number,
    "within_budget": true or false,
    "assessment": "short explanation",
    "missing_information": [
        "item 1",
        "item 2"
    ]
}}

Consider possible missing costs such as:
- security deposit
- utilities
- maintenance
- parking fees
- agent fees

Do not invent missing information.
"""
    return _generate_json(prompt, fallback_models=FALLBACK_MODELS)


# ============================================================
# LOCATION ANALYSIS
# ============================================================

def analyze_location(property_data, user_requirements):
    prompt = f"""
You are RentWise, an AI rental property investigation system.

Analyze the property's location.

PROPERTY:
{json.dumps(property_data, indent=2)}

USER REQUIREMENTS:
{json.dumps(user_requirements, indent=2)}

Return ONLY valid JSON using exactly this structure:

{{
    "property_location": "string",
    "preferred_location": "string",
    "location_match": true or false,
    "assessment": "short explanation",
    "missing_information": [
        "item 1",
        "item 2"
    ]
}}

Pay attention to missing details such as:
- exact street
- block/sector
- building name
- nearby amenities
- public transport
- main roads

Do not invent missing information.
"""
    return _generate_json(prompt, fallback_models=FALLBACK_MODELS)


# ============================================================
# REQUIREMENTS ANALYSIS
# ============================================================

def analyze_requirements(property_data, user_requirements):
    prompt = f"""
You are RentWise, an AI rental property investigation system.

Compare the property against the user's requirements.

PROPERTY:
{json.dumps(property_data, indent=2)}

USER REQUIREMENTS:
{json.dumps(user_requirements, indent=2)}

Check:
- bedrooms
- bathrooms
- property type
- furnished status
- parking
- pets if information is available
- other explicitly provided requirements

Return ONLY valid JSON using exactly this structure:

{{
    "overall_match": true or false,
    "matched_requirements": [
        "requirement 1"
    ],
    "unmatched_requirements": [
        "requirement 1"
    ],
    "missing_information": [
        "item 1"
    ],
    "assessment": "short explanation"
}}

Do not invent information.
"""
    return _generate_json(prompt, fallback_models=FALLBACK_MODELS)


# ============================================================
# RISK ANALYSIS
# ============================================================

def analyze_risk(property_data, user_requirements):
    prompt = f"""
You are RentWise, an AI rental property investigation system.

Perform a rental-property risk assessment.

PROPERTY:
{json.dumps(property_data, indent=2)}

USER REQUIREMENTS:
{json.dumps(user_requirements, indent=2)}

Look for:
- missing address information
- missing landlord/agent verification
- unclear deposit
- unclear lease terms
- unclear utilities
- unclear maintenance charges
- suspicious or contradictory information
- unrealistic claims
- missing important details

Do NOT accuse the landlord or property of fraud without evidence.

Return ONLY valid JSON using exactly this structure:

{{
    "risk_level": "Low Risk" or "Medium Risk" or "High Risk",
    "risk_score": number,
    "concerns": [
        "concern 1"
    ],
    "missing_information": [
        "item 1"
    ],
    "warning_signs": [
        "warning 1"
    ],
    "questions_for_landlord": [
        "question 1"
    ],
    "assessment": "short explanation",
    "verdict": "Proceed" or "Proceed with caution" or "Do not proceed"
}}

Use a risk_score from 0 to 100 where:
0 = extremely low risk
100 = extremely high risk.

Base the assessment only on the information provided.
"""
    return _generate_json(prompt, fallback_models=FALLBACK_MODELS)


# ============================================================
# RULE-BASED FALLBACK (no AI needed)
# ============================================================

def _rule_based_analysis(property_data, user_requirements):
    """Used when Gemini is unavailable (quota, network, missing key)."""

    rent = float(property_data.get("monthly_rent") or 0)
    budget = float(user_requirements.get("max_monthly_budget") or 0)
    within = rent <= budget

    loc = str(property_data.get("location", ""))
    pref = str(user_requirements.get("preferred_location", ""))
    loc_match = bool(pref) and pref.lower() in loc.lower()

    matched, unmatched, missing = [], [], []

    def check(label, ok):
        (matched if ok else unmatched).append(label)

    check("Bedrooms",
          (property_data.get("bedrooms") or 0) >= user_requirements.get("min_bedrooms", 0))
    check("Bathrooms",
          (property_data.get("bathrooms") or 0) >= user_requirements.get("min_bathrooms", 0))

    req_type = str(user_requirements.get("property_type", "")).lower()
    if req_type:
        check("Property type",
              req_type == str(property_data.get("property_type", "")).lower())

    for key, req_key, label in [
        ("furnished", "furnished_required", "Furnished"),
        ("parking", "parking_required", "Parking"),
    ]:
        if user_requirements.get(req_key):
            value = property_data.get(key)
            if value is True:
                matched.append(label)
            elif value is False:
                unmatched.append(label)
            else:
                missing.append(f"{label} status is not stated in the listing")

    price = {
        "rent": rent,
        "budget": budget,
        "difference": budget - rent,
        "within_budget": within,
        "assessment": (
            f"Rent is PKR {rent:,.0f} against a budget of PKR {budget:,.0f}. "
            + ("It is within budget." if within else "It exceeds the budget.")
        ),
        "missing_information": [
            "Security deposit", "Maintenance charges", "Utility arrangements"
        ],
    }

    location = {
        "property_location": loc,
        "preferred_location": pref,
        "location_match": loc_match,
        "assessment": (
            "The listed location matches the preferred area." if loc_match
            else "The listed location does not clearly match the preferred area."
        ),
        "missing_information": ["Exact street/block", "Nearby amenities"],
    }

    requirements = {
        "overall_match": not unmatched,
        "matched_requirements": matched,
        "unmatched_requirements": unmatched,
        "missing_information": missing,
        "assessment": (
            f"{len(matched)} requirement(s) matched, {len(unmatched)} not matched, "
            f"{len(missing)} could not be verified."
        ),
    }

    risk = {
        "risk_level": "Medium Risk",
        "risk_score": min(70, 40 + 5 * len(missing)),
        "concerns": [
            "Listing lacks deposit, maintenance, utility and ownership details."
        ],
        "missing_information": [
            "Security deposit", "Maintenance charges", "Utilities",
            "Owner/agent verification",
        ] + missing,
        "warning_signs": [],
        "questions_for_landlord": [
            "What is the security deposit and is it refundable?",
            "Are maintenance charges included in the rent?",
            "How are electricity, gas and water billed?",
            "Can you share proof of ownership or authorization to rent?",
            "What are the lease length and notice terms?",
        ],
        "assessment": (
            "Rule-based screening only. Missing details are not signs of fraud, "
            "but should be verified before committing."
        ),
        "verdict": "Proceed with caution",
    }

    return price, location, requirements, risk


# ============================================================
# FULL INVESTIGATION
# ============================================================

def run_investigation(property_data, user_requirements):
    """Run the complete RentWise investigation.
    Uses Gemini; falls back to rule-based screening if it fails."""

    ai_used = True
    try:
        price_result = analyze_price(property_data, user_requirements)
        location_result = analyze_location(property_data, user_requirements)
        requirements_result = analyze_requirements(property_data, user_requirements)
        risk_result = analyze_risk(property_data, user_requirements)
    except Exception as e:
        print(f"Gemini unavailable, using rule-based fallback: {e}")
        ai_used = False
        (price_result, location_result,
         requirements_result, risk_result) = _rule_based_analysis(
            property_data, user_requirements
        )

    # ---------------- scores ----------------

    requirements_score = 100 if requirements_result.get("overall_match", False) else 50
    price_score = 100 if price_result.get("within_budget", False) else 0
    location_score = 100 if location_result.get("location_match", False) else 0

    risk_level = risk_result.get("risk_level", "Medium Risk")
    if risk_level == "Low Risk":
        risk_score = 100
    elif risk_level == "Medium Risk":
        risk_score = 60
    else:
        risk_score = 20

    final_score = round(
        requirements_score * 0.30
        + price_score * 0.25
        + location_score * 0.25
        + risk_score * 0.20,
        1,
    )

    # ---------------- overall assessment ----------------

    if final_score >= 85:
        overall_assessment = (
            "Strong match with the provided requirements, "
            "but normal rental verification is still recommended."
        )
    elif final_score >= 70:
        overall_assessment = (
            "Good potential match, but several details should "
            "be verified before making a decision."
        )
    elif final_score >= 50:
        overall_assessment = (
            "The property has some positive aspects, but "
            "important concerns should be investigated."
        )
    else:
        overall_assessment = (
            "The property does not currently provide enough "
            "confidence to recommend proceeding."
        )

    summary = (
        f"The property is assessed with a RentWise score of {final_score}/100. "
        f"It is evaluated as {risk_level.lower()} based on "
        f"the information currently available."
    )

    return {
        "ai_used": ai_used,
        "property": property_data,
        "requirements": user_requirements,

        "price": price_result,
        "location": location_result,
        "requirements_analysis": requirements_result,
        "risk": risk_result,

        "scores": {
            "requirements": requirements_score,
            "price": price_score,
            "location": location_score,
            "risk": risk_score,
            "final": final_score,
        },

        "overall": {
            "assessment": overall_assessment,
            "summary": summary,
            "verdict": risk_result.get("verdict", "Proceed with caution"),
        },
    }


# ============================================================
# COMPARE MULTIPLE PROPERTIES
# ============================================================

def compare_properties(results_list):
    """Recommend the best property among already-investigated ones.
    One Gemini call; falls back to 'highest score wins'."""

    summaries = []
    for r in results_list:
        p = r["property"]
        summaries.append({
            "title": p.get("title"),
            "location": p.get("location"),
            "monthly_rent": p.get("monthly_rent"),
            "bedrooms": p.get("bedrooms"),
            "bathrooms": p.get("bathrooms"),
            "rentwise_score": r["scores"]["final"],
            "within_budget": r["price"].get("within_budget"),
            "location_match": r["location"].get("location_match"),
            "requirements_match": r["requirements_analysis"].get("overall_match"),
            "risk_level": r["risk"].get("risk_level"),
            "concerns": r["risk"].get("concerns", [])[:3],
        })

    best_by_score = max(summaries, key=lambda s: s["rentwise_score"])

    prompt = f"""
You are RentWise, an AI rental property investigation system.

Compare these already-investigated rental properties and recommend
which one best fits the renter. Base your answer only on the data below.
Do not invent facts and do not accuse anyone of fraud.

PROPERTIES:
{json.dumps(summaries, indent=2)}

Return ONLY valid JSON using exactly this structure:

{{
    "best_property": "title of the recommended property",
    "recommendation": "2-3 sentence explanation",
    "trade_offs": [
        "trade-off 1",
        "trade-off 2"
    ]
}}
"""

    try:
        result = _generate_json(prompt, fallback_models=FALLBACK_MODELS)
        result["ai_used"] = True
        return result
    except Exception as e:
        print(f"Comparison fallback used: {e}")
        return {
            "best_property": best_by_score["title"],
            "recommendation": (
                f"{best_by_score['title']} has the highest RentWise score "
                f"({best_by_score['rentwise_score']}/100). This ranking uses the "
                f"score only, because AI analysis was unavailable."
            ),
            "trade_offs": [
                "Verify deposit, maintenance and ownership details for every property."
            ],
            "ai_used": False,
        }